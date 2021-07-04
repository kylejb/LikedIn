from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse


def quick_api(api_key, secret_key, port=8000):
    """Authenticate with Linkedin API."""
    # auth = LinkedinAuthentication(
    #     api_key,
    #     secret_key,
    #     "http://localhost:8000/v1/callback",
    #     PERMISSIONS.enums.values(),
    # )

    # app = LinkedinAPI(authentication=auth)

    # print(f"Linkedin Auth URL: {auth.authorization_url}")
    # _wait_for_user_to_enter_browser(app, port)

    # return app
    ...


def _wait_for_user_to_enter_browser(app, port):
    class MyHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            p = self.path.split("?")
            if len(p) > 1:
                params = urlparse.parse_qs(p[1], True, True)
                app.authentication.authorization_code = params["code"][0]
                app.authentication.get_access_token()

    server_address = ("", port)
    httpd = HTTPServer(server_address, MyHandler)
    httpd.handle_request()
