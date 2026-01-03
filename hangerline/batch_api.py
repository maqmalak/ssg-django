# """
# Helper functions to fetch batch_no from external API
# """
# import requests
# import json
# from typing import Optional, Dict, Any


# def fetch_batch_no(
#     api_url: str = 'http://10.0.0.242:5555/#/pm/work/',
#     timeout: int = 10
# ) -> Dict[str, Any]:
#     """
#     Fetch batch_no from external production management API.
    
#     Args:
#         api_url: The API endpoint URL
#         timeout: Request timeout in seconds
        
#     Returns:
#         Dictionary with 'success', 'batch_no', 'data', and 'error' keys
#     """
#     result = {
#         'success': False,
#         'batch_no': None,
#         'data': None,
#         'error': None
#     }
    
#     try:
#         # Make GET request to the API
#         response = requests.get(api_url, timeout=timeout)
        
#         # Check if request was successful
#         response.raise_for_status()
        
#         # Parse JSON response
#         data = response.json()
#         result['data'] = data
        
#         # Extract batch_no
#         batch_no = data.get('batch_no')
        
#         if batch_no:
#             result['success'] = True
#             result['batch_no'] = batch_no
#         else:
#             result['error'] = 'batch_no field not found in response'
            
#     except requests.exceptions.Timeout:
#         result['error'] = f'Request timeout after {timeout} seconds'
        
#     except requests.exceptions.ConnectionError:
#         result['error'] = f'Connection error: Unable to connect to {api_url}'
        
#     except requests.exceptions.HTTPError as e:
#         result['error'] = f'HTTP error: {str(e)}'
        
#     except json.JSONDecodeError:
#         result['error'] = 'Invalid JSON response'
        
#     except Exception as e:
#         result['error'] = f'Unexpected error: {str(e)}'
    
#     return result
