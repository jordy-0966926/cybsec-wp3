"use client";
import Image from "next/image";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useEffect } from "react";

export default function Home() {
  const router = useRouter();

  useEffect(() => {
    authHandler();
  }, []);
  const authHandler = async () => {
    if (
      !localStorage.getItem("JWT_TOKEN") ||
      !localStorage.getItem("username") ||
      !localStorage.getItem("role")
    ) {
      router.push("/auth");
    } else if (localStorage.getItem("role") === "student") {
      router.push("/prompts");
    } else if (localStorage.getItem("role") === "teacher") {
      router.push("/dashboard");
    }

    return <div>Loading...</div>;
  };
}
