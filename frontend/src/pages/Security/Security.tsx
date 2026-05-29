import { Link } from "react-router-dom";
import SecurityForm from "../../components/SecurityForm/SecurityForm";
import { useFetch } from "../../hooks/useFetch";
import { profileService } from "../../services/profileService";
// Reuse the layout styles from EditProfile
import "../EditProfile/EditProfile.scss";

function Security() {
  const { data: profile, loading } = useFetch(() => profileService.getMine());

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
            <SecurityForm initialData={profile || {}} />
          )}
        </div>
      </div>
    </div>
  );
}

export default Security;