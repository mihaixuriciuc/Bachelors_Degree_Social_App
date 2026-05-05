import { UserProfile } from "../../interfaces/userType";
import { Link } from "react-router-dom";
import "./ProfileHeader.scss";
import SettingsDropdown from "../SettingsDropdown/SettingsDropdown";

function ProfileHeader({ profile }: { profile: UserProfile }) {
  return (
    <header className="profile-header">
      <div className="profile-picture-container">
        <img
          src={profile.profile_picture || "https://via.placeholder.com/150"}
          alt={profile.username}
          className="profile-picture"
        />
      </div>
      <div className="profile-info">
        <h2 className="username">{profile.username}</h2>
        <p className="description">
          {profile.bio || "No description provided."}
        </p>
        <div className="profile-actions">
          {/* Use the class 'btn-secondary' so it matches the Settings button */}
          <Link to="/create-post" className="btn-secondary">
            Create Post
          </Link>
          <SettingsDropdown></SettingsDropdown>
        </div>
      </div>
    </header>
  );
}

export default ProfileHeader;
