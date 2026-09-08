import requests

from utils.config_reader import ConfigReader


class ApiClient:
    """
    Thin wrapper around `requests` used for two purposes in this framework:

    1. Standalone API tests (tests/api/) against a public REST API.
    2. Hybrid UI+API patterns — e.g. verifying backend state matches what the
       UI displays, or (on sites that support it) fetching an auth/session
       token via API instead of driving the login form for every single test.

    Note: tutorialsninja.com/demo (OpenCart) does not expose a public JSON
    login/cart API, so the hybrid verification methods below are written
    generically and are demonstrated end-to-end against jsonplaceholder
    instead. This mirrors real projects, where not every legacy app under
    test exposes clean APIs — the framework is built to use them when
    available and fall back to UI-only when it isn't.
    """

    def __init__(self, base_url: str = None):
        self.base_url = base_url or ConfigReader.get_api_base_url()
        self.session = requests.Session()

    def get(self, endpoint: str, params: dict = None):
        response = self.session.get(f"{self.base_url}{endpoint}", params=params, timeout=10)
        return response

    def post(self, endpoint: str, payload: dict = None):
        response = self.session.post(f"{self.base_url}{endpoint}", json=payload, timeout=10)
        return response

    def put(self, endpoint: str, payload: dict = None):
        response = self.session.put(f"{self.base_url}{endpoint}", json=payload, timeout=10)
        return response

    def delete(self, endpoint: str):
        response = self.session.delete(f"{self.base_url}{endpoint}", timeout=10)
        return response

    def inject_cookies_into_driver(self, driver, cookies: dict):
        """
        Example hybrid pattern: once you have a session/auth cookie from an
        API login call, add it to the Selenium driver's cookie jar so the
        browser is treated as already logged in — skipping repeated UI login.
        Requires the driver to have already navigated to the target domain
        at least once (cookies are domain-scoped).
        """
        for name, value in cookies.items():
            driver.add_cookie({"name": name, "value": value})
