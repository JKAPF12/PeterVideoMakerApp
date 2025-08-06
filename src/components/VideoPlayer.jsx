export default function VideoPlayer({ src, prompt, characters, song }) {
  return (
    <div className="result">
      <h3>Here’s your video</h3>
      <div className="meta">
        <div><strong>Prompt:</strong> {prompt}</div>
        <div><strong>Characters:</strong> {characters.join(", ")}</div>
        <div><strong>Song:</strong> {song}</div>
      </div>
      <video controls width="100%" src={src} />
      <div className="actions">
        <button onClick={() => alert("Post placeholder")}>Post</button>
        <button onClick={() => alert("Download placeholder")}>Download</button>
      </div>
    </div>
  );
}
