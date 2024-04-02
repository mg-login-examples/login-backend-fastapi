from starlette.staticfiles import Response, Scope, StaticFiles


class SPAStaticFiles(StaticFiles):
    async def get_response(self, path: str, scope: Scope) -> Response:
        # Try/Except needed as it doesn't work inside docker otherwise
        # 404 Response returned as an exception
        try:
            response = await super().get_response(path, scope)
        except Exception as error_response:
            if error_response.status_code == 404:
                response = await super().get_response(".", scope)
            else:
                raise error_response
        if response.status_code == 404:
            response = await super().get_response(".", scope)
        return response
