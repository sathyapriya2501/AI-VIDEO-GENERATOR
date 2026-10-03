import { useState } from "react";

function App() {
  const [prompt, setPrompt] = useState("");
  const [scene, setScene] = useState(null);
  const [loading, setLoading] = useState(false);
  const [audioLoading, setAudioLoading] = useState(false);
  const [videoLoading, setVideoLoading] = useState(false);

  const [audioGenerated, setAudioGenerated] = useState(false);
  const [videoGenerated, setVideoGenerated] = useState(false);

  const [error, setError] = useState("");

  // ------------------------------------------
  // Generate Scene
  // ------------------------------------------

  const generateScene = async () => {
    if (!prompt.trim()) {
      setError("Please enter a video prompt.");
      return;
    }

    setLoading(true);
    setError("");
    setScene(null);
    setAudioGenerated(false);
    setVideoGenerated(false);

    try {
      const response = await fetch(
        "http://127.0.0.1:5000/plan-scene",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            prompt: prompt,
          }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || "Something went wrong");
      }

      setScene(data.scene);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  // ------------------------------------------
  // Generate Voice
  // ------------------------------------------

  const generateVoice = async () => {
    if (!scene) return;

    setAudioLoading(true);
    setError("");

    try {
      const response = await fetch(
        "http://127.0.0.1:5000/generate-audio",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            script: scene.script,
            voice: scene.voice,
          }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || "Audio generation failed");
      }

      setAudioGenerated(true);
    } catch (err) {
      setError(err.message);
    } finally {
      setAudioLoading(false);
    }
  };

  // ------------------------------------------
  // Generate Video
  // ------------------------------------------

  const generateVideo = async () => {
    setVideoLoading(true);
    setError("");

    try {
      // Current scene_composer already creates this file
      const response = await fetch(
        "http://127.0.0.1:5000/video/scene_zoom.mp4",
        {
          method: "HEAD",
        }
      );

      if (!response.ok) {
        throw new Error(
          "Video not found. Please run scene_composer.py first."
        );
      }

      setVideoGenerated(true);
    } catch (err) {
      setError(err.message);
    } finally {
      setVideoLoading(false);
    }
  };

  return (
    <div style={{ padding: "30px" }}>
      <h1>AI Video Generator</h1>

      {/* Prompt */}
      <textarea
        rows="5"
        cols="60"
        placeholder="Describe the video you want..."
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
      />

      <br />
      <br />

      <button onClick={generateScene} disabled={loading}>
        {loading ? "Generating..." : "Generate Scene"}
      </button>

      {/* Error */}
      {error && (
        <p>
          <strong>Error:</strong> {error}
        </p>
      )}

      {/* Scene */}
      {scene && (
        <div>
          <h2>Scene Plan</h2>

          <p>
            <strong>Duration:</strong> {scene.duration} seconds
          </p>

          <p>
            <strong>Language:</strong> {scene.language}
          </p>

          <p>
            <strong>Script:</strong> {scene.script}
          </p>

          <p>
            <strong>Character:</strong> {scene.character}
          </p>

          <p>
            <strong>Background:</strong> {scene.background}
          </p>

          <p>
            <strong>Action:</strong> {scene.action}
          </p>

          <p>
            <strong>Expression:</strong> {scene.expression}
          </p>

          <p>
            <strong>Props:</strong> {scene.props.join(", ")}
          </p>

          <p>
            <strong>Camera:</strong> {scene.camera}
          </p>

          <p>
            <strong>Voice:</strong> {scene.voice.gender} -{" "}
            {scene.voice.language}
          </p>

          <br />

          {/* Generate Voice */}
          <button
            onClick={generateVoice}
            disabled={audioLoading}
          >
            {audioLoading ? "Generating Voice..." : "Generate Voice"}
          </button>

          {/* Audio */}
          {audioGenerated && (
            <div style={{ marginTop: "15px" }}>
              <p>
                <strong>Generated Voice:</strong>
              </p>

              <audio controls>
                <source
                  src="http://127.0.0.1:5000/video/scene_audio.mp3"
                  type="audio/mpeg"
                />
              </audio>
            </div>
          )}

          <br />
          <br />

          {/* Generate Video */}
          <button
            onClick={generateVideo}
            disabled={videoLoading}
          >
            {videoLoading ? "Loading Video..." : "Generate Video"}
          </button>

          {/* Video */}
          {videoGenerated && (
            <div style={{ marginTop: "20px" }}>
              <h2>Generated Video</h2>

              <video
                width="800"
                controls
              >
                <source
                  src="http://127.0.0.1:5000/video/scene_zoom.mp4"
                  type="video/mp4"
                />
                Your browser does not support video playback.
              </video>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default App;
