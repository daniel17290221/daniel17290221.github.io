# /api/transcript.py

from http.server import BaseHTTPRequestHandler
import json
import re
from urllib.parse import urlparse, parse_qs
from youtube_transcript_api import YouTubeTranscriptApi

class handler(BaseHTTPRequestHandler):

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        try:
            body = json.loads(post_data)
            video_url = body.get('video_url')

            if not video_url:
                self._send_response(400, {'error': 'video_url이 필요합니다.'})
                return

            video_id = self._extract_video_id(video_url)
            if not video_id:
                self._send_response(400, {'error': '유효하지 않은 유튜브 URL입니다.'})
                return

            transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['ko', 'en'])
            full_transcript = " ".join([item['text'] for item in transcript_list])
            
            self._send_response(200, {'transcript': full_transcript})

        except Exception as e:
            self._send_response(500, {'error': f'대본 추출 중 오류 발생: {str(e)}'})

    def _extract_video_id(self, url):
        # 다양한 유튜브 URL 형식에서 비디오 ID를 추출하는 정규식
        regex = r"(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})"
        match = re.search(regex, url)
        return match.group(1) if match else None

    def _send_response(self, status_code, data):
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        # CORS 에러 방지를 위해 모든 출처 허용
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))

    def do_OPTIONS(self):
        # 웹브라우저가 POST 요청을 보내기 전에 먼저 보내는 사전 요청(preflight) 처리
        self.send_response(200, "ok")
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
