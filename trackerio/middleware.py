from urllib.parse import parse_qs
from django.contrib.auth.models import AnonymousUser
from django.conf import settings

from channels.middleware import BaseMiddleware

from asgiref.sync import sync_to_async

from jwt import decode

class JWTAuthMiddleware(BaseMiddleware):
    """
    Custom middleware that takes JWT token from query string
    and authenticates the user for WebSocket connections.
    """

    async def __call__(self, scope, receive, send):
        query_string = scope.get("query_string", b"").decode()
        print("Query String:", query_string)
        query_params = parse_qs(query_string)
        print("Query Params:", query_params)
        token = query_params.get("token")[0]
        print("Token:", token)

        if token:
            try:
                payload = decode(
                    token,
                    settings.SECRET_KEY,
                    algorithms=["HS256"],
                )
                print("Payload:", payload)
                user = await sync_to_async(self.get_user)(payload)
                scope["user"] = user
            except Exception as e:
                print("Error decoding token or fetching user:", e)
                scope["user"] = AnonymousUser()
        else:
            scope["user"] = AnonymousUser()

        return await super().__call__(scope, receive, send)

    def get_user(self, payload):
        from django.contrib.auth import get_user_model

        User = get_user_model()
        try:
            user = User.objects.get(id=payload.get("user_id"))
            return user
        except User.DoesNotExist:
            return AnonymousUser()