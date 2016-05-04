from auth_remember.utils import create_token_string
from auth_remember.utils import preset_cookie


def remember_user(request, user):
    """Set the remember-me flag on the user.

    A token is automatically generated and stored in the user's session.
    This token is set as a cookie value by the middleware.

    """
    token_string = create_token_string(user, None)
    preset_cookie(request, token_string)
