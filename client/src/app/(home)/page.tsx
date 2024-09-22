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
    const response = await fetch("/api/auth/session", {
      method: "GET",
      headers: { "Content-Type": "application/json" },
    });
    const data = await response.json();
    console.log(data);
    if (data[1] === 401) {
      {
        router.push("/auth");
      }
    }

    return (
      <main className="flex flex-col items-center justify-center h-screen px-6 py-8 mx-auto ">
        <Link href="/prompts" className="text-6xl">
          Start
        </Link>
      </main>
    );
  };
}
