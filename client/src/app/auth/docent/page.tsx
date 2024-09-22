export default function DocentAuth() {
  return (
    <section className="flex flex-col items-center justify-center px-6 py-8 mx-auto md:h-screen lg:py-0">
      <div className="w-full rounded-lg shadow bg-card-foreground md:mt-0 sm:max-w-md xl:p-0 ">
        <div className="p-6 space-y-4 md:space-y-6 sm:p-8">
          <h1 className="text-xl font-bold leading-tight tracking-tight text-gray-900 md:text-2xl">
            Meld u aan
          </h1>
          <form
            className="space-y-4 md:space-y-6"
            method="POST"
            action="{{ url_for('auth.student.student_login') }}"
          >
            <div>
              <label
                htmlFor="username"
                className="block mb-2 text-sm font-medium text-gray-900 "
              >
                Gebruikersnaam
              </label>
              <input
                type="username"
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
