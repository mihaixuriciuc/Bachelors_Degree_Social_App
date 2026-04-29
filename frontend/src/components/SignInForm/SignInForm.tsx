import SubmitAction from "../../helpers/submitAction";
import "./SignInForm.scss";
import { useNavigate } from "react-router-dom"; // 1. Import the hook
function SignInForm() {
  const navigate = useNavigate(); // 2. Initialize the hook
  return (
    <form
      onSubmit={(e) => SubmitAction(e, "/signIn", navigate)}
      className="signin-form"
    >
      <div className="input-group">
        <input type="text" name="username" placeholder="Username" required />
      </div>
      <div className="input-group">
        <input
          type="password"
          name="password"
          placeholder="Password"
          required
        />
      </div>
      <div className="form-actions">
        <button type="reset" className="btn-reset">
          Clear
        </button>
        <button type="submit" className="btn-submit">
          Sign In
        </button>
      </div>
    </form>
  );
}

export default SignInForm;
