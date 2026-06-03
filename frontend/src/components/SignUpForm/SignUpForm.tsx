import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { AxiosError } from "axios";
import { authService } from "../../services/authService";
import "./SignUpForm.scss";

function SignUpForm() {
  const navigate = useNavigate();
  const [errors, setErrors] = useState<Record<string, string | string[]>>({});
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setErrors({});
    setLoading(true);

    const formData = new FormData(e.currentTarget);
    const data = {
      username: formData.get("username") as string,
      email: formData.get("email") as string,
      password: formData.get("password") as string,
      confirm_password: formData.get("confirm_password") as string,
      first_name: formData.get("first_name") as string,
      last_name: formData.get("last_name") as string,
    };

    // Catch the password mismatch on the frontend to save an API call.
    if (data.password !== data.confirm_password) {
      setErrors({ confirm_password: ["Passwords do not match."] });
      setLoading(false);
      return;
    }

    try {
      await authService.signUp(data);
      navigate("/check-email");
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
    <form onSubmit={handleSubmit} className="signup-form">
      {errors.error && <p className="global-error">{errors.error}</p>}

      <div className="input-group">
        <input
          type="text"
          name="username"
          placeholder="Username"
          className={`form-input ${errors.username ? "input-error" : ""}`}
          required
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
          type="email"
          name="email"
          placeholder="Email Address"
          className={`form-input ${errors.email ? "input-error" : ""}`}
          required
        />
        {errors.email && (
          <span className="error-text">
            {Array.isArray(errors.email) ? errors.email[0] : errors.email}
          </span>
        )}
      </div>

      <div className="input-group">
        <input
          type="password"
          name="password"
          placeholder="Password"
          className={`form-input ${errors.password ? "input-error" : ""}`}
          required
        />
        {errors.password && (
          <span className="error-text">
            {Array.isArray(errors.password)
              ? errors.password[0]
              : errors.password}
          </span>
        )}
      </div>

      <div className="input-group">
        <input
          type="password"
          name="confirm_password"
          placeholder="Confirm Password"
          className={`form-input ${errors.confirm_password ? "input-error" : ""}`}
          required
        />
        {errors.confirm_password && (
          <span className="error-text">
            {Array.isArray(errors.confirm_password)
              ? errors.confirm_password[0]
              : errors.confirm_password}
          </span>
        )}
      </div>

      <div className="name-row">
        <div className="input-group">
          <input
            type="text"
            name="first_name"
            placeholder="First Name"
            className={`form-input ${errors.first_name ? "input-error" : ""}`}
            required
          />
          {errors.first_name && (
            <span className="error-text">
              {Array.isArray(errors.first_name)
                ? errors.first_name[0]
                : errors.first_name}
            </span>
          )}
        </div>
        <div className="input-group">
          <input
            type="text"
            name="last_name"
            placeholder="Last Name"
            className={`form-input ${errors.last_name ? "input-error" : ""}`}
            required
          />
          {errors.last_name && (
            <span className="error-text">
              {Array.isArray(errors.last_name)
                ? errors.last_name[0]
                : errors.last_name}
            </span>
          )}
        </div>
      </div>

      <div className="form-footer">
        <button type="submit" className="btn-signup" disabled={loading}>
          {loading ? "Creating Account..." : "Create Account"}
        </button>
        <button
          type="reset"
          className="btn-clear"
          onClick={() => setErrors({})}
        >
          Start Over
        </button>
      </div>
    </form>
  );
}

export default SignUpForm;
