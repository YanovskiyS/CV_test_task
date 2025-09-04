import { useState } from "react";
import axios from "axios";

export default function AddResume({ onAdded }) {
  const [title, setTitle] = useState("");
  const [content, setContent] = useState("");

  const addResume = async (e) => {
    e.preventDefault();
    try {
      await axios.post(
        "http://localhost:8000/resumes",
        { title, content },
        { withCredentials: true }
      );
      setTitle("");
      setContent("");
      if (onAdded) onAdded();
    } catch (err) {
      console.error(err);
      alert("Ошибка при добавлении резюме");
    }
  };

  return (
    <form onSubmit={addResume}>
      <input
        type="text"
        placeholder="Название"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        required
      />
      <textarea
        placeholder="Контент"
        value={content}
        onChange={(e) => setContent(e.target.value)}
      />
      <button type="submit">Добавить резюме</button>
    </form>
  );
}