import { useState } from "react";
import { Link } from "react-router-dom";
import api from "../../api/api";
import "../SignIn/SignIn.scss"; // Reusing your auth container styles!

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
      const response = await api.post("/password-reset/request/", { email });
      setStatus("success");
      setMessage(response.data.message);
    } catch (err: any) {
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

        <h1 style={{ marginBottom: "10px" }}>Forgot Password?</h1>
        <p
          style={{
            textAlign: "center",
            color: "#6c757d",
            marginBottom: "30px",
          }}
        >
          Enter your email address and we'll send you a link to reset your
          password.
        </p>

        {status === "success" ? (
          <div
            style={{ textAlign: "center", color: "#28a745", fontWeight: "600" }}
          >
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

            <div className="form-actions" style={{ marginTop: "15px" }}>
              <button
                type="submit"
                className="btn-submit"
                disabled={status === "loading"}
                style={{ width: "100%" }}
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
