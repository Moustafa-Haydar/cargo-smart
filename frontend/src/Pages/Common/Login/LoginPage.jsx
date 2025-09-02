import React, { useState } from "react";
import { useNavigate } from 'react-router-dom';
import logo from '../../../Assets/Logo/Cargo-Photoroom.png';
import AuthController from '../../../Controllers/Common/AuthController';
import {useAuth} from "../../../Contexts/AuthContext";
import './style.css';

function LoginPage() {
  const { loggedUser } = useAuth();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    
    if (loggedUser) {
      switch (user_group) {
        case "Admin":
          navigate("/AdminDashboard");
          break;
        case "ops manager":
          navigate("/OpsManagerDashboard");
          break;
        default:
          navigate("/");
      }
    }

  }, []);
  
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

      const user_group = loggedUser.groups[0].name;
      
      switch (user_group) {
        case "Admin":
          navigate("/AdminDashboard");
          break;
        case "ops manager":
          navigate("/OpsManagerDashboard");
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

  async function handleForgotPassword() {

    if (!username) {
      setError("Please enter your username to reset password.");
      return;
    }

    try {
      setLoading(true);
      await AuthController.sendResetLink({ username });
    } catch (err) {
      setError(err.message || "Failed to send reset link");
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
                onClick={() => handleForgotPassword() }
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
