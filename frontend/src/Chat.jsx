import { useState, useRef, useEffect } from "react";
import ReactMarkdown from "react-markdown";
import api from "./api";

export default function Chat() {
  const [query, setQuery] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const bottom = useRef(null);

  useEffect(() => {
    bottom.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

    const ask = async (e) => {
    e.preventDefault();
    const question = query.trim();
    if (!question || loading) return;

    // last 6 messages from BEFORE this question, sent as history
    const history = messages.slice(-6).map((m) => ({
      role: m.role === "user" ? "user" : "assistant",
      text: m.text,
    }));

    setQuery("");
    setLoading(true);
    setMessages((m) => [...m, { role: "user", text: question }]);
    try {
      const res = await api.get("/chat/search", {
        params: { query: question, history: JSON.stringify(history) },
      });
      setMessages((m) => [...m, { role: "bot", text: res.data.answer, sources: res.data.sources }]);
    } catch {
      setMessages((m) => [...m, { role: "bot", text: "Something went wrong. Please try again.", sources: [] }]);
    }
    setLoading(false);
  };
  return (
    <section className="panel">
      <h2>Ask your documents</h2>
      <div className="messages">
        {messages.length === 0 && (
          <p className="placeholder">Upload a document, then ask a question. Answers cite the file they came from.</p>
        )}
        {messages.map((m, i) => (
          <div key={i} className={`msg ${m.role}`}>
            <div className="who">{m.role === "user" ? "You" : "Answer"}</div>
            <div className="bubble">
              <ReactMarkdown>{m.text}</ReactMarkdown>
            </div>
            {m.sources && m.sources.length > 0 && (
              <div className="sources">
                {m.sources.map((s) => (
                  <span key={s.document_id}>{s.filename}</span>
                ))}
              </div>
            )}
          </div>
        ))}
        {loading && <p className="empty">Searching your documents...</p>}
        <div ref={bottom} />
      </div>
      <form className="askbar" onSubmit={ask}>
        <input type="text" placeholder="Ask a question" value={query} onChange={(e) => setQuery(e.target.value)} />
        <button type="submit" disabled={loading}>Ask</button>
      </form>
    </section>
  );
}