import { useState } from "react";
import LanguageSelector from "./LanguageSelector.jsx";
import { checkLink, checkMessage, checkClaim, checkMedia } from "../api.js";

const MODES = [
  { id: "link", label: "Check Link" },
  { id: "message", label: "Check Message" },
  { id: "media", label: "Photo / Video" },
  { id: "claim", label: "Check a Claim" },
];

export default function Home({ language, setLanguage, onResult }) {
  const [mode, setMode] = useState("link");
  const [text, setText] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");

  async function run() {
    setError("");
    setBusy(true);
    try {
      let res;
      if (mode === "link") res = await checkLink(text, language);
      else if (mode === "message") res = await checkMessage(text, language);
      else if (mode === "claim") res = await checkClaim(text, language);
      onResult(res);
    } catch (e) {
      setError(e.message);
    } finally {
      setBusy(false);
    }
  }

  async function onFile(e) {
    const file = e.target.files?.[0];
    if (!file) return;
    setBusy(true);
    setError("");
    try {
      onResult(await checkMedia(file, language));
    } catch (err) {
      setError(err.message);
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="home">
      <h1>TrustLens</h1>
      <p className="tagline">Before you trust it, check it.</p>
      <p className="prompt">Emaina suspicious ga undha? Content ni paste cheyyi or upload cheyyi.</p>

      <div className="modes">
        {MODES.map((m) => (
          <button key={m.id} className={mode === m.id ? "mode active" : "mode"}
                  onClick={() => setMode(m.id)}>
            {m.label}
          </button>
        ))}
      </div>

      {mode === "media" ? (
        <input type="file" accept="image/*" onChange={onFile} />
      ) : (
        <>
          <textarea
            rows={5}
            placeholder={mode === "link" ? "https://..." : "Paste the message or claim here..."}
            value={text}
            onChange={(e) => setText(e.target.value)}
          />
          <button className="primary" disabled={busy || !text.trim()} onClick={run}>
            {busy ? "Checking..." : "Check"}
          </button>
        </>
      )}

      <LanguageSelector value={language} onChange={setLanguage} />
      {error && <p className="error">{error}</p>}
    </div>
  );
}
