"""
API Views for Production Dashboard
Provides REST endpoints for React frontend to consume dashboard data
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .dashboard_utils import get_dashboard_data, convert_decimals


class LoginView(APIView):
    """Login endpoint to get JWT tokens"""
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({
                'error': 'Username and password are required'
            }, status=400)

        user = authenticate(username=username, password=password)

        if user is None:
            return Response({
                'error': 'Invalid credentials'
            }, status=401)

        # Generate tokens
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        return Response({
            'access': access_token,
            'refresh': str(refresh),
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'is_staff': user.is_staff,
                'is_superuser': user.is_superuser,
            }
        })


class DashboardAPIView(APIView):
    """API endpoint for dashboard data"""

    def get(self, request):
        """Get filtered dashboard data"""
        # Get filter parameters
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        line_filter = request.query_params.get('line')
        shift_filter = request.query_params.get('shift')

        try:
            # Get dashboard data
            dashboard_data = get_dashboard_data(start_date, end_date, line_filter, shift_filter)

            # Return the data
            return Response(dashboard_data)

        except Exception as e:
            return Response({
                'error': f'Dashboard data error: {str(e)}'
            }, status=500)


class UserView(APIView):
    """Get current user information"""

    def get(self, request):
        user = request.user
        return Response({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'is_staff': user.is_staff,
            'is_superuser': user.is_superuser,
        })
