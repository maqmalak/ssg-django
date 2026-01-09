# Django REST Framework API Setup

## Overview

This Django project now includes Django REST Framework (DRF) with JWT authentication, providing proper API endpoints for the React frontend to consume dashboard data.

## Architecture

- **`/home/maqmalak/ETL/ssg-django/`** - Django backend with REST API
- **`/home/maqmalak/ETL/hangerline/`** - React frontend (separate project)

## Installed Packages

```txt
djangorestframework>=3.14.0          # REST Framework core
django-cors-headers>=4.0.0           # CORS handling for React
djangorestframework-simplejwt>=5.2.0 # JWT authentication
```

## API Endpoints

### Authentication
- `POST /api/login/` - Login with username/password, returns JWT tokens
- `POST /api/token/refresh/` - Refresh access token
- `GET /api/user/` - Get current user information

### Dashboard Data
- `GET /api/dashboard/` - Get filtered dashboard data
  - Query parameters:
    - `start_date` (YYYY-MM-DD)
    - `end_date` (YYYY-MM-DD)
    - `line` (All or specific line)
    - `shift` (All, Day, or Night)

## Configuration

### Settings (ssg_project/settings.py)

```python
# Installed Apps
INSTALLED_APPS = [
    # ... existing apps
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
]

# Middleware
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # Must be first
    # ... other middleware
]

# CORS Settings
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",  # React dev server
    "http://127.0.0.1:3000",
    "http://localhost:3001",
    "http://127.0.0.1:3001",
]

CORS_ALLOW_CREDENTIALS = True

# REST Framework Settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 100,
}

# JWT Settings
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'SIGNING_KEY': SECRET_KEY,
    # ... other JWT settings
}
```

## API Views

### LoginView (hangerline/api_views.py)
- Handles user authentication
- Returns JWT access and refresh tokens
- User information included in response

### DashboardAPIView (hangerline/api_views.py)
- Provides filtered dashboard data
- Uses existing `get_dashboard_data()` function
- Supports date, line, and shift filtering

### UserView (hangerline/api_views.py)
- Returns current authenticated user information

## React Integration

### Authentication Flow
```javascript
// Login
const response = await fetch('/api/login/', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ username, password })
});
const { access, refresh } = await response.json();

// Use token in subsequent requests
const dashboardResponse = await fetch('/api/dashboard/?start_date=2024-01-01&end_date=2024-01-31', {
  headers: {
    'Authorization': `Bearer ${access}`,
    'Content-Type': 'application/json'
  }
});
```

### Dashboard Data Structure
```javascript
{
  summary: { /* KPI metrics */ },
  summaryCards: [ /* Card data */ ],
  lineComparisonRows: [ /* Line performance */ ],
  dateWiseEfficiency: [ /* Date-wise data */ ],
  pieCharts: {
    productionDistribution: [/* Chart data */],
    defectBreakdown: [/* Chart data */],
    linePerformance: [/* Chart data */],
    shiftDistribution: [/* Chart data */]
  },
  lineTrendData: [ /* 30-day trend */ ],
  defectAnalysis: { /* Defect details */ }
}
```

## Security Features

- **JWT Authentication** - Token-based auth with refresh capability
- **CORS Protection** - Configured for React frontend origins
- **Permission Classes** - API endpoints require authentication
- **Session Authentication** - Fallback to Django sessions

## Testing API Endpoints

```bash
# Test login
curl -X POST http://localhost:8001/api/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "password"}'

# Test dashboard data
curl -H "Authorization: Bearer <token>" \
  "http://localhost:8001/api/dashboard/?start_date=2024-01-01&end_date=2024-01-31"
```

## Migration to React Frontend

1. **Install Axios/Fetch** for API calls in React
2. **Implement authentication** with JWT tokens
3. **Replace mock data** with API calls to `/api/dashboard/`
4. **Add loading states** and error handling
5. **Implement token refresh** logic

## File Structure

```
ssg-django/
├── hangerline/
│   ├── api_views.py        # REST API views
│   ├── dashboard_utils.py  # Shared dashboard functions
│   ├── views.py           # Original Django views
│   └── urls.py            # App URLs
├── ssg_project/
│   ├── settings.py        # DRF configuration
│   └── urls.py            # API URL patterns
└── requirements.txt       # Updated with DRF packages
```

## Next Steps for React Integration

1. **Set up React project** in `/home/maqmalak/ETL/hangerline/`
2. **Implement JWT authentication** flow
3. **Create API service** layer for dashboard data
4. **Replace inline dashboard** with API-driven components
5. **Add loading states** and error boundaries

The Django backend is now fully equipped to serve the React frontend with secure, authenticated API endpoints!
