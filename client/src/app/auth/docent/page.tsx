"use client";

import { useRouter } from "next/navigation";

export default function DocentAuth() {
  const router = useRouter();

  const onSubmit = async (event) => {
    event.preventDefault();

    const formData = new FormData(event.currentTarget);
    const response = await fetch("/api/auth/teacher", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        username: formData.get("username"),
        password: formData.get("password"),
      }),
    });

    if (response.ok) {
      const result = await response.json();
      const JWT_TOKEN = result.access_token;

      localStorage.setItem("username", formData.get("username").toString());
      localStorage.setItem("JWT_TOKEN", JWT_TOKEN);
      localStorage.setItem("role", "teacher");

      router.push("/dashboard");
    } else {
      const error = await response.json();
      console.error("Error:", error);
    }
  };

  return (
    <section className="flex flex-col items-center justify-center px-6 py-8 mx-auto md:h-screen lg:py-0">
      <div className="w-full rounded-lg shadow bg-card-foreground md:mt-0 sm:max-w-md xl:p-0 ">
        <div className="p-6 space-y-4 md:space-y-6 sm:p-8">
          <h1 className="text-xl font-bold leading-tight tracking-tight text-gray-900 md:text-2xl">
            Meld u aan
          </h1>
          <form
            className="space-y-4 md:space-y-6"
            method="post"
            onSubmit={onSubmit}
          >
            <div>
              <label
                htmlFor="username"
                className="block mb-2 text-sm font-medium text-gray-900 "
              >
                Gebruikersnaam
              </label>
              <input
                type="text"
                name="username"
                id="username"
                className="bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 "
                placeholder="JOSP"
                required
              />
            </div>
            <div>
              <label
                htmlFor="password"
                className="block mb-2 text-sm font-medium text-gray-900 "
              >
                Wachtwoord
              </label>
              <input
                type="password"
                name="password"
                id="password"
                placeholder="••••••••"
                className="bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 "
                required
              />
            </div>
            <div className="flex items-center justify-between">
              <a
                href="#"
                className="text-sm font-medium text-primary-600 hover:underline dark:text-primary-500"
              >
                Wachtwoord vergeten?
              </a>
            </div>
            <button
              type="submit"
              className="w-full text-white bg-accent hover:bg-secondary focus:ring-4 focus:outline-none focus:ring-ring font-medium rounded-lg text-sm px-5 py-2.5 text-center "
            >
              Log in
            </button>
          </form>
        </div>
      </div>
    </section>
  );
}
