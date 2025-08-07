#
# conda activate EmailChecker
# cd C:\Users\jonat_rdnm2v4\Downloads\Applio-3.2.8-bugfix2\Applio-3.2.8-bugfix
# myenv\Scripts\activate
# cd C:\dev\video-explainers\backend
# uvicorn server:app --reload --host 0.0.0.0 --port 8000
# ngrok http 8000

import subprocess
import re
import time
import json
from fastapi import FastAPI, HTTPException, Header, BackgroundTasks
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from auth_utils import verify_firebase_token
from orchestrator import run_job
import os

from dotenv import load_dotenv
from pathlib import Path

# Explicitly load .env from root dir
load_dotenv(dotenv_path=Path(__file__).parent.parent / ".env")

app = FastAPI()
JOBS_DIR = Path("jobs")
JOBS_DIR.mkdir(exist_ok=True)

# Allow everything in dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class GenerateRequest(BaseModel):
    topic: str
    characters: list[str]
    song: str
    type: str  # e.g., "spongebob", "president"

# @app.post("/generate-video")
# async def generate_video(req: GenerateRequest, background_tasks: BackgroundTasks, authorization: str = Header(...)):
#     if not authorization.startswith("Bearer "):
#         raise HTTPException(401, "Missing token")
#     token = authorization.split(" ")[1]
#     decoded = verify_firebase_token(token)
#     uid = decoded["uid"]
@app.post("/generate-video")
async def generate_video(req: GenerateRequest, background_tasks: BackgroundTasks, authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(401, "Missing token")
    token = authorization.split(" ")[1]
    decoded = verify_firebase_token(token)
    uid = decoded["uid"]

    # 1. Generate a new job ID
    import uuid
    job_id = str(uuid.uuid4())

    # 2. Write initial job state
    job_file = JOBS_DIR / f"{job_id}.json"
    job_file.write_text(json.dumps({
        "status": "started",
        "video_url": None,
        "error": None
    }))

    # 3. Run in background
    background_tasks.add_task(process_video_job, job_id, uid, req.topic, req.characters, req.song, req.type)

    # 4. Respond immediately
    return {"jobId": job_id, "status": "started"}

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

# === NGROK STARTER ===

def start_ngrok():
    try:
        print("🔁 Launching ngrok tunnel on port 8000...")
        subprocess.Popen(["ngrok", "http", "8000"])
        time.sleep(10)

        tunnel_info = subprocess.check_output(["curl", "-s", "http://localhost:4040/api/tunnels"]).decode("utf-8")
        match = re.search(r"https://[a-zA-Z0-9\-]+\.ngrok.io", tunnel_info)
        if match:
            ngrok_url = match.group(0)
            print(f"✅ Ngrok URL: {ngrok_url}")

            # Optional: write to frontend .env file
            with open("../.env.ngrok", "w") as f:
                f.write(f"VITE_API_URL={ngrok_url}")
        else:
            print("❌ Ngrok URL not found.")
    except Exception as e:
        print(f"❌ Failed to start ngrok: {e}")

if __name__ == "__main__":
    start_ngrok()
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)

def process_video_job(job_id, uid, topic, characters, song, vid_type):
    job_file = JOBS_DIR / f"{job_id}.json"
    try:
        print(f"[PROCESS JOB] Kicked off for job {job_id}")
        job_id_str, metadata = run_job(uid, topic, characters, song, vid_type)
        print(f"[PROCESS JOB] Finished job {job_id}, got metadata: {metadata}")
        job_file.write_text(json.dumps(metadata))
    except Exception as e:
        print(f"[PROCESS JOB] Failed: {e}")
        error_meta = {"status": "failed", "error": str(e)}
        job_file.write_text(json.dumps(error_meta))