import { useState } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import AuthController from "../../Controllers/Common/AuthController";

export default function ResetPassword() {
  const navigate = useNavigate();
  const params = new URLSearchParams(useLocation().search);
  const token = params.get("token");
  const email = params.get("email") || "";

  const [password, setPassword] = useState("");
  const [confirm, setConfirm]   = useState("");
  const [msg, setMsg] = useState("");
  const [loading, setLoading] = useState(false);

  async function submit(e) {
    e.preventDefault();
    setMsg("");
    if (password !== confirm) {
      setMsg("Passwords do not match.");
      return;
    }
    try {
      setLoading(true);
      await AuthController.resetPassword({
        token, email, password, password_confirmation: confirm
      });
      setMsg("Password reset. You can now sign in.");
      setTimeout(()=>navigate("/"), 1000);
    } catch (err) {
      const m = err?.response?.data?.errors?.token?.[0]
            ?? err?.response?.data?.message
            ?? "Reset failed. The link may be expired.";
      setMsg(m);
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="login-wrapper">
      <section className="login-container">
        <div className="login-card">
          <h1 className="login-title">Set a New Password</h1>
          <form onSubmit={submit} className="login-form" noValidate>
            <div className="form-group">
              <label className="form-label">Email</label>
              <input className="form-input" value={email} readOnly />
            </div>
            <div className="form-group">
              <label className="form-label">New Password</label>
              <input type="password" className="form-input"
                     value={password} onChange={e=>setPassword(e.target.value)} minLength={8} required/>
            </div>
            <div className="form-group">
              <label className="form-label">Confirm Password</label>
              <input type="password" className="form-input"
                     value={confirm} onChange={e=>setConfirm(e.target.value)} minLength={8} required/>
            </div>
            {msg && <div className="form-info">{msg}</div>}
            <button className="form-submit-button" disabled={loading}>
              {loading ? "Resetting…" : "Reset password"}
            </button>
          </form>
        </div>
      </section>
    </main>
  );
}
