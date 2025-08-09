# #
# conda activate EmailChecker
# cd C:\Users\jonat_rdnm2v4\Downloads\Applio-3.2.8-bugfix2\Applio-3.2.8-bugfix
# myenv\Scripts\activate
# cd C:\dev\video-explainers\backend
# uvicorn server:app --reload --host 0.0.0.0 --port 8000
# # ngrok http 8000

# import subprocess
# import re
# import time
# import json
# from fastapi import FastAPI, HTTPException, Header, BackgroundTasks
# from fastapi.responses import FileResponse
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel
# from auth_utils import verify_firebase_token
# from orchestrator import run_job
# import os

# from dotenv import load_dotenv
# from pathlib import Path

# # Explicitly load .env from root dir
# load_dotenv(dotenv_path=Path(__file__).parent.parent / ".env")

# app = FastAPI()
# JOBS_DIR = Path("jobs")
# JOBS_DIR.mkdir(exist_ok=True)

# # Allow everything in dev
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# class GenerateRequest(BaseModel):
#     topic: str
#     characters: list[str]
#     song: str
#     type: str  # e.g., "spongebob", "president"

# # @app.post("/generate-video")
# # async def generate_video(req: GenerateRequest, background_tasks: BackgroundTasks, authorization: str = Header(...)):
# #     if not authorization.startswith("Bearer "):
# #         raise HTTPException(401, "Missing token")
# #     token = authorization.split(" ")[1]
# #     decoded = verify_firebase_token(token)
# #     uid = decoded["uid"]
# @app.post("/generate-video")
# async def generate_video(req: GenerateRequest, background_tasks: BackgroundTasks, authorization: str = Header(...)):
#     if not authorization.startswith("Bearer "):
#         raise HTTPException(401, "Missing token")
#     token = authorization.split(" ")[1]
#     decoded = verify_firebase_token(token)
#     uid = decoded["uid"]

#     # 1. Generate a new job ID
#     import uuid
#     job_id = str(uuid.uuid4())

#     # 2. Write initial job state
#     job_file = JOBS_DIR / f"{job_id}.json"
#     job_file.write_text(json.dumps({
#         "status": "started",
#         "video_url": None,
#         "error": None
#     }))

#     # 3. Run in background
#     background_tasks.add_task(process_video_job, job_id, uid, req.topic, req.characters, req.song, req.type)

#     # 4. Respond immediately
#     return {"jobId": job_id, "status": "started"}

# @app.get("/job-status/{job_id}")
# def job_status(job_id: str):
#     job_file = JOBS_DIR / f"{job_id}.json"
#     if not job_file.exists():
#         raise HTTPException(404, "Job not found")
#     data = json.loads(job_file.read_text())
#     return data

# @app.get("/videos/{job_id}.mp4")
# def get_video(job_id: str):
#     video_path = Path(f"generated_videos/{job_id}/{job_id}_final.mp4")
#     if not video_path.exists():
#         raise HTTPException(404, "Video not ready")
#     return FileResponse(video_path)

# # === NGROK STARTER ===

# @app.get("/health")
# def health():
#     return {"ok": True}

# def start_ngrok():
#     try:
#         print("🔁 Launching ngrok tunnel on port 8000...")
#         subprocess.Popen(["ngrok", "http", "8000"])
#         time.sleep(10)

#         tunnel_info = subprocess.check_output(["curl", "-s", "http://localhost:4040/api/tunnels"]).decode("utf-8")
#         match = re.search(r"https://[a-zA-Z0-9\-]+\.ngrok.io", tunnel_info)
#         if match:
#             ngrok_url = match.group(0)
#             print(f"✅ Ngrok URL: {ngrok_url}")

#             # Optional: write to frontend .env file
#             with open("../.env.ngrok", "w") as f:
#                 f.write(f"VITE_API_URL={ngrok_url}")
#         else:
#             print("❌ Ngrok URL not found.")
#     except Exception as e:
#         print(f"❌ Failed to start ngrok: {e}")

