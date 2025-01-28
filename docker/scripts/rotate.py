"""
Python 3.6+
pip(3) install requests
"""
import base64
import json
import requests
import sys
import datetime

# ARGS

ARG_WIZ_CLIENT_ID       = 1
ARG_WIZ_CLIENT_SECRET   = 2
ARG_FORCE_ROTATE        = 3

# Pass in Runtime Variables
wiz_client_id       = sys.argv[ARG_WIZ_CLIENT_ID]
wiz_client_secret   = sys.argv[ARG_WIZ_CLIENT_SECRET]
force_rotate        = False

def validate_runtime_variables():

    global force_rotate

    # Validate force_rotate flag
    try:
        force_rotate    = sys.argv[ARG_FORCE_ROTATE]

        if force_rotate == "True":
            force_rotate = True
        elif force_rotate == "False":
            force_rotate = False
        else:
            raise TypeError(f"force_rotate option must be \"True\" or \"False\".")
        
    except IndexError:
        print("No force rotate flag was specified, assuming we don't wish to force rotation this time.")
        sys.exit(1)


# Standard headers
HEADERS_AUTH = {"Content-Type": "application/x-www-form-urlencoded"}
HEADERS = {"Content-Type": "application/json"}

# Validate Arguments

# Query to fetch service account info from Wiz

def get_qry_service_account_info():
    return """
        query ServiceAccountsTable($first: Int, $after: String, $filterBy: ServiceAccountFilters) {
        serviceAccounts(first: $first, after: $after, filterBy: $filterBy) {
            nodes {
            ...ServiceAccount
            type
            assignedProjects {
                id
                name
            }
            createdAt
            expiresAt
            }
            pageInfo {
            hasNextPage
            endCursor
            }
            totalCount
        }
        }
        
            fragment ServiceAccount on ServiceAccount {
        id
        enabled
        name
        clientId
        scopes
        lastRotatedAt
        expiresAt
        integration {
            id
            name
            typeConfiguration {
            type
            iconUrl
            }
        }
        }
    """

def get_qryvars_service_account_info(wiz_client_id):
# The variables sent along with the above query
    return {
            "first": 20,
            "filterBy": {
                "name": wiz_client_id,
                "type": [
                    "THIRD_PARTY"
                    ],
                "source": "MODERN"
            }
        }

# The GraphQL query that defines which data you wish to fetch.
def get_qry_rotate_sa_secret():
    return """
        mutation RotateServiceAccountSecret($input: String!) {
        rotateServiceAccountSecret(ID: $input) {
            serviceAccount {
            ...ServiceAccount
            clientSecret
            }
        }
        }
        
            fragment ServiceAccount on ServiceAccount {
        id
        enabled
        name
        clientId
        scopes
        lastRotatedAt
        expiresAt
        integration {
            id
            name
            typeConfiguration {
            type
            iconUrl
            }
        }
        }
    """

# The variables sent along with the above query
def get_qryvars_rotate_sa_secret(client_id):
    return {
            "input": client_id
        }

def get_qry_patch_sa_expiry():

    return """
        mutation UpdateServiceAccount($input: UpdateServiceAccountInput!) {
        updateServiceAccount(input: $input) {
            serviceAccount {
            ...ServiceAccount
            clientSecret
            }
        }
        }
        
            fragment ServiceAccount on ServiceAccount {
        id
        enabled
        name
        clientId
        scopes
        lastRotatedAt
        expiresAt
        integration {
            id
            name
            typeConfiguration {
            type
            iconUrl
            }
        }
        }
    """

# The variables sent along with the above query
def get_qryvars_patch_sa_expiry(client_id, new_expiry_date):
    return {
        "input": {
            "serviceAccountId": client_id,
            "patch": {
                "expiresAt": new_expiry_date
            }
        }
    }

def query_wiz_api(query, variables, dc):
    """Query Wiz API for the given query data schema"""

    data = {"variables": variables, "query": query}

    try:
        # Uncomment the next first line and comment the line after that
        # to run behind proxies
        # result = requests.post(url=f"https://api.{dc}.app.wiz.io/graphql",
        #                        json=data, headers=HEADERS, proxies=proxyDict, timeout=180)
        result = requests.post(url=f"https://api.{dc}.app.wiz.io/graphql",
                               json=data, headers=HEADERS, timeout=180)

    except requests.exceptions.HTTPError as e:
        print(f"<p>Wiz-API-Error (4xx/5xx): {str(e)}</p>")
        return e

    except requests.exceptions.ConnectionError as e:
        print(f"<p>Network problem (DNS failure, refused connection, etc): {str(e)}</p>")
        return e

    except requests.exceptions.Timeout as e:
        print(f"<p>Request timed out: {str(e)}</p>")
        return e

    return result.json()


