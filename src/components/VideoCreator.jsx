// // // import { useState } from "react";
// // // import WaitingScreen from "./WaitingScreen";
// // // import VideoPlayer from "./VideoPlayer";
// // // import { useAuth } from "./contexts/AuthContext";
// // // import { getAuth } from "firebase/auth"; // NEW

// // // const CHARACTERS = [
// // //   "Peter Griffin",
// // //   "Stewie Griffin",
// // //   "Brian Griffin",
// // //   "Original Mascot",
// // // ];

// // // const SONGS = [
// // //   "Lo-fi Chill",
// // //   "Upbeat Tech",
// // //   "Cinematic Atmosphere",
// // //   "None",
// // // ];

// // // export default function VideoCreator() {
// // //   const { credits, deductCredit } = useAuth();
// // //   const [prompt, setPrompt] = useState("");
// // //   const [chars, setChars] = useState([CHARACTERS[0]]);
// // //   const [song, setSong] = useState(SONGS[0]);
// // //   const [stage, setStage] = useState("idle"); // idle, waiting, done
// // //   const [videoUrl, setVideoUrl] = useState(null);
// // //   const [error, setError] = useState("");

// // //  const submit = async (e) => {
// // //   e.preventDefault();

// // //   if (prompt.trim().split(/\s+/).length > 20) {
// // //     setError("Prompt max 20 words.");
// // //     return;
// // //   }
// // //   if (credits < 1) {
// // //     setError("No credits left.");
// // //     return;
// // //   }

// // //   setError("");
// // //   setStage("waiting");

// // //   try {
// // //     // 1️⃣ Get Firebase token
// // //     const token = await getAuth().currentUser.getIdToken();

// // //     // 2️⃣ Send job request
// // //     const API_BASE = import.meta.env.VITE_API_BASE;
// // //     console.log("🌍 API_BASE is:", API_BASE);

// // //     const res = await fetch(`${API_BASE}/generate-video`, {
// // //       method: "POST",
// // //       headers: { 
// // //         "Content-Type": "application/json",
// // //         Authorization: `Bearer ${token}`
// // //       },
// // //       body: JSON.stringify({
// // //         topic: prompt,
// // //         characters: chars,
// // //         song,
// // //         type: "spongebob"
// // //       }),
// // //     });

// // //     const data = await res.json();
// // //     console.log("🚀 POST /generate-video response:", res.status);
// // //     console.log("🎯 JSON data:", data);

// // //     if (!res.ok) {
// // //       throw new Error(data.error || "Failed to start job");
// // //     }

// // //     const jobId = data.jobId;
// // //     console.log("🎬 Job ID:", jobId);

// // //     // 3️⃣ Poll job status every 5 sec
// // //     let done = false;
// // //     while (!done) {
// // //       await new Promise(r => setTimeout(r, 5000));

// // //       try {
// // //         console.log("Polling:", `${API_BASE}/job-status/${jobId}`);

// // //         const statusRes = await fetch(`${API_BASE}/job-status/${jobId}`, { cache: "no-store" });
// // //         const text = await statusRes.text();

// // //         let statusData;
// // //         try {
// // //           statusData = JSON.parse(text);
// // //         } catch (e) {
// // //           console.error("❌ Non-JSON status body:", text);
// // //           throw new Error("Backend returned non-JSON (probably HTML from ngrok splash/limit page).");
// // //         }

// // //         console.log("🔁 Job status:", statusData);

// // //         if (statusData.status === "done") {
// // //           await deductCredit();
// // //           setVideoUrl(`${API_BASE}/videos/${jobId}.mp4`);
// // //           setStage("done");
// // //           done = true;
// // //         } else if (statusData.status === "failed") {
// // //           setError(statusData.error || "Generation failed");
// // //           setStage("idle");
// // //           done = true;
// // //         }

// // //       } catch (err) {
// // //         console.error("🛑 Polling failed:", err);
// // //         setError("Lost connection to backend while checking job status.");
// // //         setStage("idle");
// // //         done = true;
// // //       }
// // //     }


// // //   } catch (err) {
// // //     console.error("💥 Error starting job:", err);
// // //     setError("Error connecting to backend.");
// // //     setStage("idle");
// // //   }
// // // };



