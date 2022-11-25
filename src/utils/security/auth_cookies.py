from fastapi import Response

def add_authorization_cookie_to_response(
    response: Response,
    auth_cookie_type: str,
    cookie_key: str,
    cookie_value: str,
    cookie_expiry_duration_seconds: int | None
):
    # To be used in production (https) if frontend and backend have different url
    if auth_cookie_type == 'cross_site_secure':
        response.set_cookie(
            key=cookie_key,
            value=cookie_value,
            httponly=True,
            samesite='none',
            secure=True,
            expires=cookie_expiry_duration_seconds
        )

    # To be used in production (https) if frontend and backend have same url
    if auth_cookie_type == 'same_site_secure':
        response.set_cookie(
            key=cookie_key,
            value=cookie_value,
            httponly=True,
            samesite='strict',
            secure=True,
            expires=cookie_expiry_duration_seconds
        )

    # Used for E2E testing with docker, where backend and frontend docker services have different http (insecure) urls so need to be accessed via a proxy
    if auth_cookie_type == 'same_site_not_secure':
        response.set_cookie(
            key=cookie_key,
            value=cookie_value,
            httponly=True,
            samesite='strict', # samesite cannot be none for most browsers if secure=False
            secure=False,
            expires=cookie_expiry_duration_seconds
        )

    # Used for local development - use localhost and not 127.0.0.1
    if auth_cookie_type == 'localhost_development':
        response.set_cookie(
            key=cookie_key,
            value=cookie_value,
            httponly=True,
            # samesite='none', # 'strict' is not required when backend url is localhost for chrome
            secure=False,  # field can also be set to True as it is ignored by chrome if domain is localhost
            expires=cookie_expiry_duration_seconds
        )

