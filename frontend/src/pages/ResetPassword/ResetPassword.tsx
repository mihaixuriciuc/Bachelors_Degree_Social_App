import { useState } from "react";
import { useParams, Link } from "react-router-dom";
import { AxiosError } from "axios";
import { authService } from "../../services/authService";
import "../SignIn/SignIn.scss";
import "./ResetPassword.scss";

function ResetPassword() {
  const { uid, token } = useParams<{ uid: string; token: string }>();

  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [status, setStatus] = useState<
    "idle" | "loading" | "success" | "error"
  >("idle");
  const [message, setMessage] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (newPassword !== confirmPassword) {
      setStatus("error");
      setMessage("Passwords do not match.");
      return;
    }

    if (!uid || !token) {
      setStatus("error");
      setMessage("Invalid reset link.");
      return;
    }

    setStatus("loading");
    try {
      const response = await authService.confirmPasswordReset(
        uid,
        token,
        newPassword,
      );
      setStatus("success");
      setMessage(response.data.message);
    } catch (err) {
      setStatus("error");
      const errorMsg =
        err instanceof AxiosError && err.response?.data?.error
          ? err.response.data.error
          : "Link is invalid or has expired.";
      setMessage(errorMsg);
    }
  };

  return (
    <div className="signin-page">
      <div className="auth-container">
        <h1 className="page-title">Set New Password</h1>

        {status === "success" ? (
          <div className="success-container">
            <p className="success-message">{message}</p>
            <Link to="/signin" className="btn-submit">
              Go to Sign In
            </Link>
          </div>
        ) : (
          <form className="signin-form" onSubmit={handleSubmit}>
            {status === "error" && <p className="global-error">{message}</p>}

            <div className="input-group">
              <input
                type="password"
                placeholder="New Password"
                required
                value={newPassword}
                onChange={(e) => setNewPassword(e.target.value)}
              />
            </div>

            <div className="input-group input-group-spaced">
              <input
                type="password"
                placeholder="Confirm New Password"
                required
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
              />
            </div>

            <div className="form-actions-full">
              <button
                type="submit"
                className="btn-submit"
                disabled={status === "loading"}
              >
                {status === "loading" ? "Saving..." : "Reset Password"}
              </button>
            </div>
          </form>
        )}
      </div>
    </div>
  );
}

export default ResetPassword;
