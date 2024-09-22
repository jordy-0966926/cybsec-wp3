"use client";
import React from "react";
import { useRouter } from "next/navigation";

export default function StudenAuth() {
  const router = useRouter();

  const onSubmit = async (event) => {
    //https://nextjs.org/docs/pages/building-your-application/data-fetching/forms-and-mutations

    event.preventDefault();

    const formData = new FormData(event.currentTarget);
    const response = await fetch("/api/auth/student", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ student_num: formData.get("studentnummer") }),
    });

    if (response.ok) {
      const result = await response.json();
      const user_data = result.user_data;
      const JWT_TOKEN = result.access_token;

      if (typeof window !== "undefined") {
        localStorage.setItem("role", "student");
        localStorage.setItem("JWT_TOKEN", JWT_TOKEN);
        localStorage.setItem("user_data", JSON.stringify(user_data));
      }

      router.push("/prompts");
    }
  };

  return (
    <section className="flex flex-col items-center justify-center px-6 py-8 mx-auto md:h-screen lg:py-0">
      <div>
        <div className="w-full rounded-lg shadow bg-card-foreground md:mt-0 sm:max-w-md xl:p-0">
          <div className="p-6 space-y-4 md:space-y-6 sm:p-8">
            <h1 className="text-xl font-bold leading-tight tracking-tight text-center text-card md:text-2xl">
              Vul je studentnummer in:
            </h1>
            <form className="flex" method="post" onSubmit={onSubmit}>
              <input
                type="text"
                name="studentnummer"
                id="studentnummer"
                placeholder="09669266"
                className="bg-card-foreground border text-center border-border text-muted sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5"
                required
              />
              <button className="pl-4" type="submit">
                👍
              </button>
            </form>
          </div>
        </div>
      </div>
    </section>
  );
}
