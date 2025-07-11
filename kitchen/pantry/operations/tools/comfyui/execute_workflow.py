"""
ComfyUI Workflow Execution Operation

Single-purpose module for ComfyUI workflow execution operations.
"""

from typing import Dict, Any, Optional
from datetime import datetime
import requests
import json
import logging

logger = logging.getLogger(__name__)

class ComfyUIWorkflowExecutor:
    """ComfyUI workflow execution operation"""
    
    def __init__(self, base_url: str = "http://localhost:8188"):
        self.base_url = base_url.rstrip('/')
        self.api_url = f"{self.base_url}/api"
    
    def execute_workflow(self, workflow_data: Dict[str, Any], 
                        client_id: str = "kitchen_pantry") -> Dict[str, Any]:
        """Execute a ComfyUI workflow"""
        try:
            # Queue the workflow
            queue_payload = {
                "prompt": workflow_data,
                "client_id": client_id
            }
            
            response = requests.post(f"{self.api_url}/prompt", json=queue_payload)
            response.raise_for_status()
            
            result = response.json()
            prompt_id = result.get('prompt_id')
            
            if not prompt_id:
                return {
                    'success': False,
                    'error': 'No prompt ID returned',
                    'operation': 'execute_workflow'
                }
            
            # Monitor execution status
            execution_result = self._monitor_execution(prompt_id, client_id)
            
            return {
                'success': True,
                'operation': 'execute_workflow',
                'prompt_id': prompt_id,
                'client_id': client_id,
                'execution_result': execution_result,
                'timestamp': datetime.now().isoformat()
            }
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Error calling ComfyUI API: {str(e)}")
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
    
    def _monitor_execution(self, prompt_id: str, client_id: str) -> Dict[str, Any]:
        """Monitor workflow execution status"""
        try:
            # Get execution status
            response = requests.get(f"{self.api_url}/history/{prompt_id}")
            response.raise_for_status()
            
            history = response.json()
            
            return {
                'status': 'completed',
                'history': history,
                'outputs': history.get(prompt_id, {}).get('outputs', {})
            }
            
        except Exception as e:
            logger.error(f"Error monitoring execution: {str(e)}")
            return {
                'status': 'error',
                'error': str(e)
            } 