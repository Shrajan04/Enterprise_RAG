import { useEffect, useState } from "react";
import api from "./api";

export default function Documents() {
  const [docs, setDocs] = useState([]);
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);

  const load = async () => {
    const res = await api.get("/documents/");
    setDocs(res.data);
  };

  useEffect(() => {
    load();
  }, []);

  const upload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;
    setError("");
    setBusy(true);
    const form = new FormData();
    form.append("file", file);
    try {
      await api.post("/documents/upload", form);
      await load();
    } catch (err) {
      setError(err.response?.data?.detail || "Upload failed");
    }
    setBusy(false);
    e.target.value = "";
  };

  const remove = async (id) => {
    await api.delete(`/documents/${id}`);
    await load();
  };

  return (
    <section className="panel">
      <h2>Library</h2>
      <label className="upload">
        {busy ? "Processing..." : "Upload a PDF"}
        <input type="file" accept=".pdf" onChange={upload} disabled={busy} />
      </label>
      {error && <p className="error">{error}</p>}
      {docs.length === 0 && <p className="empty">No documents yet.</p>}
      <ul className="doclist">
        {docs.map((d) => (
          <li key={d.id}>
            <span className="name" title={d.filename}>{d.filename}</span>
            <button className="link" onClick={() => remove(d.id)}>Remove</button>
          </li>
        ))}
      </ul>
    </section>
  );
}