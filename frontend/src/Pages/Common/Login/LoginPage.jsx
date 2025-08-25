import React, { useState, useContext } from "react";
import { useNavigate } from 'react-router-dom';
import logo from '../../../Assets/Logo/Cargo-Photoroom.png';
import AuthController from '../../../Controllers/Common/AuthController';
import './style.css';
import { TokenContext } from '../../../Contexts/TokenContexts';

function LoginPage() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const { saveToken } = useContext(TokenContext);
  const navigate = useNavigate();

  async function handleLogin(e) {
    e.preventDefault();
    setError("");

    if (!username || !password) {
      setError("Please enter both username and password.");
      return;
    }

    const user = { username, password };

    try {
      setLoading(true);
      const loggedUser = await AuthController.login({user});
      saveToken(loggedUser.token);

      switch (loggedUser.role) {
        case "admin":
          navigate("/AdminDashboard");
          break;
        case "manager":
          navigate("/ManagerDashboard");
          break;
        case "analyst":
          navigate("/AnalystDashboard");
          break;
        default:
          navigate("/");
      }

    } catch (err) {
      setError(err.message || "Login failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="login-wrapper">
      {/* Top bar brand */}
      <header className="login-header">
        <img src={logo} alt="" className="login-page-logo"/>
      </header>

      {/* Center card */}
      <section className="login-container">
        <div className="login-card">
          <h1 className="login-title">Sign in</h1>

          <form onSubmit={handleLogin} className="login-form" noValidate>
            {/* Username */}
            <div className="form-group">
              <label htmlFor="username" className="form-label">Username</label>
              <input
                id="username"
                type="text"
                autoComplete="username"
                placeholder="e.g. john.doe"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                className="form-input"
              />
            </div>

            {/* Password */}
            <div className="form-group">
              <label htmlFor="password" className="form-label">Password</label>
              <div className="form-password-wrapper">
                <input
                  id="password"
                  type={showPassword ? "text" : "password"}
                  autoComplete="current-password"
                  placeholder="••••••••"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="form-input password-input"
                />
                <button
                  type="button"
                  onClick={() => setShowPassword((s) => !s)}
                  className="toggle-password-button"
                  aria-label={showPassword ? "Hide password" : "Show password"}
                >
                  {showPassword ? "Hide" : "Show"}
                </button>
              </div>
            </div>

            {/* Remember + Forgot */}
            <div className="form-options">
              <label className="form-checkbox-label">
                <input type="checkbox" className="form-checkbox" />
                Remember me
              </label>
              <button
                type="button"
                className="forgot-password-link"
                onClick={() => alert("Forgot password flow here")}
              >
                Forgot password?
              </button>
            </div>

            {/* Error Message */}
            {error && (
              <div className="form-error" role="alert">
                {error}
              </div>
            )}

            {/* Submit */}
            <button
              type="submit"
              disabled={loading}
              className="form-submit-button"
            >
              {loading ? "Signing in…" : "Sign in"}
            </button>
          </form>

        </div>
      </section>
    </main>
  );
}

export default LoginPage;
