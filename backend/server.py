#
# conda activate EmailChecker
# cd C:\Users\jonat_rdnm2v4\Downloads\Applio-3.2.8-bugfix2\Applio-3.2.8-bugfix
# myenv\Scripts\activate
# cd C:\dev\video-explainers\backend
# uvicorn server:app --reload --host 0.0.0.0 --port 8000
#


from fastapi import FastAPI, HTTPException, Header, BackgroundTasks
from pydantic import BaseModel
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os
from auth_utils import verify_firebase_token
from orchestrator import run_job
import json
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()
JOBS_DIR = Path("jobs")
JOBS_DIR.mkdir(exist_ok=True)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*",                # For local dev      # For deployed frontend
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class GenerateRequest(BaseModel):
    topic: str
    characters: list[str]
    song: str
    type: str  # e.g., "spongebob", "president"

@app.post("/generate-video")
async def generate_video(req: GenerateRequest, background_tasks: BackgroundTasks, authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(401, "Missing token")
    token = authorization.split(" ")[1]
    decoded = verify_firebase_token(token)
    uid = decoded["uid"]

    job_id, metadata = run_job(uid, req.topic, req.characters, req.song, req.type)
    # persist metadata
    job_file = JOBS_DIR / f"{job_id}.json"
    job_file.write_text(json.dumps(metadata))
    return {"jobId": job_id, "status": metadata["status"]}

@app.get("/job-status/{job_id}")
def job_status(job_id: str):
    job_file = JOBS_DIR / f"{job_id}.json"
    if not job_file.exists():
        raise HTTPException(404, "Job not found")
    data = json.loads(job_file.read_text())
    return data

@app.get("/videos/{job_id}.mp4")
def get_video(job_id: str):
    video_path = Path(f"generated_videos/{job_id}/{job_id}_final.mp4")
    if not video_path.exists():
        raise HTTPException(404, "Video not ready")
    return FileResponse(video_path)
