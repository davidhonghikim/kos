"""
Automatic1111 Image-to-Image Operation

Single-purpose module for Automatic1111 img2img operations.
"""

from typing import Dict, Any, Optional
from datetime import datetime
import requests
import base64
import json
import logging

logger = logging.getLogger(__name__)

class Automatic1111Img2Img:
    """Automatic1111 image-to-image operation"""
    
    def __init__(self, base_url: str = "http://localhost:7860"):
        self.base_url = base_url.rstrip('/')
        self.api_url = f"{self.base_url}/sdapi/v1"
    
    def transform_image(self, init_image: bytes, prompt: str, negative_prompt: str = "",
                       denoising_strength: float = 0.75, steps: int = 20, 
                       cfg_scale: float = 7.0, sampler_name: str = "Euler a", 
                       seed: int = -1) -> Dict[str, Any]:
        """Transform image using text prompt and Automatic1111"""
        try:
            # Encode image to base64
            init_image_b64 = base64.b64encode(init_image).decode('utf-8')
            
            payload = {
                "init_images": [init_image_b64],
                "prompt": prompt,
                "negative_prompt": negative_prompt,
                "denoising_strength": denoising_strength,
                "steps": steps,
                "cfg_scale": cfg_scale,
                "sampler_name": sampler_name,
                "seed": seed,
                "batch_size": 1
            }
            
            response = requests.post(f"{self.api_url}/img2img", json=payload)
            response.raise_for_status()
            
            result = response.json()
            
            # Decode base64 image data
            if 'images' in result and len(result['images']) > 0:
                image_data = base64.b64decode(result['images'][0])
                
                return {
                    'success': True,
                    'operation': 'img2img',
                    'prompt': prompt,
                    'negative_prompt': negative_prompt,
                    'parameters': {
                        'denoising_strength': denoising_strength,
                        'steps': steps,
                        'cfg_scale': cfg_scale,
                        'sampler_name': sampler_name,
                        'seed': result.get('info', {}).get('seed', seed)
                    },
                    'image_data': image_data,
                    'image_format': 'png',
                    'timestamp': datetime.now().isoformat()
                }
            else:
                return {
                    'success': False,
                    'error': 'No image generated',
                    'operation': 'img2img'
                }
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Error calling Automatic1111 API: {str(e)}")
            return {
                'success': False,
                'error': f"API request failed: {str(e)}",
                'operation': 'img2img'
            }
        except Exception as e:
            logger.error(f"Error transforming image: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'operation': 'img2img'
            } 