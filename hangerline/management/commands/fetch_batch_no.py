# """
# Django management command to fetch batch_no from external API.
# Usage: python manage.py fetch_batch_no
# """
# from django.core.management.base import BaseCommand
# import requests
# import json


# class Command(BaseCommand):
#     help = 'Fetch batch_no from external production management API'

#     def add_arguments(self, parser):
#         parser.add_argument(
#             '--api-url',
#             type=str,
#             default='http://10.0.0.242:5555/#/pm/work/',
#             help='API endpoint URL (default: http://10.0.0.242:5555/#/pm/work/)'
#         )
#         parser.add_argument(
#             '--timeout',
#             type=int,
#             default=10,
#             help='Request timeout in seconds (default: 10)'
#         )

#     def handle(self, *args, **options):
#         api_url = options['api_url']
#         timeout = options['timeout']

#         self.stdout.write(f"Fetching batch_no from: {api_url}")

#         try:
#             # Make GET request to the API
#             response = requests.get(api_url, timeout=timeout)
            
#             # Check if request was successful
#             response.raise_for_status()
            
#             # Parse JSON response
#             data = response.json()
            
#             # Extract batch_no
#             batch_no = data.get('batch_no')
            
#             if batch_no:
#                 self.stdout.write(self.style.SUCCESS(f"✓ Successfully fetched batch_no: {batch_no}"))
                
#                 # Pretty print the full response
#                 self.stdout.write("\nFull API Response:")
#                 self.stdout.write(json.dumps(data, indent=2))
                
#                 return batch_no
#             else:
#                 self.stdout.write(self.style.WARNING("⚠ batch_no field not found in response"))
#                 self.stdout.write(f"Response received: {json.dumps(data, indent=2)}")
                
#         except requests.exceptions.Timeout:
#             self.stdout.write(self.style.ERROR(f"✗ Request timeout after {timeout} seconds"))
            
#         except requests.exceptions.ConnectionError:
#             self.stdout.write(self.style.ERROR(f"✗ Connection error: Unable to connect to {api_url}"))
#             self.stdout.write("  Make sure the API server is running and accessible")
            
#         except requests.exceptions.HTTPError as e:
#             self.stdout.write(self.style.ERROR(f"✗ HTTP error: {e}"))
#             self.stdout.write(f"  Status code: {response.status_code}")
            
#         except json.JSONDecodeError:
#             self.stdout.write(self.style.ERROR("✗ Invalid JSON response"))
#             self.stdout.write(f"  Response text: {response.text[:200]}")
            
#         except Exception as e:
#             self.stdout.write(self.style.ERROR(f"✗ Unexpected error: {str(e)}"))
