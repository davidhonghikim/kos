"""
Video Add Subtitle Operation

Single-purpose module for adding subtitles to videos.
"""

from moviepy import VideoFileClip, TextClip, CompositeVideoClip
from pathlib import Path
from typing import Dict, Any
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class VideoSubtitleAdder:
    """Add subtitle to video operation"""
    
    def add_subtitle(self, video_path: str, subtitle_text: str, output_path: str, fontsize: int = 24) -> Dict[str, Any]:
        try:
            video_path = Path(video_path)
            output_path = Path(output_path)
            if not video_path.exists():
                return {
                    'success': False,
                    'error': f'Video not found: {video_path}',
                    'operation': 'add_subtitle'
                }
            with VideoFileClip(str(video_path)) as clip:
                txt_clip = TextClip(subtitle_text, fontsize=fontsize, color='white', bg_color='black', size=(clip.w, 50)).set_position(('center', 'bottom')).set_duration(clip.duration)
                video = CompositeVideoClip([clip, txt_clip])
                output_path.parent.mkdir(parents=True, exist_ok=True)
                video.write_videofile(str(output_path), codec="libx264", audio_codec="aac", verbose=False, logger=None)
            return {
                'success': True,
                'operation': 'add_subtitle',
                'input_path': str(video_path),
                'output_path': str(output_path),
                'subtitle_text': subtitle_text,
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Error adding subtitle to video {video_path}: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'operation': 'add_subtitle',
                'input_path': str(video_path),
                'output_path': str(output_path)
            } 