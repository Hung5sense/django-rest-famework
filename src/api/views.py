from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import AuthenticationFailed

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_fake_data(request):
    """
        Trả về dữ liệu nếu access token hợp lệ
    """
    try:
        user = request.user
        data = {
            "message": "Token hợp lệ",
            "data": [
                {"id": 1, "name": "Sản phẩm A", "price": 1000},
                {"id": 2, "name": "Sản phẩm B", "price": 2000},
            ]
        }
        return Response(data, status=200)
    except AuthenticationFailed: 
        refresh_token = request.COOKIES.get('refresh_token')  # Hoặc lấy từ body request
        
        if refresh_token:
            try:
                refresh = RefreshToken(refresh_token)
                new_access_token = str(refresh.access_token)
                return Response({"access_token": new_access_token}, status=200)
            except:
                return Response({"error": "Refresh token hết hạn hoặc không hợp lệ!"}, status=401)
        else:
            return Response({"error": "Không có refresh token, vui lòng đăng nhập lại!"}, status=401)