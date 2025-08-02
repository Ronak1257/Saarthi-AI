import { useState } from "react";
import API from "../api";

export default function Goals({ onSet }) {
  const [shortGoal, setShortGoal] = useState("");
  const [longGoal, setLongGoal] = useState("");

  const saveGoals = async () => {
    await API.post("/set-goals", {
      token: localStorage.getItem("token"),
      short_term_goal: shortGoal,
      long_term_goal: longGoal
    });
    onSet();
  };

  return (
    <div className="p-4 max-w-sm mx-auto">
      <h2 className="text-xl font-bold mb-4">Set Your Goals</h2>
      <input value={shortGoal} onChange={e => setShortGoal(e.target.value)} placeholder="Short Term Goal" className="border p-2 w-full mb-2"/>
      <input value={longGoal} onChange={e => setLongGoal(e.target.value)} placeholder="Long Term Goal" className="border p-2 w-full mb-2"/>
      <button onClick={saveGoals} className="bg-purple-500 text-white p-2 w-full">Save Goals</button>
    </div>
  );
}