// // //   const toggleChar = (c) => {
// // //     setChars((prev) =>
// // //       prev.includes(c) ? prev.filter((x) => x !== c) : [...prev, c]
// // //     );
// // //   };

// // //   return (
// // //     <div className="card">
// // //       <h2>Create Explainer Video</h2>
// // //       <p>Type a topic (max 20 words), choose characters and background music.</p>

// // //       <form onSubmit={submit} className="form">
// // //         <div className="field">
// // //           <label>Topic prompt</label>
// // //           <input
// // //             placeholder="e.g., Explain compound interest simply"
// // //             value={prompt}
// // //             onChange={(e) => setPrompt(e.target.value)}
// // //             required
// // //           />
// // //         </div>

// // //         <div className="field">
// // //           <label>Characters</label>
// // //           <div className="checkbox-group">
// // //             {CHARACTERS.map((c) => (
// // //               <label key={c} className="checkbox-label">
// // //                 <input
// // //                   type="checkbox"
// // //                   checked={chars.includes(c)}
// // //                   onChange={() => toggleChar(c)}
// // //                 />
// // //                 {c}
// // //               </label>
// // //             ))}
// // //           </div>
// // //         </div>

// // //         <div className="field">
// // //           <label>Background song</label>
// // //           <select value={song} onChange={(e) => setSong(e.target.value)}>
// // //             {SONGS.map((s) => (
// // //               <option key={s}>{s}</option>
// // //             ))}
// // //           </select>
// // //         </div>

// // //         <button type="submit" disabled={stage === "waiting"}>
// // //           Generate Video
// // //         </button>
// // //         {error && <div className="error">{error}</div>}
// // //       </form>

// // //       {stage === "waiting" && <WaitingScreen />}
// // //       {stage === "done" && videoUrl && (
// // //         <VideoPlayer
// // //           src={videoUrl}
// // //           prompt={prompt}
// // //           characters={chars}
// // //           song={song}
// // //         />
// // //       )}
// // //     </div>
// // //   );
// // // }
// // import { useState } from "react";
// // import WaitingScreen from "./WaitingScreen";
// // import VideoPlayer from "./VideoPlayer";
// // import { useAuth } from "./contexts/AuthContext";
// // import { getAuth } from "firebase/auth";

// // const CHARACTERS = [
// //   "Peter Griffin",
// //   "Stewie Griffin",
// //   "Brian Griffin",
// //   "Original Mascot",
// // ];

// // const SONGS = ["Lo-fi Chill", "Upbeat Tech", "Cinematic Atmosphere", "None"];

// // export default function VideoCreator() {
// //   const { credits /*, deductCredit*/ } = useAuth();
// //   const [prompt, setPrompt] = useState("");
// //   const [chars, setChars] = useState([CHARACTERS[0]]);
// //   const [song, setSong] = useState(SONGS[0]);
// //   const [stage, setStage] = useState("idle"); // idle, waiting, done
// //   const [videoUrl, setVideoUrl] = useState(null);
// //   const [error, setError] = useState("");

// //   const toggleChar = (c) => {
// //     setChars((prev) => (prev.includes(c) ? prev.filter((x) => x !== c) : [...prev, c]));
// //   };

// //   const submit = async (e) => {
// //     e.preventDefault();

// //     if (prompt.trim().split(/\s+/).length > 20) {
// //       setError("Prompt max 20 words.");
// //       return;
// //     }
// //     if (credits < 1) {
// //       setError("No credits left.");
// //       return;
// //     }

// //     setError("");
// //     setStage("waiting");

// //     try {
// //       // 1) Firebase token (assumes user is already signed in via your AuthContext)
// //       const token = await getAuth().currentUser.getIdToken();

// //       // 2) Start job
// //       const API_BASE = import.meta.env.VITE_API_BASE;
// //       console.log("🌍 API_BASE is:", API_BASE);

// //       const res = await fetch(`${API_BASE}/generate-video`, {
// //         method: "POST",
// //         headers: {
// //           "Content-Type": "application/json",
// //           Authorization: `Bearer ${token}`,
// //           "ngrok-skip-browser-warning": "true", // avoid ngrok interstitial
// //           Pragma: "no-cache",
// //           "Cache-Control": "no-cache",
// //         },
// //         body: JSON.stringify({
// //           topic: prompt,
// //           characters: chars,
// //           song,
// //           type: "spongebob",
// //         }),
// //       });

