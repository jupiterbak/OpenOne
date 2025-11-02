# coding: utf-8

"""
OAuth2 Authentication Handler for Alteryx Cloud API
"""

import time
import logging
from typing import Optional
import requests
from urllib3.exceptions import HTTPError
import base64
import urllib.parse
import urllib.request
import os
import json

class OAuth2Handler:
    """Handles OAuth2 authentication with refresh token support."""
    
    def __init__(self, 
                 configuration_file_path: str="~/.aacp/config.json",
                 expires_in: int = 300):
        """
        Initialize OAuth2 handler.
        
        :param client_id: OAuth2 client ID
        :param access_token: OAuth2 access token
        :param refresh_token: OAuth2 refresh token
        :param refresh_endpoint: OAuth2 refresh endpoint
        :param expires_in: OAuth2 token expiration time in seconds
        """
        # Expand user path and store
        self.configuration_file_path = os.path.expanduser(configuration_file_path)

        # if the configuration file path is not a valid file, raise an error
        if not os.path.isfile(self.configuration_file_path):
            raise FileNotFoundError(f"Configuration file not found at {self.configuration_file_path}")

        # Load the configuration file
        with open(self.configuration_file_path, "r") as f:
            self.configuration = json.load(f)

        # Use .get to avoid KeyError if a key is missing from the credentials file
        self.client_id = self.configuration.get("client_id")
        self.access_token = self.configuration.get("access_token")
        self.refresh_token = self.configuration.get("refresh_token")
        self.refresh_endpoint = self.configuration.get("refresh_endpoint")
        self.token_expires_at = self.configuration.get("token_expires_at", time.time() - 300)
        self.logger = logging.getLogger(__name__)
    
    def set_tokens(self, access_token: str, refresh_token: str, expires_in: int = 3600):
        """
        Set OAuth2 tokens.
        
        :param access_token: Access token
        :param refresh_token: Refresh token
        :param expires_in: Token expiration time in seconds
        """
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.token_expires_at = time.time() + expires_in - 300

        # Update the configuration file with the new tokens
        self.configuration["access_token"] = access_token
        self.configuration["refresh_token"] = refresh_token
        self.configuration["token_expires_at"] = self.token_expires_at
        with open(self.configuration_file_path, "w") as f:
            json.dump(self.configuration, f)

        self.logger.debug(f"Tokens set. Expires at: {self.token_expires_at}")
    
    def is_token_expired(self) -> bool:
        """
        Check if the current access token is expired.
        
        :return: True if token is expired or will expire soon
        """
        if not self.access_token or not self.token_expires_at:
            return True
        
        return time.time() >= self.token_expires_at
    
    def refresh_access_token(self) -> bool:
        """
        Refresh the access token using the refresh token.
        
        :return: True if refresh was successful
        """
        if not self.refresh_token:
            self.logger.error("No refresh token available")
            return False
        
        try:
            
            # Get the second part of the access token, which is its payload
            payload = self.access_token.split('.')[1]

            # Decode the base64-encoded access token
            info = json.loads(base64.b64decode(f'{payload}===='))

            # Create the body for the refresh request
            body = {
                'grant_type': 'refresh_token',
                'refresh_token': self.refresh_token,
                'client_id': info['client_id'],
            }

            # URL encode the body for the refresh request
            encoded_body = urllib.parse.urlencode(body).encode()

            # Make the refresh request
            request = urllib.request.Request(f"{info['iss']}/token", data=encoded_body, method='POST')
            with urllib.request.urlopen(request) as response:
                new_creds = json.load(response)

            # Overwrite the contents of the credneitals file with the new access and refresh tokens
            self.set_tokens(new_creds['access_token'], new_creds['refresh_token'], new_creds['expires_in'])
            self.logger.debug("Access token refreshed successfully")
            return True 

            # data = {
            #     'grant_type': 'refresh_token',
            #     'refresh_token': self.refresh_token,
            #     'client_id': self.client_id,
            # }
            
            # response = self.session.post(self.refresh_endpoint, data=data)
            # response.raise_for_status()
            
            # token_data = response.json()
            
            # self.access_token = token_data['access_token']
            # if 'refresh_token' in token_data:
            #     self.refresh_token = token_data['refresh_token']
            
            # expires_in = token_data.get('expires_in', 3600)
            # self.token_expires_at = time.time() + expires_in - 300  # 5 minute buffer
            
            # self.logger.debug("Access token refreshed successfully")
            # return True
            
        except (requests.RequestException, HTTPError) as e:
            self.logger.error(f"Failed to refresh access token: {e}")
            return False
        except KeyError as e:
            self.logger.error(f"Invalid token response format: {e}")
            return False
        except Exception as e:
            self.logger.error(f"An error occurred: {e}")
            return False
    
    def get_access_token(self) -> Optional[str]:
        """
        Get a valid access token, refreshing if necessary.
        
        :return: Valid access token or None if refresh failed
        """
        if self.is_token_expired():
            if not self.refresh_access_token():
                return None
        
        return self.access_token
    
    def get_refresh_token(self) -> Optional[str]:
        """
        Get a valid refresh token, refreshing if necessary.
        
        :return: Valid access token or None if refresh failed
        """
        if self.is_token_expired():
            if not self.refresh_access_token():
                return None
        
        return self.refresh_token
    
    def get_authorization_header(self) -> Optional[str]:
        """
        Get the Authorization header value.
        
        :return: Authorization header value or None if no valid token
        """
        token = self.get_access_token()
        if token:
            return f"Bearer {token}"
        return None
    
    def clear_tokens(self):
        """Clear all stored tokens."""
        self.access_token = None
        self.refresh_token = None
        self.token_expires_at = None
        self.logger.debug("Tokens cleared") 