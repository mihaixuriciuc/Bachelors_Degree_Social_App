import SignInForm from "../../components/SignInForm/SignInForm";
import "./SignIn.scss";
import { Link } from "react-router-dom";
function SignIn() {
  return (
    <div className="signin-page">
      <div className="auth-container">
        <Link to="/" className="btn-back-auth">
          <span className="arrow">&larr;</span> Back to Home
        </Link>
        <h1>Welcome Back</h1>
        <SignInForm />
      </div>
    </div>
  );
}

export default SignIn;