# def process_video_job(job_id, uid, topic, characters, song, vid_type):
#     job_file = JOBS_DIR / f"{job_id}.json"
#     try:
#         print(f"[PROCESS JOB] Kicked off for job {job_id}")
#         job_id_str, metadata = run_job(uid, topic, characters, song, vid_type)
#         print(f"[PROCESS JOB] Finished job {job_id}, got metadata: {metadata}")
#         job_file.write_text(json.dumps(metadata))
#     except Exception as e:
#         print(f"[PROCESS JOB] Failed: {e}")
#         error_meta = {"status": "failed", "error": str(e)}
#         job_file.write_text(json.dumps(error_meta))

#ACVTUALLY FUNCTIONAL
# import json
# import os
# import uuid
# from pathlib import Path

# from dotenv import load_dotenv
# from fastapi import FastAPI, HTTPException, Header, BackgroundTasks
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.responses import FileResponse
# from pydantic import BaseModel

# from auth_utils import verify_firebase_token
# from orchestrator import run_job

# # Load .env from project root (adjust if needed)
# load_dotenv()

# app = FastAPI()
# JOBS_DIR = Path("jobs")
# JOBS_DIR.mkdir(exist_ok=True)

# # Broad CORS for dev
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # lock down for prod
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# class GenerateRequest(BaseModel):
#     topic: str
#     characters: list[str]
#     song: str
#     type: str  # e.g., "spongebob", "president"

# @app.get("/health")
# def health():
#     return {"ok": True}

# @app.post("/generate-video")
# async def generate_video(req: GenerateRequest, background_tasks: BackgroundTasks, authorization: str = Header(...)):
#     if not authorization.startswith("Bearer "):
#         raise HTTPException(401, "Missing token")
#     token = authorization.split(" ")[1]
#     decoded = verify_firebase_token(token)
#     uid = decoded["uid"]

#     job_id = str(uuid.uuid4())
#     job_file = JOBS_DIR / f"{job_id}.json"
#     job_file.write_text(json.dumps({"status": "started", "video_url": None, "error": None}))

#     background_tasks.add_task(process_video_job, job_id, uid, req.topic, req.characters, req.song, req.type)

#     return {"jobId": job_id, "status": "started"}

# @app.get("/job-status/{job_id}")
# def job_status(job_id: str):
#     job_file = JOBS_DIR / f"{job_id}.json"
#     if not job_file.exists():
#         raise HTTPException(404, "Job not found")
#     data = json.loads(job_file.read_text())
#     return data

# @app.get("/videos/{job_id}.mp4")
# def get_video(job_id: str):
#     video_path = Path(f"generated_videos/{job_id}/{job_id}_final.mp4")
#     if not video_path.exists():
#         raise HTTPException(404, "Video not ready")
#     return FileResponse(video_path)

# def process_video_job(job_id, uid, topic, characters, song, vid_type):
#     job_file = JOBS_DIR / f"{job_id}.json"
#     try:
#         from orchestrator import run_job  # local import to avoid import-time side effects
#         print(f"[PROCESS JOB] Kicked off for job {job_id}")
#         job_id_str, metadata = run_job(uid, topic, characters, song, vid_type)
#         print(f"[PROCESS JOB] Finished job {job_id}, got metadata: {metadata}")
#         job_file.write_text(json.dumps(metadata))
#     except Exception as e:
#         print(f"[PROCESS JOB] Failed: {e}")
#         job_file.write_text(json.dumps({"status": "failed", "error": str(e)}))

# if __name__ == "__main__":
#     import uvicorn
#     # Run backend; start ngrok in a separate terminal
#     uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)

#REALLY FUNCTIONAL VERSION FOR PREMADE

# import json
# from pathlib import Path

# from dotenv import load_dotenv
# from fastapi import FastAPI, HTTPException, Header, BackgroundTasks
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.responses import FileResponse
# from fastapi.staticfiles import StaticFiles
# from pydantic import BaseModel

