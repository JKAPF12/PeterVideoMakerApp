import { useState } from "react";
import WaitingScreen from "./WaitingScreen";
import VideoPlayer from "./VideoPlayer";
import { useAuth } from "./contexts/AuthContext";
import { getAuth } from "firebase/auth"; // NEW

const CHARACTERS = [
  "Peter Griffin",
  "Stewie Griffin",
  "Brian Griffin",
  "Original Mascot",
];

const SONGS = [
  "Lo-fi Chill",
  "Upbeat Tech",
  "Cinematic Atmosphere",
  "None",
];

export default function VideoCreator() {
  const { credits, deductCredit } = useAuth();
  const [prompt, setPrompt] = useState("");
  const [chars, setChars] = useState([CHARACTERS[0]]);
  const [song, setSong] = useState(SONGS[0]);
  const [stage, setStage] = useState("idle"); // idle, waiting, done
  const [videoUrl, setVideoUrl] = useState(null);
  const [error, setError] = useState("");

  const submit = async (e) => {
    e.preventDefault();

    if (prompt.trim().split(/\s+/).length > 20) {
      setError("Prompt max 20 words.");
      return;
    }
    if (credits < 1) {
      setError("No credits left.");
      return;
    }

    setError("");
    setStage("waiting");

    try {
      // 1️⃣ Get Firebase token
      const token = await getAuth().currentUser.getIdToken();

      // 2️⃣ Send job request
      const API_BASE = import.meta.env.VITE_API_BASE;

      const res = await fetch(`${API_BASE}/generate-video`, {
        method: "POST",
        headers: { 
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`
        },
        body: JSON.stringify({
          topic: prompt,
          characters: chars,
          song,
          type: "spongebob"
        }),
      });

      const data = await res.json();

      if (!res.ok) {
        throw new Error(data.error || "Failed to start job");
      }

      const jobId = data.jobId;

      // 3️⃣ Poll job status every 5 sec
      let done = false;
      while (!done) {
        await new Promise(r => setTimeout(r, 5000));
        const statusRes = await fetch(`${API_BASE}/job-status/${jobId}`);
        const statusData = await statusRes.json();  // <-- missing line
        setVideoUrl(`${API_BASE}/videos/${jobId}.mp4`);

        if (statusData.status === "done") {
          await deductCredit();
          setVideoUrl(`${API_BASE}/videos/${jobId}.mp4`);
          setStage("done");
          done = true;
        } else if (statusData.status === "failed") {
          setError(statusData.error || "Generation failed");
          setStage("idle");
          done = true;
        }
      }

    } catch (err) {
      console.error(err);
      setError("Error connecting to backend.");
      setStage("idle");
    }
  };

  const toggleChar = (c) => {
    setChars((prev) =>
      prev.includes(c) ? prev.filter((x) => x !== c) : [...prev, c]
    );
  };

  return (
    <div className="card">
      <h2>Create Explainer Video</h2>
      <p>Type a topic (max 20 words), choose characters and background music.</p>

      <form onSubmit={submit} className="form">
        <div className="field">
          <label>Topic prompt</label>
          <input
            placeholder="e.g., Explain compound interest simply"
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            required
          />
        </div>

        <div className="field">
          <label>Characters</label>
          <div className="checkbox-group">
            {CHARACTERS.map((c) => (
              <label key={c} className="checkbox-label">
                <input
                  type="checkbox"
                  checked={chars.includes(c)}
                  onChange={() => toggleChar(c)}
                />
                {c}
              </label>
            ))}
          </div>
        </div>

        <div className="field">
          <label>Background song</label>
          <select value={song} onChange={(e) => setSong(e.target.value)}>
            {SONGS.map((s) => (
              <option key={s}>{s}</option>
            ))}
          </select>
        </div>

        <button type="submit" disabled={stage === "waiting"}>
          Generate Video
        </button>
        {error && <div className="error">{error}</div>}
      </form>

      {stage === "waiting" && <WaitingScreen />}
      {stage === "done" && videoUrl && (
        <VideoPlayer
          src={videoUrl}
          prompt={prompt}
          characters={chars}
          song={song}
        />
      )}
    </div>
  );
}
