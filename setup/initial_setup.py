ACCESS_TOKEN_FILENAME = "app/tokens/access_token.txt"
API_SECRET = "LINKEDIN_API_SECRET"
API_CLIENT = "LINKEDIN_API_CLIENT_ID"

if __name__ == "__main__":
    import os
    import sys

    import pawl
    from dotenv import load_dotenv
    from pawl.utils.get_access_token import get_access_token

    load_dotenv()

    _client_id = os.environ[API_CLIENT]
    _client_secret = os.environ[API_SECRET]

    linkedin = pawl.Linkedin(
        client_id=_client_id,
        client_secret=_client_secret,
        redirect_uri="http://localhost:8000",
    )

    access_token = get_access_token(linkedin)
    with open(ACCESS_TOKEN_FILENAME, "w") as fp:
        fp.write(access_token)
    print("Setup complete.")
    sys.exit()
