import { Link } from "react-router-dom";
import EditProfileForm from "../../components/EditProfileForm/EditProfileForm";
import { useFetch } from "../../hooks/useFetch";
import { profileService } from "../../services/profileService";
import "./EditProfile.scss";

function EditProfile() {
  // useFetch handles loading, error, and cleanup automatically.
  // Compare this to the old version that had 12 lines of useState +
  // useEffect + try/catch boilerplate.
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
          <h1>Edit Profile</h1>

          {loading ? (
            <div className="loading-state">
              <div className="spinner"></div>
              <p>Loading profile data...</p>
            </div>
          ) : (
            <EditProfileForm initialData={profile || {}} />
          )}
        </div>
      </div>
    </div>
  );
}

export default EditProfile;
