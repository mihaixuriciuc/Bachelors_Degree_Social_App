import requests
import random
import string
from typing import Dict, Any, Optional
from apps.user.models import User
from apps.posts.models import Post

class APIClient:
    """Handles HTTP sessions, CSRF tokens, and IP spoofing."""
    def __init__(self, base_url: str, ip_address: Optional[str] = None):
        self.base_url = base_url
        self.session = requests.Session()
        self.ip_address = ip_address
        self._initialize_session()

    def _initialize_session(self) -> None:
        try:
            self.session.get(f"{self.base_url}/account/posts/")
        except requests.exceptions.RequestException:
            pass

    def _get_headers(self) -> Dict[str, str]:
        headers = {"Content-Type": "application/json"}
        if self.ip_address:
            headers["X-Forwarded-For"] = self.ip_address
        csrf_token = self.session.cookies.get("csrftoken")
        if csrf_token:
            headers["X-CSRFToken"] = csrf_token
        return headers

    def get(self, endpoint: str) -> requests.Response:
        return self.session.get(f"{self.base_url}{endpoint}", headers=self._get_headers())

    def post(self, endpoint: str, data: Dict[str, Any] = None) -> requests.Response:
        return self.session.post(f"{self.base_url}{endpoint}", json=data or {}, headers=self._get_headers())


class SocialAppBot:
    """Domain logic for automated user actions (both bots and simulated humans)."""
    def __init__(self, client: APIClient):
        self.client = client
        self.username: Optional[str] = None

    def sign_up(self, username: str, password: str) -> bool:
        payload = {"username": username, "email": f"{username}@test.com", "password": password, "confirm_password": password}
        res = self.client.post("/signUp/", payload)
        return res.status_code in (200, 201)

    def sign_in(self, username: str, password: str) -> requests.Response:
        res = self.client.post("/signIn/", {"username": username, "password": password})
        if res.status_code == 200:
            self.username = username
        return res

    # --- THIS WAS THE MISSING METHOD ---
    def create_post(self, title: str, content: str) -> requests.Response:
        return self.client.post("/account/posts/", {"title": title, "content": content})

    def comment_on_post(self, post_id: int, content: str) -> requests.Response:
        return self.client.post(f"/account/posts/{post_id}/comments/", {"content": content})

    def like_post(self, post_id: int) -> requests.Response:
        return self.client.post(f"/account/posts/{post_id}/likes/")

    def follow_user(self, target_username: str) -> requests.Response:
        return self.client.post(f"/users/{target_username}/follow/")


# --- SHARED HELPERS ---
def random_string(length: int = 6) -> str:
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

def force_activate(username: str) -> None:
    """Bypasses email verification for local testing."""
    User.objects.filter(username=username).update(is_active=True)

def get_target_post_id() -> int:
    """Fetches a real post ID from the DB to prevent 404 errors."""
    post = Post.objects.first()
    if not post:
        raise ValueError("No posts found in the database! Please create at least one post manually or via seeders.")
    return post.id