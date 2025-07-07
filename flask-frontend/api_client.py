"""
API client for making requests to the FastAPI backend
"""
import requests
from typing import Dict, Any, Optional, Tuple
from flask import current_app, session, flash, redirect, url_for, request
import logging
from functools import wraps
from requests.exceptions import RequestException, Timeout, ConnectionError

logger = logging.getLogger(__name__)


class APIError(Exception):
    """Custom exception for API errors"""
    def __init__(self, message: str, status_code: int = None, details: Dict = None):
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)


class APIClient:
    """Client for interacting with the FastAPI backend"""
    
    def __init__(self, base_url: str = None, timeout: int = None):
        self.base_url = base_url or current_app.config.get('API_BASE_URL', 'http://localhost:8000')
        self.timeout = timeout or current_app.config.get('API_TIMEOUT', 30)
        self.session = requests.Session()
        
    def _get_headers(self) -> Dict[str, str]:
        """Get request headers"""
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }
        
        # Authentication removed - no auth token needed
            
        return headers
    
    def _handle_response(self, response: requests.Response) -> Dict[str, Any]:
        """Handle API response and errors"""
        try:
            data = response.json()
        except ValueError:
            data = {'message': response.text or 'Invalid response format'}
        
        if response.status_code >= 400:
            error_message = data.get('detail', data.get('message', 'API request failed'))
            raise APIError(
                message=error_message,
                status_code=response.status_code,
                details=data
            )
        
        return data
    
    def _request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make a request to the API with error handling"""
        url = f"{self.base_url}{endpoint}"
        
        # Set default timeout if not provided
        kwargs.setdefault('timeout', self.timeout)
        
        # Add headers
        kwargs.setdefault('headers', {}).update(self._get_headers())
        
        try:
            logger.info(f"Making {method} request to {url}")
            response = self.session.request(method, url, **kwargs)
            return self._handle_response(response)
            
        except Timeout:
            logger.error(f"Request timeout for {method} {url}")
            raise APIError("Request timed out. Please try again.", status_code=408)
            
        except ConnectionError:
            logger.error(f"Connection error for {method} {url}")
            raise APIError("Unable to connect to the API server.", status_code=503)
            
        except RequestException as e:
            logger.error(f"Request failed for {method} {url}: {str(e)}")
            raise APIError(f"Request failed: {str(e)}", status_code=500)
    
    def get(self, endpoint: str, params: Dict = None) -> Dict[str, Any]:
        """Make GET request"""
        return self._request('GET', endpoint, params=params)
    
    def post(self, endpoint: str, data: Dict = None, json: Dict = None) -> Dict[str, Any]:
        """Make POST request"""
        return self._request('POST', endpoint, data=data, json=json)
    
    def put(self, endpoint: str, data: Dict = None, json: Dict = None) -> Dict[str, Any]:
        """Make PUT request"""
        return self._request('PUT', endpoint, data=data, json=json)
    
    def patch(self, endpoint: str, data: Dict = None, json: Dict = None) -> Dict[str, Any]:
        """Make PATCH request"""
        return self._request('PATCH', endpoint, data=data, json=json)
    
    def delete(self, endpoint: str) -> Dict[str, Any]:
        """Make DELETE request"""
        return self._request('DELETE', endpoint)
    
    # Authentication methods removed - no longer needed
    # def login, logout, check_auth methods removed


# Authentication decorator removed - no longer needed
# def api_auth_required removed - all routes are now accessible without auth


# Helper function to handle API errors in views
def handle_api_error(func):
    """Decorator to handle API errors in view functions"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except APIError as e:
            logger.error(f"API error in {func.__name__}: {e.message}")
            
            # Handle specific status codes
            if e.status_code == 401:
                flash('Authentication error occurred.', 'warning')
                # No login redirect - auth not required
            elif e.status_code == 403:
                flash('You do not have permission to perform this action.', 'error')
            elif e.status_code == 404:
                flash('The requested resource was not found.', 'error')
            elif e.status_code >= 500:
                flash('A server error occurred. Please try again later.', 'error')
            else:
                flash(e.message, 'error')
            
            # Redirect to referrer or home page
            return redirect(request.referrer or url_for('index'))
            
        except Exception as e:
            logger.error(f"Unexpected error in {func.__name__}: {str(e)}")
            flash('An unexpected error occurred.', 'error')
            return redirect(url_for('index'))
    
    return wrapper


# Singleton instance for easy access
_api_client = None

def get_api_client() -> APIClient:
    """Get or create API client instance"""
    global _api_client
    if _api_client is None:
        _api_client = APIClient()
    return _api_client