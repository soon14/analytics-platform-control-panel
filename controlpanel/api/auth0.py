import auth0.v3
from django.conf import settings
import requests
from rest_framework.exceptions import APIException

from controlpanel.auth0_authorization_extension import Authorization


class Auth0Error(APIException):
    status_code = 500
    default_code = "auth0_error"
    default_detail = "Error querying Auth0 API"


def get_access_token(audience):
    get_token = auth0.v3.authentication.GetToken(settings.OIDC_DOMAIN)

    try:
        token = get_token.client_credentials(
            settings.OIDC_RP_CLIENT_ID,
            settings.OIDC_RP_CLIENT_SECRET,
            audience,
        )

    except auth0.v3.exceptions.Auth0Error as error:
        raise Auth0Error(
            f"Failed getting Auth0 access token for client "
            f"{settings.OIDC_RP_CLIENT_ID} for audience {audience} "
            f"at {settings.OIDC_DOMAIN}: {error}"
        )

    return token["access_token"]


def authorization():
    return Authorization(
        settings.OIDC_DOMAIN,
        get_access_token(audience='urn:auth0-authz-api'),
    )


def management():
    return auth0.v3.management.Auth0(
        settings.OIDC_DOMAIN,
        get_access_token(audience=f'https://{settings.OIDC_DOMAIN}/api/v2/'),
    )


def get_all(self, getter_fn, results_key, start_page=0):
    """
    Request consecutive pages of results until no more pages and return the
    aggregated list of results
    """
    items = []
    page = start_page
    total = None
    while True:
        response = getter_fn(page)

        if "total" not in response:
            raise Auth0Error(f"get_all: Missing total")

        if key not in response:
            raise Auth0Error(f"get_all: Missing key {results_key}")

        if total is None:
            total = response["total"]

        if total != response["total"]:
            raise Auth0Error(f"get_all: Total changed")

        items.extend(response[results_key])

        if len(items) >= total:
            break

        if len(response[results_key]) < 1:
            break

        page += 1

    return items


def get_users():
    mgmt = management()

    def users_page(page):
        return mgmt.users.list(
            include_totals=True,
            page=page,
            per_page=100,  # max value 100 :/
            q='identities.connection:"github"',
        )

    return get_all(users_page, 'users')


def get_group_by_name(group_name, api=None):
    api = api or authorization()
    groups = api.groups.list()
    return next(group for group in groups if group['name'] == group_name)


def get_customers(group_name):
    api = api or authorization()
    group = get_group_by_name(group_name, api)
    return get_all(
        lambda page: api.groups.list_members(group['id'], page),
        start_page=1,
    )

def add_customers(group_name, emails):
    authz = authorization()
    mgmt = management()
    group = get_group_by_name(group_name, api=authz)
    # get all existing customers (in all groups)
    # TODO - cache this?
    customers = {
        user['email']: user
        for users in get_all(
            lambda page: authz.users.list(page, per_page=200),
            start_page=1,
        )
        if 'email' in user
    }
    # map input emails to user ids
    user_ids = []
    for email in emails:
        user = customers.get(email)
        if user:
            if not any(
                identity['connection'] == 'email'
                for identity in user['identities']
            ):
                # user doesn't exist, so create them and add them to the group
                nickname, _, _ = email.partition('@')
                user = mgmt.users.create({
                    email=email,
                    email_verified=True,
                    connection='email',
                    nickname=nickname,
                })
                user_ids.append(user['user_id'])

    authz.groups.add_members(group['id'], user_ids)


def delete_customers(group_name, user_ids):
    group = get_group(group_name)
    authorization().groups.delete_members(group['id'], user_ids)


def get_user_identity(user_id, provider):
    user = management().users.get(user_id)
    for identity in user['identities']:
        if identity['provider'] == provider:
            return identity


def reset_mfa(user_id):
    management().users.delete_multifactor(user_id, 'google-authenticator')


def get_or_create_client(name, **params):
    mgmt = management()
    client = next(
        (client for client in mgmt.clients.all() if client['name'] == name),
        None,
    )
    if client is None:
        client = mgmt.clients.create({'name': name, **params})
    else:
        log.warning(f"Reusing existing Auth0 client for {app.name}")
    return client