// //       const data = await res.json().catch(async () => {
// //         // If POST ever returns HTML (rare), surface it
// //         const txt = await res.text();
// //         throw new Error(`Non-JSON from POST /generate-video: ${txt.slice(0, 200)}...`);
// //       });

// //       console.log("🚀 POST /generate-video response:", res.status);
// //       console.log("🎯 JSON data:", data);

// //       if (!res.ok) {
// //         throw new Error(data.error || "Failed to start job");
// //       }

// //       const jobId = data.jobId;
// //       console.log("🎬 Job ID:", jobId);

// //       // 3) Poll job status
// //       let done = false;
// //       while (!done) {
// //         await new Promise((r) => setTimeout(r, 5000));

// //         try {
// //           const url = `${API_BASE}/job-status/${jobId}?_ngrok_skip_browser_warning=true`;
// //           console.log("📡 Polling:", url);

// //           const statusRes = await fetch(url, {
// //             cache: "no-store",
// //             headers: {
// //               "ngrok-skip-browser-warning": "true",
// //               Pragma: "no-cache",
// //               "Cache-Control": "no-cache",
// //             },
// //           });

// //           const text = await statusRes.text();

// //           if (!statusRes.ok) {
// //             console.error("❌ Status non-OK body:", text);
// //             throw new Error(`Failed to get job status: HTTP ${statusRes.status}`);
// //           }

// //           let statusData;
// //           try {
// //             statusData = JSON.parse(text);
// //           } catch {
// //             console.error("❌ Non-JSON status body:", text);
// //             throw new Error("Backend returned non-JSON (ngrok warning/HTML).");
// //           }

// //           console.log("🔁 Job status:", statusData);

// //         if (statusData.status === "done") {
// //           // Use server-provided path and make it absolute + add ngrok skip param
// //           const path = statusData.video_url; // e.g. "/generated_videos/<id>/<id>_final.mp4"
// //           const src = `${API_BASE}${path}${
// //             path.includes("?") ? "&" : "?"
// //           }_ngrok_skip_browser_warning=true`;

// //           // IMPORTANT: don't build /videos/${jobId}.mp4 yourself anymore
// //           setVideoUrl(src);
// //           setStage("done");
// //           done = true;
// //         }
// //         } catch (err) {
// //           console.error("🛑 Polling failed:", err);
// //           setError("Lost connection to backend while checking job status.");
// //           setStage("idle");
// //           done = true;
// //         }
// //       }
// //     } catch (err) {
// //       console.error("💥 Error starting job:", err);
// //       setError("Error connecting to backend.");
// //       setStage("idle");
// //     }
// //   };

// //   return (
// //     <div className="card">
// //       <h2>Create Explainer Video</h2>
// //       <p>Type a topic (max 20 words), choose characters and background music.</p>

// //       <form onSubmit={submit} className="form">
// //         <div className="field">
// //           <label>Topic prompt</label>
// //           <input
// //             placeholder="e.g., Explain compound interest simply"
// //             value={prompt}
// //             onChange={(e) => setPrompt(e.target.value)}
// //             required
// //           />
// //         </div>

// //         <div className="field">
// //           <label>Characters</label>
// //           <div className="checkbox-group">
// //             {CHARACTERS.map((c) => (
// //               <label key={c} className="checkbox-label">
// //                 <input
// //                   type="checkbox"
// //                   checked={chars.includes(c)}
// //                   onChange={() => toggleChar(c)}
// //                 />
// //                 {c}
// //               </label>
// //             ))}
// //           </div>
// //         </div>

// //         <div className="field">
// //           <label>Background song</label>
// //           <select value={song} onChange={(e) => setSong(e.target.value)}>
// //             {SONGS.map((s) => (
// //               <option key={s}>{s}</option>
// //             ))}
// //           </select>
// //         </div>

// //         <button type="submit" disabled={stage === "waiting"}>
// //           Generate Video
// //         </button>
// //         {error && <div className="error">{error}</div>}
// //       </form>

