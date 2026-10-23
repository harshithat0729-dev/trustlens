const LANGS = [
  { id: "tinglish", label: "Tinglish" },
  { id: "telugu", label: "Telugu" },
  { id: "hindi", label: "Hindi" },
  { id: "english", label: "English" },
];

export default function LanguageSelector({ value, onChange }) {
  return (
    <div className="lang">
      <span className="lang-label">Explanation language</span>
      <div className="lang-row">
        {LANGS.map((l) => (
          <button
            key={l.id}
            className={value === l.id ? "chip active" : "chip"}
            onClick={() => onChange(l.id)}
          >
            {l.label}
          </button>
        ))}
      </div>
    </div>
  );
}