# from auth_utils import verify_firebase_token

# # Load env vars
# load_dotenv()

# app = FastAPI()
# JOBS_DIR = Path("jobs")
# JOBS_DIR.mkdir(exist_ok=True)

# # ====== CONFIG: PRE-MADE VIDEO ======
# PREMADE_JOB_ID = "37b47a64-81ac-4427-8a4b-7ad7819dc85a"
# # NOTE: this is the actual file on disk
# PREMADE_VIDEO_PATH = Path(f"generated_videos/{PREMADE_JOB_ID}/{PREMADE_JOB_ID}_final.mp4")

# # ---- CORS (dev-friendly) ----
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],           # tighten for prod
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
#     expose_headers=["Accept-Ranges", "Content-Length", "Content-Range"],
# )

# # ---- Serve /generated_videos/... as static files ----
# # This makes /generated_videos/{id}/{id}_final.mp4 directly reachable
# static_dir = Path("generated_videos")
# static_dir.mkdir(exist_ok=True, parents=True)
# app.mount("/generated_videos", StaticFiles(directory=str(static_dir)), name="generated_videos")


# class GenerateRequest(BaseModel):
#     topic: str
#     characters: list[str]
#     song: str
#     type: str


# @app.get("/health")
# def health():
#     return {"ok": True}


# @app.post("/generate-video")
# async def generate_video(
#     req: GenerateRequest,
#     background_tasks: BackgroundTasks,
#     authorization: str = Header(...),
# ):
#     """TEMP: Always return a pre-made video job."""
#     if not authorization.startswith("Bearer "):
#         raise HTTPException(401, "Missing token")
#     token = authorization.split(" ")[1]
#     decoded = verify_firebase_token(token)
#     _uid = decoded["uid"]

#     # Write an instant "done" job status snapshot (optional but keeps parity)
#     job_file = JOBS_DIR / f"{PREMADE_JOB_ID}.json"
#     job_file.write_text(json.dumps({
#         "status": "done",
#         "video_url": f"/videos/{PREMADE_JOB_ID}.mp4",   # <-- use /videos route
#         "error": None,
#     }))

#     return {"jobId": PREMADE_JOB_ID, "status": "started"}


# @app.get("/job-status/{job_id}")
# def job_status(job_id: str):
#     """TEMP: Always return 'done' with the exact path you want."""
#     if job_id != PREMADE_JOB_ID:
#         raise HTTPException(404, "Job not found")
#     # Return the URL you asked for
#     return {
#         "status": "done",
#         "video_url": f"/videos/{PREMADE_JOB_ID}.mp4",   # <-- use /videos route
#         "error": None,
#     }


# @app.get("/videos/{job_id}.mp4")
# def get_video(job_id: str):
#     # if job_id != PREMADE_JOB_ID:
#     #     raise HTTPException(404, "Video not found")
#     # if not PREMADE_VIDEO_PATH.exists():
#     #     raise HTTPException(404, f"Video file missing: {PREMADE_VIDEO_PATH}")

#     resp = FileResponse(PREMADE_VIDEO_PATH, media_type="video/mp4")
#     resp.headers["Accept-Ranges"] = "bytes"
#     return resp



# if __name__ == "__main__":
#     import uvicorn

#     uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
import json
import uuid
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Header, BackgroundTasks, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from auth_utils import verify_firebase_token
from orchestrator import run_job  # direct import since we’re controlling job_id

# --- env ---
load_dotenv()

app = FastAPI()

JOBS_DIR = Path("jobs")
JOBS_DIR.mkdir(exist_ok=True)

GEN_DIR = Path("generated_videos")
GEN_DIR.mkdir(exist_ok=True, parents=True)

# CORS (dev)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Accept-Ranges", "Content-Length", "Content-Range"],
)

# Static serving for debug
app.mount("/generated_videos", StaticFiles(directory=str(GEN_DIR)), name="generated_videos")


