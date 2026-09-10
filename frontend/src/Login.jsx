import { useState } from "react";
import {
  Eye,
  EyeOff,
  Lock,
  Mail,
  Waves,
  ArrowRight,
} from "lucide-react";

function Login({ onLogin }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    setError("");

    if (!email.trim() || !password.trim()) {
      setError("Please enter your email and password.");
      return;
    }

    // Demo authentication for SIH prototype
    if (
      email.trim().toLowerCase() === "admin@orca.ai" &&
      password === "orca123"
    ) {
      localStorage.setItem("orca_logged_in", "true");
      localStorage.setItem("orca_user", email.trim());
      onLogin();
    } else {
      setError("Invalid credentials. Use the demo account below.");
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 text-white">
      <div className="relative flex min-h-screen items-center justify-center overflow-hidden px-6 py-12">

        {/* Background effects */}
        <div className="absolute inset-0">
          <div className="absolute left-1/2 top-1/2 h-[600px] w-[600px] -translate-x-1/2 -translate-y-1/2 rounded-full bg-cyan-500/5 blur-3xl" />
          <div className="absolute left-10 top-10 h-40 w-40 rounded-full bg-blue-500/5 blur-3xl" />
          <div className="absolute bottom-10 right-10 h-48 w-48 rounded-full bg-cyan-500/5 blur-3xl" />
        </div>

        <div className="relative z-10 w-full max-w-md">

          {/* Logo */}
          <div className="mb-8 text-center">

            <div className="mx-auto flex h-16 w-16 items-center justify-center rounded-2xl border border-cyan-500/20 bg-cyan-500/10 shadow-lg shadow-cyan-500/5">
              <Waves className="h-8 w-8 text-cyan-400" />
            </div>

            <h1 className="mt-5 text-4xl font-bold tracking-tight">
              ORCA
            </h1>

            <p className="mt-2 text-sm text-slate-400">
              Marine Ecosystem Intelligence System
            </p>

          </div>

          {/* Login card */}
          <div className="rounded-3xl border border-slate-800 bg-slate-900/90 p-8 shadow-2xl backdrop-blur">

            <div className="mb-7">
              <h2 className="text-2xl font-semibold">
                Welcome back
              </h2>

              <p className="mt-2 text-sm text-slate-500">
                Sign in to access ORCA intelligence.
              </p>
            </div>

            <form
              onSubmit={handleSubmit}
              className="space-y-5"
            >

              {/* Email */}
              <div>
                <label className="mb-2 block text-sm font-medium text-slate-300">
                  Email
                </label>

                <div className="relative">

                  <Mail className="absolute left-4 top-1/2 h-5 w-5 -translate-y-1/2 text-slate-500" />

                  <input
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    placeholder="Enter your email"
                    className="w-full rounded-xl border border-slate-700 bg-slate-950 py-3.5 pl-12 pr-4 text-sm text-white outline-none transition placeholder:text-slate-600 focus:border-cyan-500/60 focus:ring-2 focus:ring-cyan-500/10"
                  />

                </div>
              </div>

              {/* Password */}
              <div>
                <label className="mb-2 block text-sm font-medium text-slate-300">
                  Password
                </label>

                <div className="relative">

                  <Lock className="absolute left-4 top-1/2 h-5 w-5 -translate-y-1/2 text-slate-500" />

                  <input
                    type={showPassword ? "text" : "password"}
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    placeholder="Enter your password"
                    className="w-full rounded-xl border border-slate-700 bg-slate-950 py-3.5 pl-12 pr-12 text-sm text-white outline-none transition placeholder:text-slate-600 focus:border-cyan-500/60 focus:ring-2 focus:ring-cyan-500/10"
                  />

                  <button
                    type="button"
                    onClick={() =>
                      setShowPassword(!showPassword)
                    }
                    className="absolute right-4 top-1/2 -translate-y-1/2 text-slate-500 transition hover:text-slate-300"
                  >
                    {showPassword ? (
                      <EyeOff className="h-5 w-5" />
                    ) : (
                      <Eye className="h-5 w-5" />
                    )}
                  </button>

                </div>
              </div>

              {/* Error */}
              {error && (
                <div className="rounded-xl border border-red-500/20 bg-red-500/5 px-4 py-3 text-sm text-red-400">
                  {error}
                </div>
              )}

              {/* Login */}
              <button
                type="submit"
                className="group flex w-full items-center justify-center gap-2 rounded-xl bg-cyan-500 py-3.5 text-sm font-semibold text-slate-950 transition hover:bg-cyan-400 active:scale-[0.99]"
              >
                Sign in

                <ArrowRight className="h-4 w-4 transition group-hover:translate-x-1" />
              </button>

            </form>

            {/* Demo credentials */}
            <div className="mt-6 rounded-xl border border-slate-800 bg-slate-950 p-4">

              <p className="text-xs font-semibold uppercase tracking-wider text-cyan-400">
                SIH Demo Account
              </p>

              <div className="mt-3 space-y-1 text-xs text-slate-500">
                <p>
                  Email:
                  <span className="ml-2 text-slate-300">
                    admin@orca.ai
                  </span>
                </p>

                <p>
                  Password:
                  <span className="ml-2 text-slate-300">
                    orca123
                  </span>
                </p>
              </div>

            </div>

          </div>

          <p className="mt-6 text-center text-xs text-slate-600">
            ORCA • Evidence-grounded marine intelligence
          </p>

        </div>
      </div>
    </div>
  );
}

export default Login;