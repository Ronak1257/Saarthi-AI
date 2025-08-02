import { useState } from "react";
import API from "../api";

export default function Signup({ onRegister }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const register = async () => {
    alert("Registered! Please login.");
    await API.post("/register", { email, password });
    onRegister();
  };

  return (
    <div className="p-4 max-w-sm mx-auto">
      <h2 className="text-xl font-bold mb-4">Signup</h2>
      <input value={email} onChange={e => setEmail(e.target.value)} placeholder="Email" className="border p-2 w-full mb-2"/>
      <input value={password} onChange={e => setPassword(e.target.value)} type="password" placeholder="Password" className="border p-2 w-full mb-2"/>
      <button onClick={register} className="bg-blue-500 text-white p-2 w-full">Register</button>
    </div>
  );
}
