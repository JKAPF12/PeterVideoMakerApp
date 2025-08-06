import uuid
import os
import subprocess
from pathlib import Path
from script_writer import build_script
from auth_utils import check_and_deduct_credit
from subtitles import VideoTranscriber
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips, CompositeVideoClip, ImageClip
import re
import sys
import uuid
import time
from pathlib import Path
# Paths
OUTPUT_BASE = Path(os.getenv("VIDEO_OUTPUT_BASE", "./generated_videos"))
CHARACTER_IMAGE_DIR = Path("./characters")
BACKGROUND_DIR = Path("./backgrounds")

def run_job(uid, topic, characters, song, video_type):
    job_id = str(uuid.uuid4())
    job_dir = OUTPUT_BASE / job_id
    job_dir.mkdir(parents=True, exist_ok=True)
    metadata = {"status": "started", "steps": []}

    # 1. Deduct credit
    try:
        check_and_deduct_credit(uid)
    except Exception as e:
        metadata["status"] = "failed"
        metadata["error"] = str(e)
        return job_id, metadata

    # 2. Script generation
    script = build_script(topic, characters)
    (job_dir / "script.txt").write_text(script)
    metadata["steps"].append("script_generated")

    # 3. Parse script into dialogue lines
    dialogues = parse_script(script)

    # 4. Generate voices
    audio_outputs = []
    for idx, dlg in enumerate(dialogues):
        char = dlg["character"]
        line = dlg["line"]
        output_audio = job_dir / f"audio_{idx}.wav"

        cmd = [
            sys.executable,
            "generate_voice.py",
            "--tts_text", line,
            "--tts_pitch", "0",
            "--output_rvc_path", str(output_audio),
            "--tts_voice", "en-US-GuyNeural",
            "--pth_path", f"C:/Users/jonat_rdnm2v4/Downloads/Applio-3.2.8-bugfix2/Applio-3.2.8-bugfix/logs/{char.lower()}/{char.lower()}.pth",
            "--index_path", f"C:/Users/jonat_rdnm2v4/Downloads/Applio-3.2.8-bugfix2/Applio-3.2.8-bugfix/logs/{char.lower()}/{char.lower()}.index"
        ]

        subprocess.run(cmd, check=True)
        audio_outputs.append({"character": char, "path": str(output_audio)})

    metadata["steps"].append("voice_done")

    # 5. Assemble video
    final_video_path = job_dir / f"{job_id}.mp4"
    assemble_video(dialogues, audio_outputs, song, final_video_path)
    metadata["steps"].append("video_done")

    # 6. Add subtitles
    transcriber = VideoTranscriber(model_path="medium", video_path=str(final_video_path))
    transcriber.extract_audio()
    transcriber.transcribe_video()
    subtitled_output = job_dir / f"{job_id}_final.mp4"
    transcriber.create_video(str(subtitled_output), video_type)
    metadata["steps"].append("subtitles_done")

    metadata["status"] = "done"
    metadata["video_path"] = str(subtitled_output)
    return job_id, metadata

# def run_job(uid, topic, characters, song, video_type):
#     job_id = str(uuid.uuid4())
#     job_dir = OUTPUT_BASE / job_id
#     job_dir.mkdir(parents=True, exist_ok=True)
#     metadata = {"status": "started", "steps": []}

#     # 1. Deduct credit
#     try:
#         check_and_deduct_credit(uid)
#     except Exception as e:
#         metadata["status"] = "failed"
#         metadata["error"] = str(e)
#         return job_id, metadata

#     # 2. Script generation
#     script = build_script(topic, characters)
#     (job_dir / "script.txt").write_text(script)
#     metadata["steps"].append("script_generated")

#     # 3. Parse script into dialogue lines
#     dialogues = parse_script(script)

#     # 4. Generate voices for each line
#     audio_outputs = []
#     for idx, dlg in enumerate(dialogues):
#         char = dlg["character"]
#         line = dlg["line"]
#         output_audio = job_dir / f"audio_{idx}.wav"

#         cmd = [
#             sys.executable,
#             "generate_voice.py",
#             "--tts_text", line,
#             "--tts_pitch", "0",
#             "--output_rvc_path", str(output_audio),
#             "--tts_voice", "en-US-GuyNeural",
#             "--pth_path", f"C:/Users/jonat_rdnm2v4/Downloads/Applio-3.2.8-bugfix2/Applio-3.2.8-bugfix/logs/{char.lower()}/{char.lower()}.pth",
#             "--index_path", f"C:/Users/jonat_rdnm2v4/Downloads/Applio-3.2.8-bugfix2/Applio-3.2.8-bugfix/logs/{char.lower()}/{char.lower()}.index"
#         ]

#         subprocess.run(cmd, check=True)
#         audio_outputs.append({"character": char, "path": str(output_audio)})

#     metadata["steps"].append("voice_done")

#     # 5. Assemble video
#     final_video_path = job_dir / f"{job_id}.mp4"
#     assemble_video(dialogues, audio_outputs, song, final_video_path)
#     metadata["steps"].append("video_done")

#     # 6. Add subtitles
#     transcriber = VideoTranscriber(model_path="medium", video_path=str(final_video_path))
#     transcriber.extract_audio()
#     transcriber.transcribe_video()
#     subtitled_output = job_dir / f"{job_id}_final.mp4"
#     transcriber.create_video(str(subtitled_output), video_type)
#     metadata["steps"].append("subtitles_done")

#     metadata["status"] = "done"
#     metadata["video_path"] = str(subtitled_output)
#     return job_id, metadata


def parse_script(script: str):
    lines = script.strip().split("\n")
    dialogues = []
    for line in lines:
        match = re.match(r'^(.+?):\s*"(.*)"$', line.strip())
        if match:
            character = match.group(1).strip()
            text = match.group(2).strip()
            dialogues.append({"character": character, "line": text})
    return dialogues


def assemble_video(dialogues, audio_data, song, output_path):
    # Load background
    bg_video_path = BACKGROUND_DIR / "default.mp4"
    if not bg_video_path.exists():
        raise FileNotFoundError(f"Background video not found: {bg_video_path}")

    bg_clip = VideoFileClip(str(bg_video_path))

    video_segments = []
    current_start = 0

    for idx, dlg in enumerate(dialogues):
        char_name = dlg["character"].lower()
        audio_path = audio_data[idx]["path"]

        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Audio not found: {audio_path}")

        audio_clip = AudioFileClip(audio_path)

        # Character image
        char_img_path = CHARACTER_IMAGE_DIR / f"{char_name}.png"
        if not char_img_path.exists():
            char_img_path = CHARACTER_IMAGE_DIR / f"{char_name}.jpg"
        if not char_img_path.exists():
            raise FileNotFoundError(f"Character image not found for: {char_name}")

        img_clip = ImageClip(str(char_img_path)).set_duration(audio_clip.duration)
        img_clip = img_clip.resize(height=300)
        img_clip = img_clip.set_position(("center", "center"))

        # Video section matching audio
        section = bg_clip.subclip(current_start, current_start + audio_clip.duration)

        # Composite: background + character image
        composite = CompositeVideoClip([section, img_clip])
        composite = composite.set_audio(audio_clip)

        video_segments.append(composite)
        current_start += audio_clip.duration

    # Merge all video segments
    final_video = concatenate_videoclips(video_segments, method="compose")
    final_video.write_videofile(str(output_path), codec="libx264", audio_codec="aac")

    # Cleanup
    bg_clip.close()
    for seg in video_segments:
        seg.close()