// //       {stage === "waiting" && <WaitingScreen />}
// //       {stage === "done" && videoUrl && (
// //         <VideoPlayer src={videoUrl} prompt={prompt} characters={chars} song={song} />
// //       )}
// //     </div>
// //   );
// // }
// //ABOVE IS PREMADE


// // import { useState, useRef, useEffect } from "react";
// // import WaitingScreen from "./WaitingScreen";
// // import VideoPlayer from "./VideoPlayer";
// // import { useAuth } from "./contexts/AuthContext";
// // import { getAuth } from "firebase/auth";

// // const CHARACTERS = ["Peter Griffin", "Stewie Griffin", "Brian Griffin", "Original Mascot"];
// // const SONGS = ["Lo-fi Chill", "Upbeat Tech", "Cinematic Atmosphere", "None"];

// // // Small helper: stable sleep
// // const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

// // // Fetch wrapper that prefers JSON but surfaces HTML/ngrok errors clearly
// // async function fetchJSON(url, options = {}) {
// //   const res = await fetch(url, {
// //     // anti-cache + ngrok skip header
// //     cache: "no-store",
// //     headers: {
// //       "ngrok-skip-browser-warning": "true",
// //       Pragma: "no-cache",
// //       "Cache-Control": "no-cache",
// //       ...(options.headers || {}),
// //     },
// //     ...options,
// //   });

// //   const text = await res.text();
// //   let data;
// //   try {
// //     data = JSON.parse(text);
// //   } catch {
// //     // likely ngrok or proxy HTML page; include head of body for debugging
// //     throw new Error(
// //       `Non-JSON response from ${url} (HTTP ${res.status}). Body head: ${text.slice(0, 300)}...`
// //     );
// //   }
// //   if (!res.ok) {
// //     const msg = data?.error || `HTTP ${res.status}`;
// //     throw new Error(msg);
// //   }
// //   return data;
// // }

// // export default function VideoCreator() {
// //   const { credits, deductCredit: maybeDeductCredit } = useAuth();
// //   const [prompt, setPrompt] = useState("");
// //   const [chars, setChars] = useState([CHARACTERS[0]]);
// //   const [song, setSong] = useState(SONGS[0]);
// //   const [stage, setStage] = useState("idle"); // idle | waiting | done
// //   const [videoUrl, setVideoUrl] = useState(null);
// //   const [error, setError] = useState("");
// //   const [jobId, setJobId] = useState(null);

// //   const isMounted = useRef(true);
// //   useEffect(() => {
// //     return () => {
// //       isMounted.current = false;
// //     };
// //   }, []);

// //   const toggleChar = (c) => {
// //     setChars((prev) => (prev.includes(c) ? prev.filter((x) => x !== c) : [...prev, c]));
// //   };

// //   const submit = async (e) => {
// //     e.preventDefault();

// //     // Simple client-side validations
// //     if (prompt.trim().split(/\s+/).length > 20) {
// //       setError("Prompt max 20 words.");
// //       return;
// //     }
// //     if (credits < 1) {
// //       setError("No credits left.");
// //       return;
// //     }

// //     setError("");
// //     setStage("waiting");
// //     setVideoUrl(null);
// //     setJobId(null);

// //     try {
// //       // 1) Firebase auth (assumes user is signed in)
// //       const user = getAuth().currentUser;
// //       if (!user) {
// //         throw new Error("You must be signed in to generate a video.");
// //       }
// //       const token = await user.getIdToken();

// //       // 2) Kick off backend job
// //       const API_BASE = import.meta.env.VITE_API_BASE;
// //       if (!API_BASE) throw new Error("VITE_API_BASE is not set.");

// //       console.log("🌍 API_BASE:", API_BASE);

// //       const startData = await fetchJSON(`${API_BASE}/generate-video`, {
// //         method: "POST",
// //         headers: {
// //           "Content-Type": "application/json",
// //           Authorization: `Bearer ${token}`,
// //         },
// //         body: JSON.stringify({
// //           topic: prompt,
// //           characters: chars,
// //           song,
// //           type: "spongebob",
// //         }),
// //       });

// //       const newJobId = startData.jobId;
// //       setJobId(newJobId);
// //       console.log("🎬 Job ID:", newJobId);

// //       // 3) Poll job status until done/failed
// //       let attempts = 0;
// //       const MAX_ATTEMPTS = 120; // up to ~10 min at 5s interval

