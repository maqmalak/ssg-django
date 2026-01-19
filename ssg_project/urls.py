"""
URL configuration for ssg_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render
from django.conf import settings
from django.conf.urls.static import static
from datetime import date
from rest_framework_simplejwt.views import TokenRefreshView
from hangerline.api_views import LoginView, DashboardAPIView, UserView
from hangerline.dashboard_utils import get_dashboard_data, convert_decimals

def dashboard_view(request):
    """React dashboard view with real data"""
    from django.db.models import Sum, Count, Avg, Q, F
    from django.db.models.functions import ExtractMonth, ExtractYear
    from datetime import datetime, date
    from django.http import JsonResponse
    import json
    from hangerline.models import OperatorDailyPerformance, Breakdown, LineTarget
    import logging

    logger = logging.getLogger(__name__)

    # Check if this is an AJAX request for filtered data
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return get_dashboard_data_api(request)

    try:
        # Get date filters from request (for initial page load)
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        line_filter = request.GET.get('line')
        shift_filter = request.GET.get('shift')

        logger.info(f"Dashboard view called with params: start_date={start_date}, end_date={end_date}, line={line_filter}, shift={shift_filter}")

        # Default to current month if no dates provided
        if not start_date or not end_date:
            today = date.today()
            start_date = date(today.year, today.month, 1)
            end_date = date(today.year, today.month + 1, 1) if today.month < 12 else date(today.year + 1, 1, 1)
            logger.info(f"Using default date range: {start_date} to {end_date}")
        else:
            start_date = date.fromisoformat(start_date)
            end_date = date.fromisoformat(end_date)
            logger.info(f"Using provided date range: {start_date} to {end_date}")

        # Get data for initial page load
        logger.info("Calling get_dashboard_data...")
        dashboard_data = get_dashboard_data(start_date, end_date, line_filter, shift_filter)
        logger.info(f"Dashboard data retrieved, keys: {list(dashboard_data.keys()) if dashboard_data else 'None'}")

        # Pass data to template as JSON
        from django.http import HttpResponse
        import os

        # Read the raw HTML file
        template_path = os.path.join(settings.BASE_DIR, 'hangerline', 'templates', 'admin', 'hangerline', 'dashboard.html')
        logger.info(f"Looking for template at: {template_path}")

        if not os.path.exists(template_path):
            logger.error(f"Template file does not exist: {template_path}")
            return HttpResponse(f"Dashboard template not found at {template_path}", status=404)

        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                html_content = f.read()

            logger.info(f"Template file read successfully, length: {len(html_content)}")

            # Inject data into the HTML by adding a script tag
            dashboard_data_json = json.dumps(dashboard_data, default=str)
            data_script = f'<script>window.data = {dashboard_data_json};</script>'

            # Insert the data script before the closing </head> tag
            if '</head>' in html_content:
                html_content = html_content.replace('</head>', f'{data_script}</head>')
                logger.info("Data script injected successfully")
            else:
                logger.warning("Could not find </head> tag in template, appending data script at end")
                html_content += data_script

            logger.info("Dashboard view completed successfully")
            return HttpResponse(html_content, content_type='text/html')

        except FileNotFoundError as e:
            logger.error(f"FileNotFoundError reading template: {e}")
            return HttpResponse(f"Dashboard template not found: {e}", status=404)
        except json.JSONEncodeError as e:
            logger.error(f"JSON encoding error: {e}")
            return HttpResponse(f"Dashboard data serialization error: {e}", status=500)
        except Exception as e:
            logger.error(f"Unexpected error in dashboard_view: {e}", exc_info=True)
            return HttpResponse(f"Dashboard error: {str(e)}", status=500)

    except Exception as e:
        logger.error(f"Unexpected error in dashboard_view outer try: {e}", exc_info=True)
        return HttpResponse(f"Dashboard initialization error: {str(e)}", status=500)

def get_dashboard_data_api(request):
    """API endpoint for filtered dashboard data"""
    from django.http import JsonResponse
    from datetime import date
    import logging

    logger = logging.getLogger(__name__)

    try:
        # Get date filters from request
        start_date_param = request.GET.get('start_date')
        end_date_param = request.GET.get('end_date')
        line_filter = request.GET.get('line')
        shift_filter = request.GET.get('shift')

        logger.info(f"API Request - Raw params: start_date={start_date_param}, end_date={end_date_param}, line={line_filter}, shift={shift_filter}")

        # Parse dates - if no dates provided, don't filter by date (show all data)
        start_date = None
        end_date = None

        if start_date_param and end_date_param:
            try:
                start_date = date.fromisoformat(start_date_param)
                end_date = date.fromisoformat(end_date_param)
                logger.info(f"Filtering by date range: {start_date} to {end_date}")
            except ValueError as e:
                logger.error(f"Invalid date format: start_date={start_date_param}, end_date={end_date_param}, error: {e}")
                return JsonResponse({'error': f'Invalid date format: {e}'}, status=400)
        else:
            logger.info("No date filters provided - showing all available data")

        # Get filtered data
        logger.info(f"Calling get_dashboard_data with: start={start_date}, end={end_date}, line={line_filter}, shift={shift_filter}")
        dashboard_data = get_dashboard_data(start_date, end_date, line_filter, shift_filter)

        logger.info(f"Dashboard data keys: {list(dashboard_data.keys()) if dashboard_data else 'None'}")
        if dashboard_data and 'summary' in dashboard_data:
            logger.info(f"Returning dashboard data with summary: {dashboard_data['summary']}")

        return JsonResponse(dashboard_data)

    except Exception as e:
        logger.error(f"API Error: {str(e)}", exc_info=True)
        import traceback
        logger.error(f"Full traceback: {traceback.format_exc()}")
        return JsonResponse({
            'error': str(e),
            'traceback': traceback.format_exc()
        }, status=500)


def production_dashboard_view(request):
    """Django production dashboard view"""
    from hangerline.views import django_dashboard
    return django_dashboard(request)

def breakdown_dashboard_view(request):
    """Original breakdown dashboard view"""
    from hangerline.views import breakdown_dashboard
    return breakdown_dashboard(request)

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # API endpoints
    path('api/login/', LoginView.as_view(), name='api_login'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/dashboard/', DashboardAPIView.as_view(), name='api_dashboard'),
    path('api/user/', UserView.as_view(), name='api_user'),

    # App URLs
    path('hangerline/', include('hangerline.urls')),

    # Dashboard views
    path('dashboard/', dashboard_view, name='main_dashboard'),  # React dashboard (main)
    path('production-dashboard/', production_dashboard_view, name='production_dashboard'),  # Original Django dashboard
    path('breakdown-dashboard/', breakdown_dashboard_view, name='breakdown_dashboard'),  # Original breakdown dashboard
] + static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
