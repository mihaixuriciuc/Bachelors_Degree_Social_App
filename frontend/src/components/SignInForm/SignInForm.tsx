import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../../api/api";
import "./SignInForm.scss";
import { Link } from "react-router-dom";

function SignInForm() {
  const navigate = useNavigate();
  // State to hold Django's error messages
  const [errors, setErrors] = useState<Record<string, string[]>>({});
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setErrors({}); // Clear previous errors
    setLoading(true);

    const formData = new FormData(e.currentTarget);
    const data = Object.fromEntries(formData.entries());

    try {
      const response = await api.post("/signIn/", data);
      if (response.status === 200) {
        navigate("/feed"); // Or wherever you want them to go after signing in
      }
    } catch (err: any) {
      console.error("Sign in failed:", err);
      // If Django sends back specific field errors (e.g., {"username": ["..."]})
      if (err.response && err.response.data) {
        setErrors(err.response.data);
      } else {
        // Fallback for network issues or unexpected errors
        setErrors({ detail: ["Something went wrong. Please try again."] });
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="signin-form">
      {/* Display generic errors (like "Invalid username or password") */}
      {errors.detail && <p className="global-error">{errors.detail}</p>}

      <div className="input-group">
        <input
          type="text"
          name="username"
          placeholder="Username"
          required
          className={`form-input ${errors.username ? "input-error" : ""}`}
        />
        {errors.username && (
          <span className="error-text">{errors.username[0]}</span>
        )}
      </div>

      <div className="input-group">
        <input
          type="password"
          name="password"
          placeholder="Password"
          required
          className={`form-input ${errors.password ? "input-error" : ""}`}
        />
        {errors.password && (
          <span className="error-text">{errors.password[0]}</span>
        )}
      </div>

      <div className="form-actions">
        <button
          type="reset"
          className="btn-reset"
          onClick={() => setErrors({})}
        >
          Clear
        </button>
        <button type="submit" className="btn-submit" disabled={loading}>
          {loading ? "Signing In..." : "Sign In"}
        </button>

        <div style={{ textAlign: "center" }}>
          <Link
            to="/forgot-password"
            style={{
              color: "#9414e3",
              textDecoration: "none",
              fontSize: "0.9rem",
              fontWeight: "600",
            }}
          >
            Forgot Password?
          </Link>
        </div>
      </div>
    </form>
  );
}

export default SignInForm;
