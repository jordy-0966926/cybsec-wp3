"use client";
import React, { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { Button } from "../../components/ui/button";

export default function Prompts() {
  const router = useRouter();
  const [data, setData] = useState([]);
  const [promptId, setPromptId] = useState(1);
  const [chosenStatements, setChosenStatements] = useState([]);
  const [submitCount, setSubmitCount] = useState(0);

  const [user, setUser] = useState(null);
  const [JWT_TOKEN, setJWT_TOKEN] = useState(null);
  const [role, setRole] = useState(null);

  const checkAuth = () => {
    if (
      !localStorage.getItem("JWT_TOKEN") ||
      !localStorage.getItem("user_data") ||
      !localStorage.getItem("role")
    ) {
      router.push("/auth/student");
    } else {
      setUser(localStorage.getItem("user_data"));
      setJWT_TOKEN(localStorage.getItem("JWT_TOKEN"));
      setRole(localStorage.getItem("role"));
    }
  };

  useEffect(() => {
    checkAuth();
    getProgress();
    fetchData();
  }, []);

  // get user id if user is authenticated
  const user_id = user ? JSON.parse(user).id : null;

  const getProgress = async () => {
    try {
      const response = await fetch(`/api/student/answers`, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          authorization: `Bearer ${localStorage.getItem("JWT_TOKEN")}`,
        },
      });
      if (!response.ok) {
        throw new Error("Error fetching progress");
      }
      const data = await response.json();
      setSubmitCount(data.length);
      setPromptId(data.length + 1);
      if (data.length === 20) {
        router.push("prompts/results");
      }
    } catch (error) {
      console.error(error);
      router.push("/auth/student");
    }
  };

  const fetchData = async () => {
    try {
      if (promptId > 20) return;

      const response = await fetch(`/api/prompt/${promptId}`);
      if (!response.ok) {
        throw new Error("Error fetching data");
      }

      const data = await response.json();
      setData(data.statements);
    } catch (error) {
      console.error("Error fetching data", error);
    }
  };

  const handleNextPrompt = () => {
    setPromptId((prev) => prev + 1);
  };

  const handleChosenStatements = async (statement_id) => {
    try {
      const response = await fetch(`/api/student/answers`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          authorization: `Bearer ${JWT_TOKEN}`,
        },
        body: JSON.stringify({
          statement_id,
          student_id: user_id,
          prompt_id: promptId,
        }),
      });

      if (!response.ok) {
        throw new Error("Error submitting answer");
      }

      setChosenStatements((prev) => [...prev, statement_id]);
      setSubmitCount((prev) => prev + 1);
      handleNextPrompt();
    } catch (error) {
      console.error(error);
      router.push("/auth/student");
    }
  };

  if (
    !localStorage.getItem("JWT_TOKEN") ||
    !localStorage.getItem("user_data") ||
    !localStorage.getItem("role")
  ) {
    return <div>Redirecting...</div>;
  } else {
    return (
      <section className="flex flex-col items-center justify-center h-screen px-6 py-8 mx-auto ">
        <h1 className="pb-5 text-3xl font-semibold text-center text-card-foreground">
          Welkom {user ? JSON.parse(user).name : null} {`(`}
          {user ? JSON.parse(user).student_num : null}
          {`)`}
        </h1>

        <h1 className="pb-10 text-3xl font-semibold text-center text-card-foreground">
          {submitCount === 20 ? null : `${promptId}/20`}
        </h1>
        {submitCount === 20 ? (
          <h1 className="text-3xl">Done!</h1>
        ) : (
          <div className="flex flex-col gap-10">
            {data.map((item) => (
              <Button
                onClick={() => handleChosenStatements(item.statement_id)}
                key={item.statement_id}
                className="py-20 text-xl text-center text-wrap max-w-80 min-w-80"
              >
                {item.statement}
              </Button>
            ))}
          </div>
        )}
      </section>
    );
  }
}
