import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import api from "../../api/api";
import SecurityForm from "../../components/SecurityForm/SecurityForm";
// Reuse the layout styles from EditProfile
import "../EditProfile/EditProfile.scss";

function Security() {
  const [initialData, setInitialData] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const response = await api.get("/account/profile/");
        setInitialData(response.data);
      } catch (err) {
        console.error("Failed to load security data", err);
      } finally {
        setLoading(false);
      }
    };
    fetchProfile();
  }, []);

  return (
    <div className="edit-profile-page">
      <nav className="top-nav">
        <Link to="/profile" className="btn-back-minimal">
          <span className="arrow">&larr;</span> Back to Profile
        </Link>
      </nav>

      <div className="content-wrapper">
        <div className="form-container">
          <h1>Account Security</h1>

          {loading ? (
            <div className="loading-state">
              <div className="spinner"></div>
              <p>Loading security data...</p>
            </div>
          ) : (
            <SecurityForm initialData={initialData || {}} />
          )}
        </div>
      </div>
    </div>
  );
}

export default Security;
