import { useState } from "react";
import { Link } from "react-router-dom";
import { authService } from "../../services/authService";
import "../SignIn/SignIn.scss";
import "./ForgotPassword.scss";

function ForgotPassword() {
  const [email, setEmail] = useState("");
  const [status, setStatus] = useState<
    "idle" | "loading" | "success" | "error"
  >("idle");
  const [message, setMessage] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setStatus("loading");
    setMessage("");

    try {
      const response = await authService.requestPasswordReset(email);
      setStatus("success");
      setMessage(response.data.message);
    } catch {
      setStatus("error");
      setMessage("Something went wrong. Please try again.");
    }
  };

  return (
    <div className="signin-page">
      <div className="auth-container">
        <Link to="/signin" className="btn-back-auth">
          <span className="arrow">&larr;</span> Back to Sign In
        </Link>

        <h1 className="page-title">Forgot Password?</h1>
        <p className="page-subtitle">
          Enter your email address and we'll send you a link to reset your
          password.
        </p>

        {status === "success" ? (
          <div className="success-message">
            <p>{message}</p>
          </div>
        ) : (
          <form className="signin-form" onSubmit={handleSubmit}>
            {status === "error" && <p className="global-error">{message}</p>}

            <div className="input-group">
              <input
                type="email"
                placeholder="Email Address"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
            </div>

            <div className="form-actions-full">
              <button
                type="submit"
                className="btn-submit"
                disabled={status === "loading"}
              >
                {status === "loading" ? "Sending..." : "Send Reset Link"}
              </button>
            </div>
          </form>
        )}
      </div>
    </div>
  );
}

export default ForgotPassword;
