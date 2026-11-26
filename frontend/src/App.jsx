import { useState } from "react";
import Login from "./Login";

export default function App() {
  const [loggedIn, setLoggedIn] = useState(!!localStorage.getItem("token"));
  return loggedIn ? <h1>Logged in</h1> : <Login onLogin={() => setLoggedIn(true)} />;
}