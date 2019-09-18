"""
Client for the Auth0 Authorization Extension API

XXX: not function-complete
"""

from auth0.v3 import management
from django.conf import settings


class Authorization:
    """
    Provides an interface to the Authorization Extension API similar to the one
    the official Auth0 module provides for Management API
    """
    def __init__(self, domain, token):
        base_url = settings.OIDC_OP_AUTHORIZATION_ENDPOINT
        if not base_url.endswith('/'):
            base_url += '/'

        self.groups = Groups(domain, token, base_url)
        self.users = Users(domain, token, base_url)


class Endpoints:
    """
    Base class for authorization API endpoints classes
    """
    def __init__(self, domain, token, base_url, telemetry=True):
        self.base_url = base_url
        self.client = management.RestClient(jwt=token, telemetry=telemetry)
        self.domain = domain

    def _url(self, id=None):
        url = f'{self.base_url}/{self.endpoint_prefix}'
        if id is not None:
            return f'{url}/{id}'
        return url


class Groups(Endpoints):
    """
    Auth0 authorization groups endpoints
    """

    endpoint_prefix = 'groups'

    def list(self):
        """Get all groups

        See https://auth0.com/docs/api/authorization-extension#get-all-groups
        """
        return self.client.get(self._url())

    def get(self, id):
        """Get a single group

        Args:
            id (str): The group id

        See https://auth0.com/docs/api/authorization-extension#get-a-single-group
        """
        return self.client.get(self._url(id))

    def list_members(self, id, page=1, per_page=25):
        """List group members

        Args:
            id (str): The group id

            page (int, optional): The result page number (1-based)

            per_page (int, optional): The number of entries per page (max 25).

        See https://auth0.com/docs/api/authorization-extension#get-group-members
        """
        params = {
            'page': page,
            'per_page': per_page,
        }
        url = f'{self._url(id)}/members'
        return self.client.get(url, params=params)

    def add_members(self, id, user_ids):
        """Add one or more members to a group

        Args:
            id (str): The group id

            user_ids (list[str]): A list of user ids

        See https://auth0.com/docs/api/authorization-extension#add-group-members
        """
        url = f'{self._url(id)}/members'
        return self.client.patch(url, data=user_ids)

    def delete_members(self, id, user_ids):
        """Remove one or more members from a group

        Args:
            id (str): The group id

            user_ids (list[str]): A list of user ids

        See https://auth0.com/docs/api/authorization-extension#delete-group-members
        """
        url = f'{self._url(id)}/members'
        return self.client.delete(url, data=user_ids)


class Users(Endpoints):
    """
    Auth0 authorization users endpoints
    """

    endpoint_prefix = 'users'

    def list(self, page=1, per_page=100):
        """List users

        Args:
            page (int, optional): The result page number (1-based)

            per_page (int, optional): The number of entries per page (max 200)

        See https://auth0.com/docs/api/authorization-extension#get-all-users
        """
        params = {
            'page': page,
            'per_page': per_page,
        }
        return self.client.get(self._url(), params=params)

