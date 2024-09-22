"use client";
import Link from "next/link";

export default function Auth() {
  localStorage.clear();
  return (
    <section className="flex flex-col items-center justify-center h-screen px-6 py-8 mx-auto">
      <div className="w-full rounded-sm shadow bg-primary-foreground md:mt-0 sm:max-w-md xl:p-0">
        <div className="flex-col items-center justify-center p-6 space-y-4 md:space-y-6 sm:p-8">
          <div>
            <h1 className="text-5xl font-bold leading-tight tracking-tight text-center text-card-foreground">
              Ik ben een
            </h1>
          </div>

          <div>
            <Link href="/auth/student">
              <button
                type="button"
                className="w-full text-4xl text-white bg-accent hover:bg-secondary focus:ring-4 focus:outline-none focus:ring-ring font-medium rounded-md px-5 py-2.5 text-center"
              >
                Student
              </button>
            </Link>
          </div>
          <div className="flex flex-col items-center ">
            <Link href="/auth/docent">
              <button
                type="button"
                className="  text-white bg-accent hover:bg-accent focus:ring-4 focus:outline-none focus:ring-ring font-medium rounded-md px-5 py-2.5 text-center"
              >
                Docent
              </button>
            </Link>
          </div>
        </div>
      </div>
    </section>
  );
}
