from http.server import BaseHTTPRequestHandler
import json
from urllib.parse import urlparse, parse_qs
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound

class handler(BaseHTTPRequestHandler):

    def do_OPTIONS(self):
        self.send_response(200, "ok")
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header("Access-Control-Allow-Headers", "X-Requested-With, Content-type")
        self.end_headers()

    def do_GET(self):
        # CORS 헤더 설정
        self.send_header('Access-Control-Allow-Origin', '*')
        
        query_components = parse_qs(urlparse(self.path).query)
        video_id = query_components.get('video_id', [None])[0]

        if not video_id:
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': 'video_id is required'}).encode('utf-8'))
            return

        try:
            # find_transcript는 수동으로 생성된 자막과 자동 생성된 자막 모두에서 찾습니다.
            transcript = YouTubeTranscriptApi.list_transcripts(video_id).find_transcript(['ko', 'en'])
            transcript_data = transcript.fetch()
            full_transcript = " ".join([item['text'] for item in transcript_data])
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'transcript': full_transcript}).encode('utf-8'))

        except TranscriptsDisabled:
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': '해당 영상은 자막 기능이 비활성화되어 있습니다.'}).encode('utf-8'))
        except NoTranscriptFound:
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': '영상에서 한국어 또는 영어 자막을 찾을 수 없습니다.'}).encode('utf-8'))
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': f'서버에서 오류가 발생했습니다: {str(e)}'}).encode('utf-8'))
        
        return
