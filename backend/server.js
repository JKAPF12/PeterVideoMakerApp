import express from "express";
import { exec } from "child_process";
import path from "path";
import cors from "cors";

const app = express();
app.use(cors());
app.use(express.json());

const OUTPUT_DIR = path.join(process.cwd(), "generated-videos");

app.post("/generate-video", (req, res) => {
  const { prompt, characters, song } = req.body;

  // Example: run your local program
  // Replace `python my_script.py` with your real generator command
  const command = `python generate_video.py "${prompt}" "${characters.join(",")}" "${song}"`;

  exec(command, { cwd: OUTPUT_DIR }, (err, stdout, stderr) => {
    if (err) {
      console.error(stderr);
      return res.status(500).json({ error: "Video generation failed." });
    }

    const videoPath = path.join(OUTPUT_DIR, "output.mp4"); // adjust to match your generator output
    res.json({ videoUrl: `http://localhost:4000/videos/output.mp4` });
  });
});

// Serve generated videos
app.use("/videos", express.static(OUTPUT_DIR));

app.listen(4000, () => {
  console.log("Backend listening on http://localhost:4000");
});
