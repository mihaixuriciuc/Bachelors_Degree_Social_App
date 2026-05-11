import { Link } from "react-router-dom";
import "./CheckEmail.scss";

function CheckEmail() {
  return (
    <div className="check-email-page">
      <div className="auth-container text-center">
        <div className="icon-wrapper">
          <span className="mail-icon">✉️</span>
        </div>

        <h1>Check Your Email</h1>

        <p className="instruction-text">
          We've sent an activation link to your email address. Please click the
          link to activate your account before signing in.
        </p>

        <p className="spam-notice">
          <em>(Don't forget to check your spam folder just in case!)</em>
        </p>

        <div className="action-links">
          <Link to="/signin" className="btn-primary inline-block">
            I've verified my email
          </Link>
          <Link to="/" className="btn-back-auth mt-3">
            <span className="arrow">&larr;</span> Back to Home
          </Link>
        </div>
      </div>
    </div>
  );
}

export default CheckEmail;
