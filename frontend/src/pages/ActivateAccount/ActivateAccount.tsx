import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import api from "../../api/api";
import "./ActivateAccount.scss";

function ActivateAccount() {
  // Grab the variables from the URL (e.g., /activate/123/abc-def)
  const { uid, token } = useParams<{ uid: string; token: string }>();

  const [status, setStatus] = useState<"loading" | "success" | "error">(
    "loading",
  );
  const [message, setMessage] = useState("Verifying your account...");

  useEffect(() => {
    const verifyAccount = async () => {
      try {
        // Send the POST request to Django
        const response = await api.post(`/activate/${uid}/${token}/`);
        setStatus("success");
        setMessage(response.data.message || "Account activated successfully!");
      } catch (err: any) {
        setStatus("error");
        // If Django sends a specific error message, use it. Otherwise, fallback.
        setMessage(
          err.response?.data?.error || "Invalid or expired activation link.",
        );
      }
    };

    if (uid && token) {
      verifyAccount();
    } else {
      setStatus("error");
      setMessage("Missing activation data in the URL.");
    }
  }, [uid, token]);

  return (
    <div className="activate-page">
      <div className="auth-container text-center">
        {status === "loading" && (
          <>
            <div className="spinner"></div>
            <h2>{message}</h2>
          </>
        )}

        {status === "success" && (
          <>
            <h1 className="success-text">Success!</h1>
            <p>{message}</p>
            <Link to="/signin" className="btn-primary mt-4 inline-block">
              Go to Sign In
            </Link>
          </>
        )}

        {status === "error" && (
          <>
            <h1 className="error-text"> Verification Failed</h1>
            <p>{message}</p>
            <Link to="/signup" className="btn-secondary mt-4 inline-block">
              Try Registering Again
            </Link>
          </>
        )}
      </div>
    </div>
  );
}

export default ActivateAccount;
