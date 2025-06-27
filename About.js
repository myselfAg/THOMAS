import React from "react";
import Header from "./Header";
import { useNavigate } from "react-router-dom";

export default function About() {
  const navigate = useNavigate();

  const goToHome = () => {
    navigate("/");
  };

  return (
    <>
        <Header />
        <div className="btns">
          <button onClick={goToHome}>Home</button>
        </div>
    </>
  );
}