def request_wiz_api_token(client_id, client_secret):
    """Retrieve an OAuth access token to be used against Wiz API"""

    auth_payload = {
      'grant_type': 'client_credentials',
      'audience': 'wiz-api',
      'client_id': client_id,
      'client_secret': client_secret
    }
    try:
        # Uncomment the next first line and comment the line after that
        # to run behind proxies
        # response = requests.post(url="https://auth.app.wiz.io/oauth/token",
        #                         headers=HEADERS_AUTH, data=auth_payload,
        #                         proxies=proxyDict, timeout=180)
        response = requests.post(url="https://auth.app.wiz.io/oauth/token",
                                headers=HEADERS_AUTH, data=auth_payload, timeout=180)

    except requests.exceptions.HTTPError as e:
        print(f"<p>Error authenticating to Wiz (4xx/5xx): {str(e)}</p>")
        return e

    except requests.exceptions.ConnectionError as e:
        print(f"<p>Network problem (DNS failure, refused connection, etc): {str(e)}</p>")
        return e

    except requests.exceptions.Timeout as e:
        print(f"<p>Request timed out: {str(e)}</p>")
        return e

    try:
        response_json = response.json()
        token = response_json.get('access_token')
        if not token:
            message = f"Could not retrieve token from Wiz: {response_json.get('message')}"
            raise ValueError(message)
    except ValueError as exception:
        message = f"Could not parse API response {exception}. Check Service Account details " \
                    "and variables"
        raise ValueError(message) from exception

    response_json_decoded = json.loads(
        base64.standard_b64decode(pad_base64(token.split(".")[1]))
    )

    response_json_decoded = json.loads(
        base64.standard_b64decode(pad_base64(token.split(".")[1]))
    )
    dc = response_json_decoded["dc"]

    return token, dc


def pad_base64(data):
    """Makes sure base64 data is padded"""
    missing_padding = len(data) % 4
    if missing_padding != 0:
        data += "=" * (4 - missing_padding)
    return data

def check_rotation_timeframe(service_account):

    expiry_date = datetime.datetime.strptime(service_account["expiresAt"],'%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=datetime.timezone.utc)

    print("Expires at: " + str(expiry_date))
    print("Expires in: " + str(abs((expiry_date) - datetime.datetime.now().replace(tzinfo=datetime.timezone.utc)).days) + " days time")

    if abs((expiry_date) - datetime.datetime.now().replace(tzinfo=datetime.timezone.utc)).days <= 2:
        print("This service account will expire soon, so it should be rotated.")
        return True
    elif service_account["enabled"] == False:
        print("This service account has already expired, so it should be rotated.")
        return True
    else:
        print("This service account is not within 2 days of expiry, so it should not be rotated.")
        return False


def rotate_wiz_client_secret(token, dc, expiry_days, service_account, maintain_expiry_date = False):

    HEADERS["Authorization"] = "Bearer " + token
    
    result = query_wiz_api(get_qry_rotate_sa_secret(), get_qryvars_rotate_sa_secret(wiz_client_id), dc)

    new_client_secret = result["data"]["rotateServiceAccountSecret"]["serviceAccount"]["clientSecret"]
    
    print("Client secret rotated")

    # with is like your try .. finally block in this case
    with open('/opt/wiz-sa-rotate/bin/wiz-auth.sh', 'r') as file:
        # read a list of lines into data
        data = file.readlines()

    # now change the 2nd line, note that you have to add a newline
    data[1] = "export WIZ_CLIENT_SECRET=" + new_client_secret

    # and write everything back
    with open('/opt/wiz-sa-rotate/bin/wiz-auth.sh', 'w') as file:
        file.writelines( data )

    if maintain_expiry_date == False:
        new_expiry_date = datetime.datetime.now() + datetime.timedelta(days=expiry_days)

        new_expiry_date = new_expiry_date.replace(hour=0, minute=0, second=0, microsecond=0, tzinfo=datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')

        updated_service_account = query_wiz_api(get_qry_patch_sa_expiry(),get_qryvars_patch_sa_expiry(wiz_client_id, new_expiry_date), dc)

        print("Service Account Expiry Updated to " + new_expiry_date)
    elif maintain_expiry_date == True:

        existing_expiry_date = service_account["expiresAt"]

        updated_service_account = query_wiz_api(get_qry_patch_sa_expiry(),get_qryvars_patch_sa_expiry(wiz_client_id, existing_expiry_date), dc)

        print("Service Account Expiry Date maintained to " + existing_expiry_date)


def main():
    """Main function"""

    validate_runtime_variables()

    print("Getting token.")
    token, dc = request_wiz_api_token(wiz_client_id, wiz_client_secret)
    HEADERS["Authorization"] = "Bearer " + token

    service_account = query_wiz_api(get_qry_service_account_info(), get_qryvars_service_account_info(wiz_client_id), dc)["data"]["serviceAccounts"]["nodes"][0]

    if force_rotate == True:
        rotate_wiz_client_secret(token, dc, 30, service_account, True)
    elif force_rotate == False:
        if check_rotation_timeframe(service_account) == True:
            rotate_wiz_client_secret(token, dc, 30, service_account, False)

if __name__ == '__main__':
    main()