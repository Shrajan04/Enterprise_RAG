import { useState } from "react";
import Login from "./Login";
import Documents from "./Documents";
import Chat from "./Chat";

export default function App() {
  const [loggedIn, setLoggedIn] = useState(!!localStorage.getItem("token"));

  const logout = () => {
    localStorage.removeItem("token");
    setLoggedIn(false);
  };

  if (!loggedIn) return <Login onLogin={() => setLoggedIn(true)} />;

  return (
    <div>
      <header className="topbar">
        <span className="brand">Enterprise Knowledge</span>
        <button onClick={logout}>Sign out</button>
      </header>
      <main className="layout">
        <Documents />
        <Chat />
      </main>
    </div>
  );
}   