# -*- coding: utf-8 -*-
"""
Arkindex API Client
"""
import logging
import os
import warnings
from time import sleep
from urllib.parse import urljoin, urlsplit, urlunsplit

import requests
import yaml
from tenacity import (
    before_sleep_log,
    retry,
    retry_if_exception,
    stop_after_attempt,
    wait_exponential,
)

from arkindex.auth import TokenSessionAuthentication
from arkindex.client.base import BaseClient
from arkindex.exceptions import ErrorResponse, SchemaError
from arkindex.pagination import ResponsePaginator

logger = logging.getLogger(__name__)

try:
    from yaml import CSafeLoader as SafeLoader

    logger.debug("Using LibYAML-based parser")
except ImportError:
    from yaml import SafeLoader

    logger.debug("Using default PyYAML parser")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DEFAULT_BASE_URL = "https://arkindex.teklia.com/"

# Endpoint accessed by the client on instantiation to retrieve the OpenAPI schema
SCHEMA_ENDPOINT = "/api/v1/openapi/?format=json"


def _is_500_error(exc: Exception) -> bool:
    """
    Check if an Arkindex API error is a 50x
    This is used to retry most API calls implemented here
    """
    if not isinstance(exc, ErrorResponse):
        return False

    return 500 <= exc.status_code < 600


def options_from_env():
    """
    Get API client keyword arguments from environment variables.
    """
    options = {}
    # ARKINDEX_TASK_TOKEN takes priority over ARKINDEX_API_TOKEN
    if "ARKINDEX_TASK_TOKEN" in os.environ:
        options["auth_scheme"] = "Ponos"
        options["token"] = os.environ.get("ARKINDEX_TASK_TOKEN")
    elif "ARKINDEX_API_TOKEN" in os.environ:
        options["auth_scheme"] = "Token"
        options["token"] = os.environ.get("ARKINDEX_API_TOKEN")

    # Allow overriding the default auth schemes
    if "ARKINDEX_API_AUTH_SCHEME" in os.environ:
        options["auth_scheme"] = os.environ.get("ARKINDEX_API_AUTH_SCHEME")

    if "ARKINDEX_API_URL" in os.environ:
        options["base_url"] = os.environ.get("ARKINDEX_API_URL")

    if "ARKINDEX_API_SCHEMA_URL" in os.environ:
        options["schema_url"] = os.environ.get("ARKINDEX_API_SCHEMA_URL")

    if "ARKINDEX_API_CSRF_COOKIE" in os.environ:
        options["csrf_cookie"] = os.environ.get("ARKINDEX_API_CSRF_COOKIE")

    return options


def _find_operation(schema, operation_id):
    for path_object in schema["paths"].values():
        for operation in path_object.values():
            if operation["operationId"] == operation_id:
                return operation
    raise KeyError("Operation '{}' not found".format(operation_id))


def _find_param(operation, param_name):
    for parameter in operation.get("parameters", []):
        if parameter["name"] == param_name:
            return parameter
    raise KeyError("Parameter '{}' not found".format(param_name))