// //       while (attempts < MAX_ATTEMPTS) {
// //         attempts += 1;
// //         await sleep(5000);

// //         // If component unmounted, stop
// //         if (!isMounted.current) return;

// //         try {
// //           const status = await fetchJSON(
// //             `${API_BASE}/job-status/${newJobId}?_ngrok_skip_browser_warning=true`
// //           );
// //           console.log("🔁 Job status:", status);

// //           if (status.status === "done") {
// //             // Prefer server-provided video_url; append ngrok param if tunneling
// //             const path = status.video_url || `/videos/${newJobId}.mp4`;
// //             const src = `${API_BASE}${path}${
// //               path.includes("?") ? "&" : "?"
// //             }_ngrok_skip_browser_warning=true`;

// //             // Deduct credit if available
// //             try {
// //               if (typeof maybeDeductCredit === "function") {
// //                 await maybeDeductCredit();
// //               }
// //             } catch (e) {
// //               console.warn("Credit deduction failed (non-fatal):", e);
// //             }

// //             setVideoUrl(src);
// //             setStage("done");
// //             return;
// //           }

// //           if (status.status === "failed") {
// //             throw new Error(status.error || "Generation failed.");
// //           }

// //           // else still running; continue loop
// //         } catch (pollErr) {
// //           console.error("🛑 Polling error:", pollErr);
// //           setError("Lost connection while checking job status. Try again.");
// //           setStage("idle");
// //           return;
// //         }
// //       }

// //       // Timeout
// //       setError("Generation is taking too long. Please try again later.");
// //       setStage("idle");
// //     } catch (err) {
// //       console.error("💥 Error starting job:", err);
// //       setError(err.message || "Error connecting to backend.");
// //       setStage("idle");
// //     }
// //   };

// //   return (
// //     <div className="card">
// //       <h2>Create Explainer Video</h2>
// //       <p>Type a topic (max 20 words), choose characters and background music.</p>

// //       <form onSubmit={submit} className="form">
// //         <div className="field">
// //           <label>Topic prompt</label>
// //           <input
// //             placeholder="e.g., Explain compound interest simply"
// //             value={prompt}
// //             onChange={(e) => setPrompt(e.target.value)}
// //             required
// //           />
// //         </div>

// //         <div className="field">
// //           <label>Characters</label>
// //           <div className="checkbox-group">
// //             {CHARACTERS.map((c) => (
// //               <label key={c} className="checkbox-label">
// //                 <input
// //                   type="checkbox"
// //                   checked={chars.includes(c)}
// //                   onChange={() => toggleChar(c)}
// //                 />
// //                 {c}
// //               </label>
// //             ))}
// //           </div>
// //         </div>

// //         <div className="field">
// //           <label>Background song</label>
// //           <select value={song} onChange={(e) => setSong(e.target.value)}>
// //             {SONGS.map((s) => (
// //               <option key={s}>{s}</option>
// //             ))}
// //           </select>
// //         </div>

// //         <button type="submit" disabled={stage === "waiting"}>
// //           {stage === "waiting" ? "Generating..." : "Generate Video"}
// //         </button>

// //         {error && <div className="error" style={{ marginTop: 8 }}>{error}</div>}
// //       </form>

// //       {stage === "waiting" && <WaitingScreen />}

// //       {stage === "done" && videoUrl && (
// //         <div style={{ marginTop: 16 }}>
// //           <VideoPlayer src={videoUrl} prompt={prompt} characters={chars} song={song} />
// //           {jobId && (
// //             <div style={{ marginTop: 8, fontSize: 12, opacity: 0.8 }}>
// //               Job ID: <code>{jobId}</code>
// //             </div>
// //           )}
// //         </div>
// //       )}
// //     </div>
// //   );
// // }


// import { useState, useRef, useEffect } from "react";
// import WaitingScreen from "./WaitingScreen";
// import VideoPlayer from "./VideoPlayer";
// import { useAuth } from "./contexts/AuthContext";
// import { getAuth } from "firebase/auth";

// const CHARACTERS = ["Peter Griffin", "Stewie Griffin", "Brian Griffin", "Original Mascot"];
// const SONGS = ["Lo-fi Chill", "Upbeat Tech", "Cinematic Atmosphere", "None"];

