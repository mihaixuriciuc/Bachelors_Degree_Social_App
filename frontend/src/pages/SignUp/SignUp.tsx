import SignUpForm from "../../components/SignUpForm/SignUpForm";
import "./SignUp.scss";

function SignUp() {
  return (
    <>
      <div className="signup-page">
        <div className="auth-container">
          <h1>Salut bine ai venit</h1>
          <SignUpForm />
        </div>
      </div>
    </>
  );
}

export default SignUp;
