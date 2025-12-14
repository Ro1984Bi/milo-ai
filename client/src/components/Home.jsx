import { useEffect, useState } from "react";
import Navbar from "./Navbar";
import { FilePenLine, Trash2, Send, Loader } from "lucide-react";
import axios from "axios";

export default function Home() {
  const [prompts, setPrompts] = useState("");
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(false);
  const [isGroq, setIsGroq] = useState(true);
  const [isMistral, setIsMistral] = useState(false);
  const token = localStorage.getItem("token");

  const aiType = isMistral ? "mistral" : "groq";

  useEffect(() => {
    fetchPrompts();
  }, []);

  const fetchPrompts = async () => {
    try {
      const res = await axios.get(
        `${import.meta.env.VITE_BACKEND_URL}/api/${aiType}/prompts`,
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      );
      setHistory(res.data.items ?? res.data);
    } catch (error) {
      console.error("Error fetching prompts", error);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const res = await axios.post(
        `${import.meta.env.VITE_BACKEND_URL}/api/${aiType}/prompt`,
        { prompt: prompts },
        { headers: { Authorization: `Bearer ${token}` } }
      );

      setHistory((prev) => [...prev, res.data]);
      setPrompts("");
    } catch (error) {
      console.error("Error sending prompt", error);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id) => {
    try {
      await axios.delete(
        `${import.meta.env.VITE_BACKEND_URL}/api/${aiType}/prompt/${id}`,
        { headers: { Authorization: `Bearer ${token}` } }
      );

      setHistory((prev) => prev.filter((p) => p.id !== id));
    } catch (error) {
      console.error("Error deleting prompt", error);
    }
  };

  const handleUpdate = async (id, newPrompt) => {
    try {
      await axios.put(
        `${import.meta.env.VITE_BACKEND_URL}/api/${aiType}/prompt/${id}`,
        { prompt: newPrompt },
        { headers: { Authorization: `Bearer ${token}` } }
      );

      fetchPrompts();
    } catch (error) {
      console.error("Error updating prompt", error);
    }
  };

  function DisplayAndEditPrompt({ item, onDelete, onUpdate }) {
    const [isEditing, setIsEditing] = useState(false);
    const [editPrompt, setEditPrompt] = useState(item.prompt);

    return (
      <div className="border-b border-neutral-700 pb-4">
        {isEditing ? (
          <textarea
            className="textarea textarea-neutral textarea-xl w-full mb-2"
            value={editPrompt}
            onChange={(e) => setEditPrompt(e.target.value)}
          />
        ) : (
          <p className="text-white whitespace-pre-line">{item.prompt}</p>
        )}

        <div className="flex justify-end gap-2 mt-2">
          {isEditing ? (
            <>
              <button
                className="btn btn-success btn-sm"
                onClick={() => {
                  onUpdate(item.id, editPrompt);
                  setIsEditing(false);
                }}
              >
                Save
              </button>
              <button
                className="btn btn-ghost btn-sm"
                onClick={() => setIsEditing(false)}
              >
                Cancel
              </button>
            </>
          ) : (
            <>
              <FilePenLine
                className="cursor-pointer"
                onClick={() => setIsEditing(true)}
              />
              <Trash2
                className="cursor-pointer text-red-400"
                onClick={() => onDelete(item.id)}
              />
            </>
          )}
        </div>

        <p className="text-neutral-300 mt-3 whitespace-pre-line">
          {item.response}
        </p>
      </div>
    );
  }

  return (
    <div>
      <Navbar />
      <div className="min-h-screen flex flex-col items-center p-6">
        <h2 className="text-2xl font-bold text-white mb-4">
          Using {isMistral ? "Mistral AI" : "Groq AI"}
        </h2>

        <div className="w-full max-w-2xl space-y-4">
          {history.map((item) => (
            <DisplayAndEditPrompt
              key={item.id}
              item={item}
              onDelete={handleDelete}
              onUpdate={handleUpdate}
            />
          ))}
        </div>

        {loading && <Loader className="mt-6 animate-spin" />}

        <form onSubmit={handleSubmit} className="w-full max-w-2xl mt-8">
          <textarea
            rows={4}
            placeholder="Enter your prompt"
            value={prompts}
            onChange={(e) => setPrompts(e.target.value)}
            className="textarea textarea-neutral textarea-xl w-full"
          />

          <div className="flex justify-end gap-2 mt-2">
            <button
              type="button"
              className="btn btn-accent"
              onClick={() => {
                setIsGroq(true);
                setIsMistral(false);
              }}
            >
              Groq
            </button>

            <button
              type="button"
              className="btn btn-accent"
              onClick={() => {
                setIsGroq(false);
                setIsMistral(true);
              }}
            >
              Mistral
            </button>

            <button
              type="submit"
              disabled={!prompts.trim()}
              className="btn btn-primary"
            >
              <Send className="w-4 h-4" />
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
