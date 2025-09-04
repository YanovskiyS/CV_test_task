import React, { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import axios from "axios";

export default function ResumeDetail({ user }) {
  const { id } = useParams();
  const navigate = useNavigate();
  const [resume, setResume] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchResume = async () => {
      try {
        const res = await axios.get(`http://127.0.0.1:8000/resumes/${id}`, {
          headers: { Authorization: `Bearer ${user.accessToken}` },
          withCredentials: true,
        });
        setResume(res.data);
      } catch (err) {
        setError("Ошибка при получении резюме");
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchResume();
  }, [id, user]);

  const improveResume = async () => {
    try {
      const res = await axios.patch(
        `http://127.0.0.1:8000/resumes/${id}/improve`,
        {},
        {
          headers: { Authorization: `Bearer ${user.accessToken}` },
          withCredentials: true,
        }
      );
      setResume({ ...resume, content: res.data });
    } catch (err) {
      console.error(err);
    }
  };

  if (loading) return <p>Загрузка...</p>;
  if (error) return <p style={{ color: "red" }}>{error}</p>;
  if (!resume) return <p>Резюме не найдено</p>;

  return (
    <div style={{ maxWidth: 600, margin: "0 auto", padding: 20 }}>
      <h2 onClick={improveResume} style={{ cursor: "pointer" }}>{resume.title}</h2>
      <p>{resume.content}</p>
      <button onClick={improveResume}>Улучшить</button>
      <button onClick={() => navigate("/resumes")} style={{ marginTop: 10 }}>
        Назад к списку
      </button>
    </div>
  );
}