import { UserProfile } from "../../interfaces/userType";
import "./ProfileHeader.scss";
import { Link } from "react-router-dom";

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
          <Link
            to="/create-post"
            className="btn-primary"
            style={{
              textDecoration: "none",
              display: "inline-block",
              textAlign: "center",
            }}
          >
            Create Post
          </Link>
          <button className="btn-secondary">Settings</button>
        </div>
      </div>
    </header>
  );
}

export default ProfileHeader;
