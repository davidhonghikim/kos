"""
Video Trim Operation

Single-purpose module for trimming videos.
"""

from moviepy import VideoFileClip
from pathlib import Path
from typing import Dict, Any
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class VideoTrimmer:
    """Trim video operation"""
    
    def trim(self, video_path: str, start_time: float, end_time: float, output_path: str) -> Dict[str, Any]:
        try:
            video_path = Path(video_path)
            output_path = Path(output_path)
            if not video_path.exists():
                return {
                    'success': False,
                    'error': f'Video not found: {video_path}',
                    'operation': 'trim_video'
                }
            with VideoFileClip(str(video_path)) as clip:
                trimmed = clip.subclip(start_time, end_time)
                output_path.parent.mkdir(parents=True, exist_ok=True)
                trimmed.write_videofile(str(output_path), codec="libx264", audio_codec="aac", verbose=False, logger=None)
            return {
                'success': True,
                'operation': 'trim_video',
                'input_path': str(video_path),
                'output_path': str(output_path),
                'trim_range': f"{start_time} to {end_time}",
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Error trimming video {video_path}: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'operation': 'trim_video',
                'input_path': str(video_path),
                'output_path': str(output_path)
            } 