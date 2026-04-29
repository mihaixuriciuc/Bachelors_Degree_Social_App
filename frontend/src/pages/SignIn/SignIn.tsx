import SignInForm from "../../components/SignInForm/SignInForm";
import "./SignIn.scss";

function SignIn() {
  return (
    <div className="signin-page">
      <div className="auth-container">
        <h1>Welcome Back</h1>
        <SignInForm />
      </div>
    </div>
  );
}

export default SignIn;
