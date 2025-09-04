import React, { useState } from "react";
import axios from "axios";

export default function AuthForm({ setUser }) {
  const [mode, setMode] = useState("login");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (mode === "login") {
        const res = await axios.post(
          "http://127.0.0.1:8000/auth/login",
          new URLSearchParams({ username: email, password }),
          { withCredentials: true }
        );
        // сохраним токен и email
        setUser({
          email,
          accessToken: res.data.access_token,
        });
        setMessage("");
      } else {
        await axios.post("http://127.0.0.1:8000/auth/register", {
          email,
          password,
        });
        setMessage("Регистрация успешна! Теперь войдите.");
        setMode("login");
      }
    } catch (err) {
      setMessage("Ошибка: неправильные данные или регистрация не удалась.");
      console.error(err);
    }
  };

  return (
    <div style={{ maxWidth: 400, margin: "0 auto", padding: 20 }}>
      <h2>{mode === "login" ? "Вход" : "Регистрация"}</h2>
      {message && <p style={{ color: "red" }}>{message}</p>}
      <form onSubmit={handleSubmit} style={{ display: "flex", flexDirection: "column", gap: 10 }}>
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
        <input
          type="password"
          placeholder="Пароль"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
        <button type="submit">{mode === "login" ? "Войти" : "Зарегистрироваться"}</button>
      </form>
      <button onClick={() => setMode(mode === "login" ? "register" : "login")} style={{ marginTop: 10 }}>
        {mode === "login" ? "Перейти к регистрации" : "Перейти к логину"}
      </button>
    </div>
  );
}