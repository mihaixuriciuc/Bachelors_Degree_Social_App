import SignUpForm from "../../components/SignUpForm/SignUpForm";
import "./SignUp.scss";
import { Link } from "react-router-dom";

function SignUp() {
  return (
    <>
      <div className="signup-page">
        <div className="auth-container">
          <Link to="/" className="btn-back-auth">
            <span className="arrow">&larr;</span> Back to Home
          </Link>
          <h1>Salut bine ai venit</h1>
          <SignUpForm />
        </div>
      </div>
    </>
  );
}

export default SignUp;
