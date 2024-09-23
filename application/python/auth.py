import msal

CLIENT_ID = "4dcd6afc-b59f-4215-95f7-4b6c2c2d83e1"
TENANT_ID = "2080ad1c-4ca1-4961-98ba-51996277c9ba"
CLIENT_SECRET = "fbc165d4-1a2f-44c2-9522-62fb7ff5c7cc"
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
REDIRECT_URI = "http://localhost:5000/callback"
SCOPE = ["Mail.ReadWrite", "Mail.Send"]


def get_access_token():
    app = msal.ConfidentialClientApplication(
        CLIENT_ID, authority=AUTHORITY, client_credentials=CLIENT_SECRET
    )

    # get access token (interactive for first time use then use cache)
    result = app.acquire_token_interactive(scopes=SCOPE, redirect_uri=REDIRECT_URI)
    if "access_token" in result:
        return result["access_token"]
    else:
        raise Exception("could not authenticate: ", result.get("error_description"))


def get_cached_access_token():
    app = msal.ConfidentialClientApplication(
        CLIENT_ID, authority=AUTHORITY, client_credentials=CLIENT_SECRET
    )
    accounts = app.get_accounts()
    if accounts:
        result = app.acquire_token_silent(SCOPE, account=accounts[0])
        if result:
            return result["access_token"]
    return get_access_token()
