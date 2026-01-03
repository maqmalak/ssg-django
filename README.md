# SSG Django Production Dashboard

A comprehensive Django-based production analytics dashboard for manufacturing operations, featuring real-time monitoring, line-wise performance tracking, and detailed visual analytics.

## Features

### 📊 Dashboard Components

- **Top Filters**: Date range selection, production line selector (Line-21 to Line-32), and shift filtering (Day/Night)
- **11 Summary Cards**: Total Loading, Offloading, WIP, Defects, Target, Variance, Achievement %, Breakdown Time, Efficiency, and Active Lines
- **4 Line-wise Performance Cards**: Loading by line, Offloading by line with efficiency, WIP tracking, and Target vs Achievement with variance indicators
- **5 Interactive Charts**:
  - Stacked vertical bar chart (Loading + Offloading + WIP per line)
  - Horizontal shift-wise bar chart (Day/Night production)
  - Production distribution pie chart
  - Breakdown by Category pie chart
  - Breakdown by Line pie chart

## Tech Stack

- **Backend**: Django 4.2
- **Database**: PostgreSQL
- **Frontend**: Chart.js for visualizations
- **Server**: Gunicorn (production)
- **Containerization**: Docker & Docker Compose

## Installation

### Using Docker (Recommended)

1. Clone the repository:
```bash
git clone https://github.com/maqmalak/ssg-django.git
cd ssg-django
```

2. Build and run with Docker Compose:
```bash
docker-compose up --build
```

3. Access the dashboard at `http://localhost:8008`

### Manual Installation

1. Clone the repository:
```bash
git clone https://github.com/maqmalak/ssg-django.git
cd ssg-django
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables in `ssg_project/settings.py` or create a `.env` file:
```
DB_NAME=ssg
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
```

5. Run migrations:
```bash
python manage.py migrate
```

6. Create a superuser:
```bash
python manage.py createsuperuser
```

7. Run the development server:
```bash
python manage.py runserver
```

8. Access the dashboard at `http://localhost:8000/hangerline/dashboard/`

## Project Structure

```
ssg-django/
├── hangerline/                 # Main app
│   ├── management/            # Custom management commands
│   │   └── commands/
│   │       ├── fetch_batch_no.py
│   │       ├── import_colors.py
│   │       ├── import_sizes.py
│   │       └── import_styles.py
│   ├── migrations/            # Database migrations
│   ├── templates/             # HTML templates
│   │   └── admin/
│   │       └── hangerline/
│   │           ├── dashboard.html
│   │           └── breakdown/
│   ├── admin.py              # Django admin configuration
│   ├── models.py             # Database models
│   ├── views.py              # View functions and API endpoints
│   └── urls.py               # URL routing
├── ssg_project/              # Project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── templates/                # Global templates
├── docker-compose.yml        # Docker Compose configuration
├── Dockerfile                # Docker image definition
├── requirements.txt          # Python dependencies
├── requirements-frozen.txt   # Frozen dependencies with versions
└── manage.py                 # Django management script
```

## API Endpoints

- `/hangerline/dashboard/` - Main production dashboard
- `/hangerline/api/chart/shift/` - Shift-wise data
- `/hangerline/api/chart/source/` - Line-wise stacked data
- `/hangerline/api/chart/production/` - Production distribution
- `/hangerline/api/chart/line-loading/` - Line loading summary
- `/hangerline/api/chart/line-offloading/` - Line offloading summary

## Database Models

- **OperatorDailyPerformance**: Daily performance records per operator
- **LineTarget**: Production targets per line
- **LineTargetDetail**: Detailed target information
- **Style**, **Color**, **Size**: Product configuration
- **LoadingInformation**: Loading operation details

## Management Commands

```bash
# Import data
python manage.py import_colors
python manage.py import_sizes
python manage.py import_styles
python manage.py fetch_batch_no
```

## Docker Configuration

The project includes:
- **Dockerfile**: Python 3.10-slim based image
- **docker-compose.yml**: Service orchestration with PostgreSQL connection
- **.dockerignore**: Optimized build context

## Environment Variables

Configure these in `docker-compose.yml` or your environment:

- `DB_NAME`: Database name (default: ssg)
- `DB_USER`: Database user (default: postgres)
- `DB_PASSWORD`: Database password
- `DB_HOST`: Database host (default: 172.16.7.6)
- `DB_PORT`: Database port (default: 5432)

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is proprietary software developed for SSG manufacturing operations.

## Support

For issues and questions, please contact the development team.

## Acknowledgments

- Django Framework
- Chart.js for beautiful visualizations
- PostgreSQL database
