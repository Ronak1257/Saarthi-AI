// src/pages/Landing.jsx
import { Link } from "react-router-dom";

export default function Landing() {
  return (
    <div className="min-h-screen flex flex-col bg-gradient-to-br from-indigo-600 to-purple-700 text-white">
      <header className="flex justify-between p-6">
        <h1 className="text-2xl font-bold">Saarthi AI</h1>
        <div>
          <Link to="/login" className="px-4 py-2 bg-white text-indigo-600 rounded mr-2">Login</Link>
          <Link to="/signup" className="px-4 py-2 bg-indigo-500 border border-white rounded">Sign Up</Link>
        </div>
      </header>

      <main className="flex flex-col items-center justify-center flex-grow text-center px-4">
        <h2 className="text-4xl font-bold mb-4">Your AI Life Companion</h2>
        <p className="max-w-2xl mb-6">
          Saarthi AI remembers your goals, tracks your progress, and guides you using wisdom from the Bhagavad Gita, Ramayan, and modern productivity methods.
        </p>
        <Link to="/signup" className="px-6 py-3 bg-white text-indigo-600 font-semibold rounded shadow-lg hover:shadow-xl transition">
          Start Your Journey
        </Link>
      </main>

      <footer className="text-center p-4 text-sm">
        © {new Date().getFullYear()} Saarthi AI. All rights reserved.
      </footer>
    </div>
  );
}
