import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import api from "../../api/api";
import EditProfileForm from "../../components/EditProfileForm/EditProfileForm";
import "./EditProfile.scss";

function EditProfile() {
  const [initialData, setInitialData] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Fetch the current profile data to pre-fill the form
    const fetchProfile = async () => {
      try {
        const response = await api.get("/account/profile/");
        setInitialData(response.data);
      } catch (err) {
        console.error("Failed to load profile data", err);
      } finally {
        setLoading(false);
      }
    };
    fetchProfile();
  }, []);

  return (
    <div className="edit-profile-page">
      {/* Top Navigation with Back Button */}
      <nav className="top-nav">
        <Link to="/profile" className="btn-back-minimal">
          <span className="arrow">&larr;</span> Back to Profile
        </Link>
      </nav>

      {/* Main Content Wrapper */}
      <div className="content-wrapper">
        <div className="form-container">
          <h1>Edit Profile</h1>

          {loading ? (
            <div className="loading-state">
              <div className="spinner"></div>
              <p>Loading profile data...</p>
            </div>
          ) : (
            <EditProfileForm initialData={initialData || {}} />
          )}
        </div>
      </div>
    </div>
  );
}

export default EditProfile;
