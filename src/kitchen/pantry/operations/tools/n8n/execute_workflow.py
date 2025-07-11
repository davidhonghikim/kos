"""
n8n Workflow Execution Operation

Single-purpose module for n8n workflow execution operations.
"""

from typing import Dict, Any, Optional
from datetime import datetime
import requests
import json
import logging

logger = logging.getLogger(__name__)

class N8NWorkflowExecutor:
    """n8n workflow execution operation"""
    
    def __init__(self, base_url: str = "http://localhost:5678", api_key: str = ""):
        self.base_url = base_url.rstrip('/')
        self.api_url = f"{self.base_url}/api/v1"
        self.api_key = api_key
        self.headers = {
            'Content-Type': 'application/json',
            'X-N8N-API-KEY': api_key
        } if api_key else {'Content-Type': 'application/json'}
    
    def execute_workflow(self, workflow_id: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Execute an n8n workflow"""
        try:
            payload = {
                "workflowId": workflow_id
            }
            
            if data:
                payload["data"] = data
            
            response = requests.post(f"{self.api_url}/workflows/{workflow_id}/trigger", 
                                   json=payload, headers=self.headers)
            response.raise_for_status()
            
            result = response.json()
            
            return {
                'success': True,
                'operation': 'execute_workflow',
                'workflow_id': workflow_id,
                'execution_id': result.get('executionId'),
                'status': result.get('status', 'running'),
                'data': data,
                'timestamp': datetime.now().isoformat()
            }
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Error calling n8n API: {str(e)}")
            return {
                'success': False,
                'error': f"API request failed: {str(e)}",
                'operation': 'execute_workflow'
            }
        except Exception as e:
            logger.error(f"Error executing workflow: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'operation': 'execute_workflow'
            }
    
    def get_workflows(self) -> Dict[str, Any]:
        """Get list of available workflows"""
        try:
            response = requests.get(f"{self.api_url}/workflows", headers=self.headers)
            response.raise_for_status()
            
            workflows = response.json()
            
            return {
                'success': True,
                'operation': 'get_workflows',
                'workflows': workflows.get('data', []),
                'total': len(workflows.get('data', [])),
                'timestamp': datetime.now().isoformat()
            }
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Error calling n8n API: {str(e)}")
            return {
                'success': False,
                'error': f"API request failed: {str(e)}",
                'operation': 'get_workflows'
            }
        except Exception as e:
            logger.error(f"Error getting workflows: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'operation': 'get_workflows'
            } 