class GenerateRequest(BaseModel):
    topic: str
    characters: list[str]
    song: str
    type: str  # e.g. "spongebob", "president"


@app.get("/health")
def health():
    return {"ok": True}


@app.post("/generate-video")
async def generate_video(
    req: GenerateRequest,
    background_tasks: BackgroundTasks,
    authorization: str = Header(...)
):
    # Auth
    if not authorization.startswith("Bearer "):
        raise HTTPException(401, "Missing token")
    token = authorization.split(" ")[1]
    decoded = verify_firebase_token(token)
    uid = decoded["uid"]

    # Create controlled job id
    job_id = str(uuid.uuid4())

    # Seed job status file
    job_file = JOBS_DIR / f"{job_id}.json"
    job_file.write_text(json.dumps({
        "status": "started",
        "video_url": None,
        "error": None
    }))

    # Background process
    background_tasks.add_task(process_video_job, job_id, uid, req.topic, req.characters, req.song, req.type)

    return {"jobId": job_id, "status": "started"}


@app.get("/job-status/{job_id}")
def job_status(job_id: str):
    job_file = JOBS_DIR / f"{job_id}.json"
    if not job_file.exists():
        raise HTTPException(404, "Job not found")
    return json.loads(job_file.read_text())


# ---- Byte-range streaming ----
def _open_segment(path: Path, start: int, end: int, chunk_size: int = 1024 * 1024):
    with path.open("rb") as f:
        f.seek(start)
        remaining = end - start + 1
        while remaining > 0:
            read_len = min(chunk_size, remaining)
            data = f.read(read_len)
            if not data:
                break
            remaining -= len(data)
            yield data


@app.get("/videos/{job_id}.mp4")
def stream_video(job_id: str, request: Request):
    path = GEN_DIR / job_id / f"{job_id}_final.mp4"
    if not path.exists():
        raise HTTPException(404, "Video not ready")

    file_size = path.stat().st_size
    range_header: Optional[str] = request.headers.get("range")

    if range_header:
        try:
            bytes_str = range_header.strip().lower().replace("bytes=", "")
            start_str, end_str = bytes_str.split("-", 1) if "-" in bytes_str else (bytes_str, "")
            start = int(start_str) if start_str else 0
            end = int(end_str) if end_str else file_size - 1
            end = min(end, file_size - 1)

            if start > end or start >= file_size:
                headers = {
                    "Content-Range": f"bytes */{file_size}",
                    "Accept-Ranges": "bytes",
                }
                return Response(status_code=416, headers=headers)

            chunk_iter = _open_segment(path, start, end)
            content_length = end - start + 1
            headers = {
                "Content-Range": f"bytes {start}-{end}/{file_size}",
                "Accept-Ranges": "bytes",
                "Content-Length": str(content_length),
            }
            return StreamingResponse(chunk_iter, media_type="video/mp4", status_code=206, headers=headers)
        except Exception:
            pass

    headers = {
        "Accept-Ranges": "bytes",
        "Content-Length": str(file_size),
    }
    return StreamingResponse(path.open("rb"), media_type="video/mp4", headers=headers)


# --- Background job runner ---
def process_video_job(job_id: str, uid: str, topic: str, characters: list[str], song: str, vid_type: str):
    job_file = JOBS_DIR / f"{job_id}.json"
    try:
        run_job(job_id, uid, topic, characters, song, vid_type)

        # Build the final video path
        final_path = GEN_DIR / job_id / f"{job_id}_final.mp4"
        if not final_path.exists():
            raise FileNotFoundError(f"Final video not found: {final_path}")

        final_meta = {
            "status": "done",
            "video_url": f"/videos/{job_id}.mp4",
            "error": None
        }
        job_file.write_text(json.dumps(final_meta))

    except Exception as e:
        job_file.write_text(json.dumps({
            "status": "failed",
            "video_url": None,
            "error": str(e)
        }))




if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
