import { ReactNode } from "react";
import "./ProfileHeader.scss";

interface ProfileHeaderProps {
  username: string;
  profilePic: string | null;
  bio: string | null;
  followersCount: number;
  followingCount: number;
  // `actions` is a slot: the own Profile passes Create Post + Settings,
  // the UserProfile passes a Follow button. This keeps ProfileHeader
  // reusable without it knowing anything about who's viewing it.
  actions: ReactNode;
  onFollowersClick: () => void;
  onFollowingClick: () => void;
}

function ProfileHeader({
  username,
  profilePic,
  bio,
  followersCount,
  followingCount,
  actions,
  onFollowersClick,
  onFollowingClick,
}: ProfileHeaderProps) {
  return (
    <header className="profile-header">
      <div className="profile-picture-container">
        <img
          src={profilePic || "https://via.placeholder.com/150"}
          alt={username}
          className="profile-picture"
        />
      </div>

      <div className="profile-info">
        <h2 className="username">{username}</h2>

        <div className="follow-stats">
          <button className="stat" onClick={onFollowersClick}>
            <span className="count">{followersCount}</span> Followers
          </button>
          <button className="stat" onClick={onFollowingClick}>
            <span className="count">{followingCount}</span> Following
          </button>
        </div>

        <p className="description">{bio || "No description provided."}</p>

        <div className="profile-actions">{actions}</div>
      </div>
    </header>
  );
}

export default ProfileHeader;
