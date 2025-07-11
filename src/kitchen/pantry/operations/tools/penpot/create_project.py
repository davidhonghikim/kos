"""
Penpot Project Creation Operation

Single-purpose module for Penpot project creation operations.
"""

from typing import Dict, Any, Optional
from datetime import datetime
import requests
import json
import logging

logger = logging.getLogger(__name__)

class PenpotProjectCreator:
    """Penpot project creation operation"""
    
    def __init__(self, base_url: str = "http://localhost:9001", api_token: str = ""):
        self.base_url = base_url.rstrip('/')
        self.api_url = f"{self.base_url}/api"
        self.api_token = api_token
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Token {api_token}'
        } if api_token else {'Content-Type': 'application/json'}
    
    def create_project(self, name: str, description: str = "", 
                      team_id: Optional[str] = None) -> Dict[str, Any]:
        """Create a new Penpot project"""
        try:
            payload = {
                "name": name,
                "description": description
            }
            
            if team_id:
                payload["team-id"] = team_id
            
            response = requests.post(f"{self.api_url}/projects", 
                                   json=payload, headers=self.headers)
            response.raise_for_status()
            
            result = response.json()
            
            return {
                'success': True,
                'operation': 'create_project',
                'project_id': result.get('id'),
                'project_name': name,
                'description': description,
                'team_id': team_id,
                'created_at': result.get('created-at'),
                'timestamp': datetime.now().isoformat()
            }
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Error calling Penpot API: {str(e)}")
            return {
                'success': False,
                'error': f"API request failed: {str(e)}",
                'operation': 'create_project'
            }
        except Exception as e:
            logger.error(f"Error creating project: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'operation': 'create_project'
            }
    
    def get_projects(self) -> Dict[str, Any]:
        """Get list of available projects"""
        try:
            response = requests.get(f"{self.api_url}/projects", headers=self.headers)
            response.raise_for_status()
            
            projects = response.json()
            
            return {
                'success': True,
                'operation': 'get_projects',
                'projects': projects,
                'total': len(projects),
                'timestamp': datetime.now().isoformat()
            }
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Error calling Penpot API: {str(e)}")
            return {
                'success': False,
                'error': f"API request failed: {str(e)}",
                'operation': 'get_projects'
            }
        except Exception as e:
            logger.error(f"Error getting projects: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'operation': 'get_projects'
            } 