from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

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
def get_simple_test(video_id: str = Query(None)):
    # 어떤 요청이 오든, 무조건 성공 메시지를 반환하는 테스트용 코드
    return {"transcript": f"서버가 성공적으로 응답했습니다. 요청하신 비디오 ID는 '{video_id}' 입니다."}
