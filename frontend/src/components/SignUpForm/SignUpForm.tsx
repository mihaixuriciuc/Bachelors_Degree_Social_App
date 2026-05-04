import "./SignUpForm.scss";
import SubmitAction from "../../helpers/submitAction";
import { useNavigate } from "react-router-dom"; // 1. Import the hook

function SignUpForm() {
  const navigate = useNavigate();
  return (
    <form
      onSubmit={(e) => SubmitAction(e, "/signUp", navigate)}
      className="signup-form"
    >
      <input
        type="text"
        name="username"
        placeholder="Username"
        className="form-input"
        required
      />
      <input
        type="email"
        name="email"
        placeholder="Email Address"
        className="form-input"
        required
      />
      <input
        type="password"
        name="password"
        placeholder="Password"
        className="form-input"
        required
      />

      <div className="name-row">
        <input
          type="text"
          name="first_name"
          placeholder="First Name"
          className="form-input"
        />
        <input
          type="text"
          name="last_name"
          placeholder="Last Name"
          className="form-input"
        />
      </div>

      <div className="form-footer">
        <button type="submit" className="btn-signup">
          Create Account
        </button>
        <button type="reset" className="btn-clear">
          Start Over
        </button>
      </div>
    </form>
  );
}

export default SignUpForm;
