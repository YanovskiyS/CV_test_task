import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:8000", // URL твоего FastAPI
  withCredentials: true, // чтобы передавались куки
});

export const registerUser = (data) => api.post("/auth/register", data);
export const loginUser = (data) => api.post("/auth/login", data);
export const getResumes = () => api.get("/resumes/me");
export const addResume = (data) => api.post("/resumes", data);
export const improveResume = (id) => api.post(`/resumes/${id}/improve`);
export const logoutUser = () => api.post("/auth/logout");