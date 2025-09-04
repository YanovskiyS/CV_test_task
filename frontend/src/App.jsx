import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import AuthForm from "./components/AuthForm.jsx";
import Resumes from "./components/Resume.jsx";
import ResumeDetail from "./components/ResumeDetail.jsx";
import React from "react";

function App() {
  const [user, setUser] = React.useState(null);

  return (
    <Router>
      <Routes>
        <Route
          path="/"
          element={user ? <Navigate to="/resumes" /> : <AuthForm setUser={setUser} />}
        />
        <Route
          path="/resumes"
          element={user ? <Resumes user={user} /> : <Navigate to="/" />}
        />
        <Route
          path="/resume/:id"
          element={user ? <ResumeDetail user={user} /> : <Navigate to="/" />}
        />
      </Routes>
    </Router>
  );
}

export default App;
