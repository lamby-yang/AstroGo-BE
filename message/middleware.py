import jwt
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings

JWT_SECRET = settings.JWT_SECRET

class TokenAuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # 登录注册接口不需要验证token
        if request.path in ['/api/register_user/', '/api/login_user/']:
            return None

        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return JsonResponse({"error": "Missing token"}, status=401)

        parts = auth_header.split()
        if len(parts) != 2 or parts[0].lower() != 'bearer':
            return JsonResponse({"error": "Invalid Authorization header format"}, status=401)

        token = parts[1]

        try:
            # 解码并验证token
            payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
            # 把用户id放到request对象，方便后续使用
            request.user = {'id': payload.get('id')}
        except jwt.ExpiredSignatureError:
            return JsonResponse({"error": "Token expired"}, status=401)
        except jwt.InvalidTokenError:
            return JsonResponse({"error": "Invalid token"}, status=401)

        return None
