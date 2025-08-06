import whisper
import os
import shutil
import cv2
from moviepy.editor import ImageSequenceClip, AudioFileClip, VideoFileClip, CompositeAudioClip
from tqdm import tqdm
import moviepy.video.fx.all as vfx
import time
import subprocess
import random
FONT = cv2.FONT_HERSHEY_TRIPLEX
FONT_SCALE = 2
FONT_THICKNESS = 6

class VideoTranscriber:
    def __init__(self, model_path, video_path):
        self.model = whisper.load_model(model_path)
        self.video_path = video_path
        self.audio_path = ''
        self.text_array = []
        self.fps = 0
        self.char_width = 0
        self.music = "./music/music.wav"

    def clear_image_folder(self, folder_path):
        if os.path.exists(folder_path):
            for file in os.listdir(folder_path):
                file_path = os.path.join(folder_path, file)
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
        else:
            os.makedirs(folder_path)
        print('Cleared image folder')

    def transcribe_video(self):
        print('Transcribing video')
        result = self.model.transcribe(self.audio_path)
        sample_text = result["segments"][0]["text"]
        textsize = cv2.getTextSize(sample_text, FONT, FONT_SCALE, FONT_THICKNESS)[0]
        cap = cv2.VideoCapture(self.video_path)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        asp = 16 / 9
        ret, frame = cap.read()
        frame_crop = frame[:, int((width - 1 / asp * height) / 2):width - int((width - 1 / asp * height) / 2)]
        width = frame_crop.shape[1] - int(frame_crop.shape[1] * 0.1)
        self.fps = cap.get(cv2.CAP_PROP_FPS)
        self.char_width = int(textsize[0] / len(sample_text))
        max_line_width = width * 0.7

        for segment in tqdm(result["segments"]):
            text = segment["text"]
            seg_end = segment["end"]
            seg_start = segment["start"]
            total_frames = int((seg_end - seg_start) * self.fps)
            current_frame = int(seg_start * self.fps)
            total_chars = len(text)
            words = [w for w in text.split(" ") if w.strip()]
            i = 0
            while i < len(words):
                line = words[i]
                line_length = (len(line) + 1) * self.char_width
                i += 1
                while i < len(words) and (line_length + (len(words[i]) + 1) * self.char_width) <= max_line_width:
                    line += " " + words[i]
                    line_length += (len(words[i]) + 1) * self.char_width
                    i += 1
                line_duration = int((len(line) / total_chars) * total_frames)
                self.text_array.append([line, current_frame + 15, current_frame + line_duration + 15])
                current_frame += line_duration

        cap.release()
        print('Transcription complete')

    def extract_audio(self):
        print('Extracting audio')
        audio_path = os.path.join(os.path.dirname(self.video_path), "audio.mp3")
        video = VideoFileClip(self.video_path)
        audio = video.audio
        audio.write_audiofile(audio_path)
        self.audio_path = audio_path
        print('Audio extracted')

    def extract_frames(self, output_folder):
            print('Extracting frames')
            cap = cv2.VideoCapture(self.video_path)
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            asp = width / height
            N_frames = 0

            while True:
                ret, frame = cap.read()
                if not ret:
                    break

                # Crop to aspect ratio
                frame = frame[:, int(int(width - 1 / asp * height) / 2):width - int((width - 1 / asp * height) / 2)]

                # Add subtitles if necessary
                for i in self.text_array:
                    if N_frames >= i[1] and N_frames <= i[2]:
                        full_text = i[0].upper()
                        words = [w for w in full_text.split() if w.strip()]
                        if not words:
                            break

                        # Cache word colors once per subtitle
                        if len(i) < 4:  # If no cached colors
                            word_colors = []
                            for _ in words:
                                r = random.random()
                                if r < 0.3:
                                    word_colors.append((0, 255, 255))  # Yellow
                                elif r < 0.6:
                                    word_colors.append((0, 255, 0))    # Green
                                else:
                                    word_colors.append((255, 255, 255))  # White
                            i.append(word_colors)  # Append to subtitle data
                        else:
                            word_colors = i[3]

                        text_y = int(height * 7 / 8)
                        spacing = 20  # Space between words

                        # Center-align: calculate total width
                        word_sizes = [cv2.getTextSize(word, FONT, FONT_SCALE, FONT_THICKNESS)[0] for word in words]
                        total_text_width = sum([size[0] for size in word_sizes]) + spacing * (len(words) - 1)
                        text_x = int((frame.shape[1] - total_text_width) / 2)

                        frames_since_start = N_frames - i[1]
                        delay_per_word = 2  # how many frames to delay each word

                        for idx, word in enumerate(words):
                            if frames_since_start >= delay_per_word * idx:
                                # Animation: scale from 0.8 to 1.0 over 5 frames
                                word_frames_visible = frames_since_start - delay_per_word * idx
                                max_anim_frames = 5
                                scale = min(1.0, 0.8 + 0.2 * (word_frames_visible / max_anim_frames))

                                color = word_colors[idx]
                                font = FONT
                                thickness = max(1, int(FONT_THICKNESS * scale))
                                font_scale = FONT_SCALE * scale

                                word_size, _ = cv2.getTextSize(word, font, font_scale, thickness)
                                cv2.putText(frame, word, (text_x, text_y), font, font_scale, (0, 0, 0), thickness * 2, cv2.LINE_AA)
                                cv2.putText(frame, word, (text_x, text_y), font, font_scale, color, thickness, cv2.LINE_AA)

                                text_x += word_size[0] + spacing
                        break


                cv2.imwrite(os.path.join(output_folder, f"{N_frames}.jpg"), frame)
                N_frames += 1

            cap.release()
            print('Frames extracted')

    def create_video(self, output_video_path, type):
        print('Creating video')
        image_folder = os.path.join(os.path.dirname(self.video_path), "frames")
        if not os.path.exists(image_folder):
            os.makedirs(image_folder)
        self.extract_frames(image_folder)

        images = [img for img in os.listdir(image_folder) if img.endswith(".jpg")]
        images.sort(key=lambda x: int(x.split(".")[0]))

        clip = ImageSequenceClip([os.path.join(image_folder, img) for img in images], fps=self.fps)
        dialogue_audio = AudioFileClip(self.audio_path)
        video_duration = clip.duration

        music_path = os.path.join(os.path.dirname(os.path.dirname(self.video_path)), self.music)
        if os.path.exists(music_path):
            music_audio = AudioFileClip(music_path).volumex(0.38)
            if music_audio.duration > video_duration:
                music_audio = music_audio.subclip(0, video_duration)
            else:
                music_audio = music_audio.fx(vfx.loop, duration=video_duration)
            final_audio = CompositeAudioClip([dialogue_audio, music_audio])
        else:
            print("WARNING: Background music not found. Using only dialogue.")
            final_audio = dialogue_audio

        clip = clip.set_audio(final_audio)
        clip.write_videofile(output_video_path, codec="libx264", audio_codec="aac")

        shutil.rmtree(image_folder)
        os.remove(self.audio_path)
        print(f"Finished processing: {output_video_path}")
