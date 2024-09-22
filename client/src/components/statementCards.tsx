import React, { useState, useEffect } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "./ui/card";

export function StatementCards() {
  const [data, setData] = useState([]);

  const getData = async () => {
    try {
      const response = await fetch("/api/statement");
      const data = await response.json();
      setData(data);
    } catch (error) {
      console.error("Error fetching data", error);
    }
  };
  useEffect(() => {
    getData();
  }, []);

  return (
    <section className="bg-background max-w-3xl mx-auto ">
      <div className="grid grid-cols-3 gap-10">
        {data.map((item, index) => (
          <Card key={index}>
            <CardHeader>
              <CardTitle className="text-right">{item.id}</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-center">{item.statement}</p>
            </CardContent>
          </Card>
        ))}
      </div>
    </section>
  );
}
