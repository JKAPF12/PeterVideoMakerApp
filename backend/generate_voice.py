import subprocess
import sys
import os
import argparse

print("Using Python executable:", sys.executable)

# **Step 1: Parse Arguments** (Now accepts character name & voice dynamically)
parser = argparse.ArgumentParser()
parser.add_argument("--tts_text", type=str, required=True, help="Text to convert to speech")
parser.add_argument("--tts_pitch", type=str, required=True, help="Pitch")
parser.add_argument("--output_rvc_path", type=str, required=True, help="Output path for generated audio")
parser.add_argument("--tts_voice", type=str, required=True, help="The voice model to use")
parser.add_argument("--pth_path", type=str, required=True, help="The path to the pth file")
parser.add_argument("--index_path", type=str, required=True, help="The path to the index file")
args = parser.parse_args()

# **Step 2: Ensure Output Folder Exists**
output_folder = os.path.dirname(args.output_rvc_path)
os.makedirs(output_folder, exist_ok=True)

# **Step 3: Construct Command to Run `core.py`**
python_executable = sys.executable  # Ensures correct Python is used

command = [
    python_executable,
    "C:/Users/jonat_rdnm2v4/Downloads/Applio-3.2.8-bugfix2/Applio-3.2.8-bugfix/core.py",
    "tts",
    "--tts_file", "path/to/tts_template.wav",
    "--tts_text", args.tts_text,
    "--tts_voice", args.tts_voice,  # **Dynamically use character's voice**
    "--tts_rate", "17",
    "--pitch", args.tts_pitch,
    "--filter_radius", "3",
    "--index_rate", "0.5",
    "--volume_envelope", "1",
    "--protect", "0.3",
    "--hop_length", "128",
    "--f0_method", "rmvpe",
    "--output_tts_path", "C:/Peter_automation_folders/Baker_Peter/peter_automation/audios/peter_tts.wav",
    "--output_rvc_path", args.output_rvc_path,
    "--pth_path", args.pth_path,
    "--index_path", args.index_path,
    "--split_audio", "False",
    "--f0_autotune", "False",
    "--f0_autotune_strength", "1.0",
    "--clean_audio", "True",
    "--clean_strength", "0.6",
    "--export_format", "WAV",
    "--f0_file", "None",
    "--embedder_model", "contentvec"
]

# **Step 4: Validate Core.py Exists**
if not os.path.exists(command[1]):  
    raise FileNotFoundError(f"DEBUG: core.py not found at {command[1]}")

# **Step 5: Run the TTS Process**
print(f"DEBUG: Running command: {' '.join(command)}")  # Debug output

try:
    subprocess.run(command, check=True)
    print(f"DEBUG: Audio successfully generated at {args.output_rvc_path}")
except subprocess.CalledProcessError as e:
    print(f"ERROR: Voice generation failed: {e}")
