const LABELS = {
  high_risk: { text: "High risk", cls: "risk-high" },
  suspicious_signals_found: { text: "Suspicious signals found", cls: "risk-susp" },
  no_known_warning_found: { text: "No known warning found", cls: "risk-ok" },
  inconclusive: { text: "Inconclusive", cls: "risk-inc" },
};

export default function ResultCard({ result, onBack }) {
  const meta = LABELS[result.risk_label] || LABELS.inconclusive;
  return (
    <div className="card">
      <button className="back" onClick={onBack}>← Check something else</button>
      <div className={`badge ${meta.cls}`}>{meta.text}</div>
      <p className="summary">{result.summary}</p>

      <h4>Signals</h4>
      <ul className="signals">
        {result.signals.map((s, i) => (
          <li key={i} className={s.result}>
            <b>{s.name}</b> — {s.result}
            {s.detail ? `: ${s.detail}` : ""}
          </li>
        ))}
      </ul>

      {result.sources?.length > 0 && (
        <>
          <h4>Sources</h4>
          <ul>{result.sources.map((s, i) => <li key={i}><a href={s}>{s}</a></li>)}</ul>
        </>
      )}

      {result.limitations?.length > 0 && (
        <>
          <h4>Limitations</h4>
          <ul>{result.limitations.map((s, i) => <li key={i}>{s}</li>)}</ul>
        </>
      )}

      {result.safe_next_steps?.length > 0 && (
        <>
          <h4>Safe next steps</h4>
          <ul>{result.safe_next_steps.map((s, i) => <li key={i}>{s}</li>)}</ul>
        </>
      )}

      <details>
        <summary>Why this result? (technical)</summary>
        <p>Checks run: {result.checks_run.join(", ") || "none"}</p>
        <p>Checks unavailable: {result.checks_unavailable.join(", ") || "none"}</p>
      </details>
    </div>
  );
}
