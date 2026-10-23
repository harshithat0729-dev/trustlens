import { useState } from "react";
import Home from "./components/Home.jsx";
import ResultCard from "./components/ResultCard.jsx";

export default function App() {
  const [language, setLanguage] = useState("tinglish");
  const [result, setResult] = useState(null);

  return (
    <div className="app">
      {result ? (
        <ResultCard result={result} onBack={() => setResult(null)} />
      ) : (
        <Home language={language} setLanguage={setLanguage} onResult={setResult} />
      )}
      <footer className="foot">
        TrustLens is a prototype. It never claims 100% real/fake — when evidence is
        not enough it says <b>Inconclusive</b>.
      </footer>
    </div>
  );
}
