import { useState, useEffect } from "react";
import API from "../api";

export default function Chat() {
  const [message, setMessage] = useState("");
  const [history, setHistory] = useState([]);
  const [page, setPage] = useState(1);

  const fetchHistory = async (pageNum) => {
    const res = await API.get(`/history?token=${localStorage.getItem("token")}&page=${pageNum}&limit=10`);
    setHistory(res.data.history);
    setPage(pageNum);
  };

  const sendMessage = async () => {
    const res = await API.post("/chat", {
      token: localStorage.getItem("token"),
      message
    });
    setMessage("");
    fetchHistory(page);
  };

  useEffect(() => {
    fetchHistory(1);
  }, []);

  return (
    <div className="p-4 max-w-xl mx-auto">
      <h2 className="text-xl font-bold mb-4">Chat</h2>
      <div className="border p-4 h-80 overflow-y-auto bg-gray-50">
        {history.map((h, idx) => (
          <div key={idx} className="mb-3">
            <p className="font-semibold">You: {h.message}</p>
            <p className="text-gray-700">AI: {h.reply}</p>
          </div>
        ))}
      </div>
      <div className="mt-4 flex">
        <input value={message} onChange={e => setMessage(e.target.value)} placeholder="Type a message..." className="border p-2 flex-1"/>
        <button onClick={sendMessage} className="bg-blue-500 text-white p-2 ml-2">Send</button>
      </div>
      <div className="mt-4 flex justify-between">
        <button disabled={page === 1} onClick={() => fetchHistory(page - 1)} className="bg-gray-300 px-4 py-1 rounded">Prev</button>
        <button onClick={() => fetchHistory(page + 1)} className="bg-gray-300 px-4 py-1 rounded">Next</button>
      </div>
    </div>
  );
}
