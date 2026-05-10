import { useState } from "react";
import { useParams, Link } from "react-router-dom";
import api from "../../api/api";
import "../SignIn/SignIn.scss";

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

    setStatus("loading");
    try {
      // Send the new_password to the backend endpoint using the URL parameters
      const response = await api.post(
        `/password-reset/confirm/${uid}/${token}/`,
        {
          new_password: newPassword,
        },
      );
      setStatus("success");
      setMessage(response.data.message);
    } catch (err: any) {
      setStatus("error");
      setMessage(
        err.response?.data?.error || "Link is invalid or has expired.",
      );
    }
  };

  return (
    <div className="signin-page">
      <div className="auth-container">
        <h1 style={{ marginBottom: "20px" }}>Set New Password</h1>

        {status === "success" ? (
          <div style={{ textAlign: "center" }}>
            <p
              style={{
                color: "#28a745",
                fontWeight: "600",
                marginBottom: "20px",
              }}
            >
              {message}
            </p>
            <Link
              to="/signin"
              className="btn-submit"
              style={{ textDecoration: "none", display: "inline-block" }}
            >
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

            <div className="input-group" style={{ marginTop: "15px" }}>
              <input
                type="password"
                placeholder="Confirm New Password"
                required
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
              />
            </div>

            <div className="form-actions" style={{ marginTop: "20px" }}>
              <button
                type="submit"
                className="btn-submit"
                disabled={status === "loading"}
                style={{ width: "100%" }}
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
