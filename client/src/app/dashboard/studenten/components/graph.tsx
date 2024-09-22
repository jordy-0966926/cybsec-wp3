"use client";

import { Bar, BarChart, ResponsiveContainer, XAxis, YAxis } from "recharts";

const data = [
  {
    name: "INFJ",
    total: Math.floor(Math.random() * 5) + 1,
  },
  {
    name: "INFP",
    total: Math.floor(Math.random() * 5) + 1,
  },
  {
    name: "ENFJ",
    total: Math.floor(Math.random() * 5) + 1,
  },
  {
    name: "ENFP",
    total: Math.floor(Math.random() * 5) + 1,
  },
  {
    name: "ISTJ",
    total: Math.floor(Math.random() * 5) + 1,
  },
  {
    name: "ISFJ",
    total: Math.floor(Math.random() * 5) + 1,
  },
  {
    name: "ESTJ",
    total: Math.floor(Math.random() * 5) + 1,
  },
  {
    name: "ESFJ",
    total: Math.floor(Math.random() * 5) + 1,
  },
  {
    name: "INTJ",
    total: Math.floor(Math.random() * 5) + 1,
  },
  {
    name: "INTP",
    total: Math.floor(Math.random() * 5) + 1,
  },
  {
    name: "ENTJ",
    total: Math.floor(Math.random() * 5) + 1,
  },
  {
    name: "ENTP",
    total: Math.floor(Math.random() * 5) + 1,
  },
  {
    name: "ISTP",
    total: Math.floor(Math.random() * 5) + 1,
  },
  {
    name: "ISFP",
    total: Math.floor(Math.random() * 5) + 1,
  },
  {
    name: "ESTP",
    total: Math.floor(Math.random() * 5) + 1,
  },
  {
    name: "ESFP",
    total: Math.floor(Math.random() * 5) + 1,
  },
];

export function Graph() {
  return (
    <ResponsiveContainer width="100%" height={350}>
      <BarChart data={data}>
        <XAxis
          dataKey="name"
          stroke="#888888"
          fontSize={12}
          tickLine={false}
          axisLine={false}
        />
        <YAxis
          stroke="#888888"
          fontSize={12}
          tickLine={false}
          axisLine={false}
          tickFormatter={(value) => `${value}`}
        />
        <Bar
          dataKey="total"
          fill="currentColor"
          radius={[4, 4, 0, 0]}
          className="fill-primary"
        />
      </BarChart>
    </ResponsiveContainer>
  );
}
