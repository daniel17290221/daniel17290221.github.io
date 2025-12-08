from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound

# FastAPI 앱 생성
app = FastAPI()

# CORS 미들웨어 추가: 모든 출처에서의 요청을 허용합니다.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Vercel에서 FastAPI 앱을 인식하도록 핸들러를 지정합니다.
handler = app

@app.get("/api/extractor")
def get_transcript(video_id: str = Query(None)):
    if not video_id:
        raise HTTPException(status_code=400, detail="video_id is required")
    try:
        # 한국어 자막을 먼저 시도하고, 없으면 영어 자막을 가져옵니다.
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['ko', 'en'])
        full_transcript = " ".join([item['text'] for item in transcript_list])
        return {"transcript": full_transcript}
    except TranscriptsDisabled:
        raise HTTPException(status_code=404, detail="해당 영상은 자막 기능이 비활성화되어 있습니다.")
    except NoTranscriptFound:
        raise HTTPException(status_code=404, detail="영상에서 한국어 또는 영어 자막을 찾을 수 없습니다.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"서버에서 오류가 발생했습니다: {str(e)}")
