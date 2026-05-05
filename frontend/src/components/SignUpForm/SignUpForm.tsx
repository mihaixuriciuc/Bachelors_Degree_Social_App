import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../../api/api";
import "./SignUpForm.scss";

function SignUpForm() {
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
      const response = await api.post("/signUp", data);
      if (response.status === 200 || response.status === 201) {
        navigate("/check-email");
      }
    } catch (err: any) {
      console.error("Sign up failed:", err);
      // If Django sends back form validation errors, save them to state!
      if (err.response && err.response.data) {
        setErrors(err.response.data);
      } else {
        setErrors({ general: ["Something went wrong. Please try again."] });
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="signup-form">
      {errors.general && <p className="global-error">{errors.general[0]}</p>}

      <div className="input-group">
        <input
          type="text"
          name="username"
          placeholder="Username"
          className={`form-input ${errors.username ? "input-error" : ""}`}
          required
        />
        {errors.username && (
          <span className="error-text">{errors.username[0]}</span>
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
        {errors.email && <span className="error-text">{errors.email[0]}</span>}
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
          <span className="error-text">{errors.password[0]}</span>
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
            <span className="error-text">{errors.first_name[0]}</span>
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
            <span className="error-text">{errors.last_name[0]}</span>
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
