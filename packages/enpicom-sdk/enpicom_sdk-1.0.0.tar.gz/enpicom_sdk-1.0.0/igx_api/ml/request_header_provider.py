"""@private
Nothing in this module is useful for customers to invoke directly, hide it from the docs.

Gets the public API key from the environment variable and adds it to the header of all requests
performed by MLflow
"""

import os

from mlflow.tracking.request_header.abstract_request_header_provider import RequestHeaderProvider

API_KEY = os.environ["IGX_API_KEY"]
USER_ID = os.environ.get("USER_ID")
USER_ORG_ID = os.environ.get("USER_ORG_ID")


class PluginRequestHeaderProvider(RequestHeaderProvider):
    """RequestHeaderProvider provided through plugin system"""

    def in_context(self):
        return True

    def request_headers(self):
        headers = {"igx-api-key": API_KEY}

        if USER_ID is not None and USER_ORG_ID is not None:
            headers.update({"igx-user-id": str(USER_ID), "igx-user-org-id": str(USER_ORG_ID)})

        return headers
