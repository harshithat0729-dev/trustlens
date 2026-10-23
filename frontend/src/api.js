const API = import.meta.env.VITE_API_URL || "http://localhost:8000";

async function post(path, body) {
  const res = await fetch(`${API}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  if (!res.ok) throw new Error((await res.json()).detail || "Request failed");
  return res.json();
}

export const checkLink = (url, language) => post("/api/check/link", { url, language });
export const checkMessage = (text, language) => post("/api/check/message", { text, language });
export const checkClaim = (text, language) => post("/api/check/claim", { text, language });

export async function checkMedia(file, language) {
  const form = new FormData();
  form.append("file", file);
  form.append("language", language);
  const res = await fetch(`${API}/api/check/media`, { method: "POST", body: form });
  if (!res.ok) throw new Error((await res.json()).detail || "Upload failed");
  return res.json();
}
