import { useState } from "react";
import API from "../api";

export default function Login({ onLogin }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const login = async () => {
    const res = await API.post("/login", { email, password });
    localStorage.setItem("token", res.data.access_token);
    onLogin();
  };

  return (
    <div className="p-4 max-w-sm mx-auto">
      <h2 className="text-xl font-bold mb-4">Login</h2>
      <input value={email} onChange={e => setEmail(e.target.value)} placeholder="Email" className="border p-2 w-full mb-2"/>
      <input value={password} onChange={e => setPassword(e.target.value)} type="password" placeholder="Password" className="border p-2 w-full mb-2"/>
      <button onClick={login} className="bg-green-500 text-white p-2 w-full">Login</button>
    </div>
  );
}
