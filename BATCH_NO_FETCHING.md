# Batch No Fetching Feature

This feature allows you to fetch `batch_no` data from the external Production Management API at `http://10.0.0.242:5001`.

## Installation

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Method 1: Django Management Command (CLI)

Fetch batch_no using the command line:

```bash
python manage.py fetch_batch_no
```

**With custom API URL:**
```bash
python manage.py fetch_batch_no --api-url="http://10.0.0.242:5555/#/pm/work/"
```

**With custom timeout:**
```bash
python manage.py fetch_batch_no --timeout=15
```

**Output Example:**
```
Fetching batch_no from: http://10.0.0.242:5001/api/admin/WorkSectionInfo/Extend/GetMyWorkSectionInfo/
✓ Successfully fetched batch_no: ABC123

Full API Response:
{
  "batch_no": "ABC123"
}
```

### Method 2: Django View/API Endpoint

Access via HTTP endpoint (requires authentication):

**Endpoint:** `/hangerline/api/batch-no/`

**Example:**
```bash
curl http://localhost:8000/hangerline/api/batch-no/
```

**Response:**
```json
{
  "success": true,
  "batch_no": "ABC123",
  "data": {
    "batch_no": "ABC123"
  },
  "error": null
}
```

**With custom API URL:**
```bash
curl "http://localhost:8000/hangerline/api/batch-no/?api_url=http://10.0.0.242:5001/api/admin/WorkSectionInfo/Extend/GetMyWorkSectionInfo/"
```

### Method 3: Python Code

Use the helper function in your Python code:

```python
from hangerline.batch_api import fetch_batch_no

# Fetch batch_no
result = fetch_batch_no()

if result['success']:
    print(f"Batch No: {result['batch_no']}")
else:
    print(f"Error: {result['error']}")
```

**With custom parameters:**
```python
result = fetch_batch_no(
    api_url='http://10.0.0.242:5001/api/admin/WorkSectionInfo/Extend/GetMyWorkSectionInfo/',
    timeout=15
)
```

## Response Format

The `fetch_batch_no()` function returns a dictionary with the following structure:

```python
{
    'success': bool,      # True if batch_no was successfully fetched
    'batch_no': str,      # The batch number (or None if failed)
    'data': dict,         # Full API response data
    'error': str          # Error message (or None if successful)
}
```

## Error Handling

The function handles various error scenarios:

- **Connection Error**: API server is unreachable
- **Timeout**: Request takes too long
- **HTTP Error**: API returns error status code
- **JSON Decode Error**: Invalid JSON response
- **Missing Field**: `batch_no` field not found in response

## Configuration

### Default API URL
The default API URL is configured in both:
- `hangerline/management/commands/fetch_batch_no.py`
- `hangerline/batch_api.py`

To change the default, edit these files or pass the `--api-url` parameter.

### Timeout
Default timeout is 10 seconds. Adjust using:
- CLI: `--timeout` parameter
- Python: `timeout` argument
- View: No timeout parameter (uses default)

## Integration Examples

### Schedule Periodic Fetching

Use cron or Django Celery to periodically fetch batch_no:

**Cron example (every 5 minutes):**
```bash
*/5 * * * * cd /home/maqmalak/ETL/ssg-django && python manage.py fetch_batch_no >> /var/log/batch_fetch.log 2>&1
```

### Store in Database

Extend the functionality to save batch_no to a model:

```python
from hangerline.batch_api import fetch_batch_no
from hangerline.models import YourModel

result = fetch_batch_no()
if result['success']:
    YourModel.objects.create(
        batch_no=result['batch_no'],
        fetched_at=timezone.now()
    )
```

## Files Created

- `requirements.txt` - Added `requests` library
- `hangerline/batch_api.py` - Core fetching logic
- `hangerline/management/commands/fetch_batch_no.py` - CLI command
- `hangerline/views.py` - Added `get_batch_no` view
- `hangerline/urls.py` - Added API endpoint route
- `BATCH_NO_FETCHING.md` - This documentation

## Troubleshooting

### Connection Refused
```
Connection error: Unable to connect to http://10.0.0.242:5001/...
```
**Solution:** Ensure the API server is running and accessible from your network.

### Permission Denied (HTTP 403)
**Solution:** Check if authentication is required. The current implementation assumes no authentication.

### Field Not Found
```
batch_no field not found in response
```
**Solution:** Verify the API response structure matches `{"batch_no": "value"}`.