// // Simple delay helper
// const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

// // Safe fetch that tries JSON but surfaces HTML/ngrok issues
// async function fetchJSON(url, options = {}) {
//   const res = await fetch(url, {
//     cache: "no-store",
//     headers: {
//       "ngrok-skip-browser-warning": "true",
//       Pragma: "no-cache",
//       "Cache-Control": "no-cache",
//       ...(options.headers || {}),
//     },
//     ...options,
//   });

//   const text = await res.text();
//   let data;
//   try {
//     data = JSON.parse(text);
//   } catch {
//     throw new Error(
//       `Non-JSON response from ${url} (HTTP ${res.status}). Body head: ${text.slice(0, 300)}...`
//     );
//   }
//   if (!res.ok) {
//     throw new Error(data?.error || `HTTP ${res.status}`);
//   }
//   return data;
// }

// export default function VideoCreator() {
//   const { credits, deductCredit: maybeDeductCredit } = useAuth();
//   const [prompt, setPrompt] = useState("");
//   const [chars, setChars] = useState([CHARACTERS[0]]);
//   const [song, setSong] = useState(SONGS[0]);
//   const [stage, setStage] = useState("idle"); // idle | waiting | done
//   const [videoUrl, setVideoUrl] = useState(null);
//   const [error, setError] = useState("");
//   const [jobId, setJobId] = useState(null);

//   const isMounted = useRef(true);
//   useEffect(() => {
//     return () => {
//       isMounted.current = false;
//     };
//   }, []);

//   const toggleChar = (c) => {
//     setChars((prev) => (prev.includes(c) ? prev.filter((x) => x !== c) : [...prev, c]));
//   };

//   const submit = async (e) => {
//     e.preventDefault();

//     if (prompt.trim().split(/\s+/).length > 20) {
//       setError("Prompt max 20 words.");
//       return;
//     }
//     if (credits < 1) {
//       setError("No credits left.");
//       return;
//     }

//     setError("");
//     setStage("waiting");
//     setVideoUrl(null);
//     setJobId(null);

//     try {
//       const user = getAuth().currentUser;
//       if (!user) {
//         throw new Error("You must be signed in to generate a video.");
//       }
//       const token = await user.getIdToken();

//       const API_BASE = import.meta.env.VITE_API_BASE;
//       if (!API_BASE) throw new Error("VITE_API_BASE is not set.");
//       console.log("🌍 API_BASE:", API_BASE);

//       const startData = await fetchJSON(`${API_BASE}/generate-video`, {
//         method: "POST",
//         headers: {
//           "Content-Type": "application/json",
//           Authorization: `Bearer ${token}`,
//         },
//         body: JSON.stringify({
//           topic: prompt,
//           characters: chars,
//           song,
//           type: "spongebob",
//         }),
//       });

//       const newJobId = startData.jobId;
//       setJobId(newJobId);
//       console.log("🎬 Job ID:", newJobId);

//       // Poll for completion
//       let attempts = 0;
//       const MAX_ATTEMPTS = 120;
//       let done = false;

//       while (!done && attempts < MAX_ATTEMPTS) {
//         attempts++;
//         await sleep(5000);
//         if (!isMounted.current) return;

//         try {
//           const url = `${API_BASE}/job-status/${newJobId}?_ngrok_skip_browser_warning=true`;
//           console.log("📡 Polling:", url);

//           const statusRes = await fetch(url, {
//             cache: "no-store",
//             headers: {
//               "ngrok-skip-browser-warning": "true",
//               Pragma: "no-cache",
//               "Cache-Control": "no-cache",
//             },
//           });

//           const raw = await statusRes.text();
//           console.log("📦 job-status raw:", statusRes.status, raw);

//           let statusData;
//           try {
//             statusData = JSON.parse(raw);
//           } catch {
//             throw new Error("Backend returned non-JSON (likely ngrok HTML).");
//           }

//           console.log("🔁 Parsed statusData:", statusData);

//           if (statusData.status === "done") {
//             const path = statusData.video_url || `/videos/${newJobId}.mp4`;
//             const src = `${API_BASE}${path}${
//               path.includes("?") ? "&" : "?"
//             }_ngrok_skip_browser_warning=true`;

