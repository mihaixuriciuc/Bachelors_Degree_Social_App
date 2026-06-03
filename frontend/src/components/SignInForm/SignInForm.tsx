import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { AxiosError } from "axios";
import { authService } from "../../services/authService";
import { useAuth } from "../../hooks/useAuth";
import "./SignInForm.scss";

function SignInForm() {
  const navigate = useNavigate();
  const { refreshUser } = useAuth();
  const [errors, setErrors] = useState<Record<string, string | string[]>>({});
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setErrors({});
    setLoading(true);

    const formData = new FormData(e.currentTarget);
    const data = {
      username: formData.get("username") as string,
      password: formData.get("password") as string,
    };

    try {
      await authService.signIn(data);
      // After login, hydrate the AuthContext so ProtectedRoute lets us in.
      await refreshUser();
      navigate("/feed");
    } catch (err) {
      if (err instanceof AxiosError && err.response?.data) {
        setErrors(err.response.data);
      } else {
        setErrors({ error: "Something went wrong. Please try again." });
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="signin-form">
      {/* The backend sends generic errors under the "error" key (e.g. "Invalid username or password.") */}
      {errors.error && <p className="global-error">{errors.error}</p>}

      <div className="input-group">
        <input
          type="text"
          name="username"
          placeholder="Username"
          required
          className={`form-input ${errors.username ? "input-error" : ""}`}
        />
        {errors.username && (
          <span className="error-text">
            {Array.isArray(errors.username)
              ? errors.username[0]
              : errors.username}
          </span>
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
          <span className="error-text">
            {Array.isArray(errors.password)
              ? errors.password[0]
              : errors.password}
          </span>
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

        <div className="forgot-password-link">
          <Link to="/forgot-password" className="link-primary">
            Forgot Password?
          </Link>
        </div>
      </div>
    </form>
  );
}

export default SignInForm;
