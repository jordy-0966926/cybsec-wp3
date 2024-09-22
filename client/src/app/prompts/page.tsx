"use client";
import React, { useState, useEffect } from "react";
import { Button } from "../../components/ui/button";

export default function Prompts() {
  const [data, setData] = useState([]);
  const [promptId, setPromptId] = useState(1);
  const [chosenStatements, setChosenStatements] = useState([]);
  const [submitCount, setSubmitCount] = useState(0);

  const fetchData = async () => {
    try {
      if (promptId > 20) {
        return;
      }
      const response = await fetch(`/api/prompt/${promptId}`);
      const data = await response.json();
      setData(data.statements);
    } catch (error) {
      console.error("Error fetching data", error);
    }
  };

  useEffect(() => {
    fetchData();
  }, [promptId]);

  const handleNextPrompt = () => {
    setPromptId(promptId + 1);
  };

  const handleChosenStatements = (statement) => {
    setChosenStatements([...chosenStatements, statement]);
    setSubmitCount(submitCount + 1);
    handleNextPrompt();
  };

  useEffect(() => {
    if (submitCount === 20) {
      submitStatements();
    }
  }, [submitCount]);

  const submitStatements = async () => {
    try {
      const response = await fetch("/api/answer/submit", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(chosenStatements),
      });
      console.log("Statements submitted:", response);
    } catch (error) {
      console.error("Error submitting statements", error);
    }
  };

  return (
    <section className="flex flex-col items-center justify-center h-screen px-6 py-8 mx-auto ">
      <h1 className="pb-10 text-3xl font-semibold text-center text-card-foreground">
        {submitCount === 20 ? null : promptId + "/20"}
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