//             try {
//               if (typeof maybeDeductCredit === "function") {
//                 await maybeDeductCredit();
//               }
//             } catch (e) {
//               console.warn("Credit deduction failed (non-fatal):", e);
//             }

//             setVideoUrl(src);
//             setStage("done");
//             done = true;
//           } else if (statusData.status === "failed") {
//             setError(statusData.error || "Generation failed.");
//             setStage("idle");
//             done = true;
//           }
//         } catch (pollErr) {
//           console.error("🛑 Polling failed:", pollErr);
//           setError("Lost connection to backend while checking job status.");
//           setStage("idle");
//           done = true;
//         }
//       }

//       if (!done) {
//         setError("Generation is taking too long. Please try again later.");
//         setStage("idle");
//       }
//     } catch (err) {
//       console.error("💥 Error starting job:", err);
//       setError(err.message || "Error connecting to backend.");
//       setStage("idle");
//     }
//   };

//   return (
//     <div className="card">
//       <h2>Create Explainer Video</h2>
//       <p>Type a topic (max 20 words), choose characters and background music.</p>

//       <form onSubmit={submit} className="form">
//         <div className="field">
//           <label>Topic prompt</label>
//           <input
//             placeholder="e.g., Explain compound interest simply"
//             value={prompt}
//             onChange={(e) => setPrompt(e.target.value)}
//             required
//           />
//         </div>

//         <div className="field">
//           <label>Characters</label>
//           <div className="checkbox-group">
//             {CHARACTERS.map((c) => (
//               <label key={c} className="checkbox-label">
//                 <input
//                   type="checkbox"
//                   checked={chars.includes(c)}
//                   onChange={() => toggleChar(c)}
//                 />
//                 {c}
//               </label>
//             ))}
//           </div>
//         </div>

//         <div className="field">
//           <label>Background song</label>
//           <select value={song} onChange={(e) => setSong(e.target.value)}>
//             {SONGS.map((s) => (
//               <option key={s}>{s}</option>
//             ))}
//           </select>
//         </div>

//         <button type="submit" disabled={stage === "waiting"}>
//           {stage === "waiting" ? "Generating..." : "Generate Video"}
//         </button>

//         {error && <div className="error" style={{ marginTop: 8 }}>{error}</div>}
//       </form>

//       {stage === "waiting" && <WaitingScreen />}

//       {stage === "done" && videoUrl && (
//         <div style={{ marginTop: 16 }}>
//           <VideoPlayer src={videoUrl} prompt={prompt} characters={chars} song={song} />
//           {jobId && (
//             <div style={{ marginTop: 8, fontSize: 12, opacity: 0.8 }}>
//               Job ID: <code>{jobId}</code>
//             </div>
//           )}
//         </div>
//       )}
//     </div>
//   );
// }
import { useState, useRef, useEffect } from "react";
import WaitingScreen from "./WaitingScreen";
import VideoPlayer from "./VideoPlayer";
import { useAuth } from "./contexts/AuthContext";
import { getAuth } from "firebase/auth";

const CHARACTERS = ["Peter Griffin", "Stewie Griffin", "Brian Griffin", "Original Mascot"];
const SONGS = ["Lo-fi Chill", "Upbeat Tech", "Cinematic Atmosphere", "None"];

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

async function fetchJSON(url, options = {}) {
  console.log("🌐 fetchJSON called:", url);
  const res = await fetch(url, {
    cache: "no-store",
    headers: {
      "ngrok-skip-browser-warning": "true",
      Pragma: "no-cache",
      "Cache-Control": "no-cache",
      ...(options.headers || {}),
    },
    ...options,
  });

  const text = await res.text();
  console.log("📦 Raw fetchJSON response text:", text);

  let data;
  try {
    data = JSON.parse(text);
  } catch {
    throw new Error(`❌ Non-JSON from ${url} (HTTP ${res.status})`);
  }

  if (!res.ok) {
    throw new Error(data?.error || `HTTP ${res.status}`);
  }

  return data;
}

