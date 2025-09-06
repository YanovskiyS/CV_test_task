import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

export default function Resumes({ user }) {
  const [resumes, setResumes] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [title, setTitle] = useState("");
  const [content, setContent] = useState("");
  const navigate = useNavigate();

  const fetchResumes = async () => {
    setLoading(true);
    setError("");
    try {
      const res = await axios.get("http://127.0.0.1:7777/resumes/me", {
        headers: { Authorization: `Bearer ${user.accessToken}` },
        withCredentials: true,
      });
      setResumes(res.data);
    } catch (err) {
      setError("Ошибка при получении резюме");
      console.error(err);
    }
    setLoading(false);
  };

  const addResume = async (e) => {
    e.preventDefault();
    setError("");
    try {
      const res = await axios.post(
        "http://127.0.0.1:7777/resumes/",
        { title, content },
        {
          headers: { Authorization: `Bearer ${user.accessToken}` },
          withCredentials: true,
        }
      );
      setResumes((prev) => [...prev, res.data]);
      setTitle("");
      setContent("");
    } catch (err) {
      setError("Ошибка при добавлении резюме");
      console.error(err);
    }
  };

  return (
    <div style={{ maxWidth: 600, margin: "0 auto", padding: 20 }}>
      <h2>Мои резюме</h2>
      <button onClick={fetchResumes} style={{ marginBottom: 20 }}>
        Показать мои резюме
      </button>

      {loading && <p>Загрузка...</p>}
      {error && <p style={{ color: "red" }}>{error}</p>}

      <ul>
        {resumes.map((resume) => (
          <li key={resume.id} style={{ marginBottom: "16px" }}>
            {/* Клик по заголовку открывает отдельную страницу */}
            <h3
              style={{ cursor: "pointer", color: "blue" }}
              onClick={() => navigate(`/resume/${resume.id}`)}
            >
              {resume.title}
            </h3>

          </li>
        ))}
      </ul>

      <hr style={{ margin: "24px 0" }} />

      <h3>Добавить новое резюме</h3>
      <form onSubmit={addResume} style={{ display: "flex", flexDirection: "column", gap: 10 }}>
        <input
          type="text"
          placeholder="Название (title)"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          required
        />
        <textarea
          placeholder="Содержание (content)"
          value={content}
          onChange={(e) => setContent(e.target.value)}
          rows={4}
          required
        />
        <button type="submit">Добавить</button>
      </form>
    </div>
  );
}