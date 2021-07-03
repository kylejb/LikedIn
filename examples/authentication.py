from linkedin.api.linkedin_api import LinkedinAuthentication, LinkedinAPI, PERMISSIONS


if __name__ == "__main__":
    API_CLIENT_ID = "CLIENT_ID_VALUE"
    API_SECRET = "API_SECRET_VALUE"
    RETURN_URL = "http://localhost:8000/v1/callback"
    authentication = LinkedinAuthentication(
        API_CLIENT_ID, API_SECRET, RETURN_URL, PERMISSIONS.enums.values()
    )
    print(f"Click here: {authentication.authorization_url}")
    application = LinkedinAPI(authentication)