class ArkindexClient(BaseClient):
    """
    An Arkindex API client.
    """

    def __init__(
        self,
        token=None,
        auth_scheme="Token",
        base_url=DEFAULT_BASE_URL,
        schema_url=None,
        csrf_cookie=None,
        sleep=0,
        verify=True,
        **kwargs,
    ):
        r"""
        :param token: An API token to use. If omitted, access is restricted to public endpoints.
        :type token: str or None
        :param str base_url: A custom base URL for the client. If omitted, defaults to the Arkindex main server.
        :param schema_url: URL or local path to an OpenAPI schema to use instead of the Arkindex instance's own schema.
        :type schema_url: str or None
        :param csrf_cookie: Use a custom CSRF cookie name. By default, the client will try to use any cookie
           defined in ``x-csrf-cookie`` on the Server Object of the OpenAPI specification, and fall back to
           ``arkindex.csrf``.
        :type csrf_cookie: str or None
        :param float sleep: Number of seconds to wait before sending each API request,
           as a simple means of throttling.
        :param \**kwargs: Keyword arguments to send to ``arkindex.client.base.BaseClient``.
        """
        if not schema_url:
            schema_url = urljoin(base_url, SCHEMA_ENDPOINT)

        self.verify = verify
        try:
            split = urlsplit(schema_url)
            if split.scheme == "file" or not (split.scheme or split.netloc):
                # This is a local path
                with open(schema_url) as f:
                    schema = yaml.load(f, Loader=SafeLoader)
            else:
                resp = requests.get(schema_url, verify=self.verify)
                resp.raise_for_status()
                schema = yaml.load(resp.content, Loader=SafeLoader)
        except Exception as e:
            raise SchemaError(
                f"Could not retrieve a proper OpenAPI schema from {schema_url}"
            ) from e

        super().__init__(schema, **kwargs)

        # An OpenAPI schema is considered valid even when there are no endpoints, making the client completely useless.
        if not len(self.document.walk_links()):
            raise SchemaError(
                f"The OpenAPI schema from {base_url} has no defined endpoints"
            )

        # Post-processing of the parsed schema
        for link_info in self.document.walk_links():
            # Look for deprecated links
            # https://github.com/encode/apistar/issues/664
            operation = _find_operation(schema, link_info.link.name)
            link_info.link.deprecated = operation.get("deprecated", False)
            for item in link_info.link.get_query_fields():
                parameter = _find_param(operation, item.name)
                item.deprecated = parameter.get("deprecated", False)

            # Detect paginated links
            if "x-paginated" in operation:
                link_info.link._paginated = operation["x-paginated"]

            # Remove domains from each endpoint; allows to properly handle our base URL
            # https://github.com/encode/apistar/issues/657
            original_url = urlsplit(link_info.link.url)
            # Removes the scheme and netloc
            new_url = ("", "", *original_url[2:])
            link_info.link.url = urlunsplit(new_url)

        # Try to autodetect the CSRF cookie:
        # - Try to find a matching server for this base URL and look for the x-csrf-cookie extension
        # - Fallback to arkindex.csrf
        if not csrf_cookie:
            split_base_url = urlsplit(base_url or self.document.url)
            csrf_cookies = {
                urlsplit(server.get("url", "")).netloc: server.get("x-csrf-cookie")
                for server in schema.get("servers", [])
            }
            csrf_cookie = csrf_cookies.get(split_base_url.netloc) or "arkindex.csrf"

        self.configure(
            token=token,
            auth_scheme=auth_scheme,
            base_url=base_url,
            csrf_cookie=csrf_cookie,
            sleep=sleep,
        )

    def __repr__(self):
        return "<{} on {!r}>".format(
            self.__class__.__name__,
            self.document.url if hasattr(self, "document") else "",
        )

    def configure(
        self,
        token=None,
        auth_scheme="Token",
        base_url=None,
        csrf_cookie=None,
        sleep=None,
    ):
        """
        Reconfigure the API client.

        :param token: An API token to use. If omitted, access is restricted to public endpoints.
        :type token: str or None
        :param auth_scheme:
           An authentication scheme to use. This is added in the HTTP header before the token:
           ``Authorization: [scheme] [token]``.
           This should use ``Token`` to authenticate as a regular user and ``Ponos`` to authenticate as a Ponos task.
           If omitted, this defaults to ``Token``.
        :type auth_scheme: str or None
        :param base_url: A custom base URL for the client. If omitted, defaults to the Arkindex main server.
        :type base_url: str or None
        :param csrf_cookie: Use a custom CSRF cookie name. Falls back to ``arkindex.csrf``.
        :type csrf_cookie: str or None
        :param float sleep: Number of seconds to wait before sending each API request,
           as a simple means of throttling.
        """
        if not csrf_cookie:
            csrf_cookie = "arkindex.csrf"
        self.transport.session.auth = TokenSessionAuthentication(
            token,
            csrf_cookie_name=csrf_cookie,
            scheme=auth_scheme,
        )

        if not sleep or not isinstance(sleep, float) or sleep < 0:
            self.sleep_duration = 0
        self.sleep_duration = sleep

        if base_url:
            self.document.url = base_url

        # Add the Referer header to allow Django CSRF to function
        self.transport.headers.setdefault("Referer", self.document.url)

    def paginate(self, operation_id, *args, **kwargs):
        """
        Perform a usual API request, but handle paginated endpoints.

        :return: An iterator for a paginated endpoint.
        :rtype: Union[arkindex.pagination.ResponsePaginator, dict, list]
        """
        link = self.lookup_operation(operation_id)
        # If there was no x-paginated, trust the caller and assume the endpoint is paginated
        if getattr(link, "_paginated", True):
            return ResponsePaginator(self, operation_id, *args, **kwargs)
        return self.request(operation_id, *args, **kwargs)

    def login(self, email, password):
        """
        Login to Arkindex using an email/password combination.
        This helper method automatically sets the client's authentication settings with the token.
        """
        resp = self.request("Login", body={"email": email, "password": password})
        if "auth_token" in resp:
            self.transport.session.auth.scheme = "Token"
            self.transport.session.auth.token = resp["auth_token"]
        return resp

    def single_request(self, operation_id, *args, **kwargs):
        """
        Perform an API request.
        :param args: Arguments passed to the BaseClient.
        :param kwargs: Keyword arguments passed to the BaseClient.
        """
        link = self.lookup_operation(operation_id)
        if link.deprecated:
            warnings.warn(
                "Endpoint '{}' is deprecated.".format(operation_id),
                DeprecationWarning,
                stacklevel=2,
            )

        query_params = self.get_query_params(link, kwargs)
        fields = link.get_query_fields()
        for field in fields:
            if field.deprecated and field.name in query_params:
                warnings.warn(
                    "Parameter '{}' is deprecated.".format(field.name),
                    DeprecationWarning,
                    stacklevel=2,
                )
        if self.sleep_duration:
            logger.debug(
                "Delaying request by {:f} seconds...".format(self.sleep_duration)
            )
            sleep(self.sleep_duration)
        return super().request(operation_id, *args, **kwargs)

    @retry(
        retry=retry_if_exception(_is_500_error),
        wait=wait_exponential(multiplier=2, min=3),
        reraise=True,
        stop=stop_after_attempt(5),
        before_sleep=before_sleep_log(logger, logging.INFO),
    )
    def request(self, operation_id, *args, **kwargs):
        """
        Proxy all Arkindex API requests with a retry mechanism in case of 50X errors.
        The same API call will be retried 5 times, with an exponential sleep time
        going through 3, 4, 8 and 16 seconds of wait between call.
        If the 5th call still gives a 50x, the exception is re-raised and the caller should catch it.
        Log messages are displayed before sleeping (when at least one exception occurred).

        :param args: Arguments passed to the BaseClient.
        :param kwargs: Keyword arguments passed to the BaseClient.
        """
        return self.single_request(operation_id, *args, **kwargs)