export default function VideoCreator() {
  console.log("🎯 Rendering VideoCreator component");

  const { credits, deductCredit: maybeDeductCredit } = useAuth();
  const [prompt, setPrompt] = useState("");
  const [chars, setChars] = useState([CHARACTERS[0]]);
  const [song, setSong] = useState(SONGS[0]);
  const [stage, setStage] = useState("idle");
  const [videoUrl, setVideoUrl] = useState(null);
  const [error, setError] = useState("");
  const [jobId, setJobId] = useState(null);

  const isMounted = useRef(true);
  useEffect(() => {
    return () => {
      isMounted.current = false;
    };
  }, []);

  const toggleChar = (c) => {
    setChars((prev) => (prev.includes(c) ? prev.filter((x) => x !== c) : [...prev, c]));
  };

  const submit = async (e) => {
    e.preventDefault();
    console.log("📝 Submit clicked");

    if (prompt.trim().split(/\s+/).length > 20) {
      console.warn("⚠️ Prompt too long");
      setError("Prompt max 20 words.");
      return;
    }
    if (credits < 1) {
      console.warn("⚠️ No credits");
      setError("No credits left.");
      return;
    }

    setError("");
    setStage("waiting");
    setVideoUrl(null);
    setJobId(null);

    try {
      const user = getAuth().currentUser;
      if (!user) {
        throw new Error("You must be signed in to generate a video.");
      }
      const token = await user.getIdToken();

      const API_BASE = import.meta.env.VITE_API_BASE;
      if (!API_BASE) throw new Error("VITE_API_BASE is not set.");
      console.log("🌍 API_BASE:", API_BASE);

      console.log("🚀 Sending POST /generate-video");
      const startData = await fetchJSON(`${API_BASE}/generate-video`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          topic: prompt,
          characters: chars,
          song,
          type: "spongebob",
        }),
      });

      console.log("✅ POST /generate-video returned:", startData);

      const newJobId = startData.jobId;
      setJobId(newJobId);
      console.log("🎬 Job ID:", newJobId);

      console.log("➡ Entering polling loop");
      let attempts = 0;
      const MAX_ATTEMPTS = 120;
      let done = false;

      while (!done && attempts < MAX_ATTEMPTS) {
        attempts++;
        console.log(`⏳ Poll attempt ${attempts}`);
        await sleep(5000);
        if (!isMounted.current) {
          console.warn("⛔ Component unmounted, stopping poll loop");
          return;
        }

        try {
          const url = `${API_BASE}/job-status/${newJobId}?_ngrok_skip_browser_warning=true&t=${Date.now()}`;
          console.log("📡 Polling URL:", url);

          const status = await fetchJSON(url);
          console.log("🔁 Job status JSON:", status);

          if (status.status === "done") {
            console.log("🎉 Job completed, video URL:", status.video_url);
            const path = status.video_url || `/videos/${newJobId}.mp4`;
            const src = `${API_BASE}${path}${path.includes("?") ? "&" : "?"}_ngrok_skip_browser_warning=true`;

            try {
              if (typeof maybeDeductCredit === "function") {
                await maybeDeductCredit();
              }
            } catch (e) {
              console.warn("⚠️ Credit deduction failed (non-fatal):", e);
            }

            setVideoUrl(src);
            setStage("done");
            done = true;
          } else if (status.status === "failed") {
            console.error("❌ Job failed:", status.error);
            setError(status.error || "Generation failed.");
            setStage("idle");
            done = true;
          }
        } catch (pollErr) {
          console.error("🛑 Polling error:", pollErr);
          setError("Lost connection to backend while checking job status.");
          setStage("idle");
          done = true;
        }
      }

      if (!done) {
        console.error("⏱️ Polling timed out");
        setError("Generation is taking too long. Please try again later.");
        setStage("idle");
      }
    } catch (err) {
      console.error("💥 Error starting job:", err);
      setError(err.message || "Error connecting to backend.");
      setStage("idle");
    }
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
          {stage === "waiting" ? "Generating..." : "Generate Video"}
        </button>

        {error && <div className="error" style={{ marginTop: 8 }}>{error}</div>}
      </form>

      {stage === "waiting" && <WaitingScreen />}

      {stage === "done" && videoUrl && (
        <div style={{ marginTop: 16 }}>
          <VideoPlayer src={videoUrl} prompt={prompt} characters={chars} song={song} />
          {jobId && (
            <div style={{ marginTop: 8, fontSize: 12, opacity: 0.8 }}>
              Job ID: <code>{jobId}</code>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
