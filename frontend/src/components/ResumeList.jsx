import React from "react";
import { Link } from "react-router-dom";

export default function ResumeList({ resumes }) {
  return (
    <ul>
      {resumes.map((resume) => (
        <li key={resume.id}>
          <Link to={`/resumes/${resume.id}`}>
            <strong>{resume.title}</strong>
          </Link>
        </li>
      ))}
    </ul>
  );
}