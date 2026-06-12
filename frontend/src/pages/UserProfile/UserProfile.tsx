import { useEffect, useState } from "react";
import { useParams, useNavigate, Link } from "react-router-dom";
import { Post } from "../../interfaces/postType";
import ProfileHeader from "../../components/ProfileHeader/ProfileHeader";
import PostsGrid from "../../components/PostsGrid/PostsGrid";
import PostCard from "../../components/PostCard/PostCard";
import FollowListModal from "../../components/FollowListModal/FollowListModal";
import { useFetch } from "../../hooks/useFetch";
import { useFollow } from "../../hooks/useFollow";
import { useFollowListModal } from "../../hooks/useFollowListModal";
import { useAuth } from "../../hooks/useAuth";
import { userService } from "../../services/userService";
// Reuse the Profile page layout (top nav, modal overlay, status text).
import "../Profile/Profile.scss";

function UserProfile() {
  const { username } = useParams<{ username: string }>();
  const navigate = useNavigate();
  const { user: currentUser } = useAuth();
  const [selectedPost, setSelectedPost] = useState<Post | null>(null);

  // Re-fetch whenever the username in the URL changes (e.g. navigating from
  // one profile to another via a follower list).
  const { data: profile, loading: profileLoading } = useFetch(
    () => userService.getProfile(username!),
    [username],
  );
  const { data: posts, loading: postsLoading } = useFetch(
    () => userService.getPosts(username!),
    [username],
  );

  const { isFollowing, followersCount, toggleFollow } = useFollow(
    username,
    profile,
  );

  const followModal = useFollowListModal(username);

  // If you land on your own profile via /users/<you>, send you to /profile
  // where you have edit controls (and no nonsensical "follow yourself" button).
  useEffect(() => {
    if (currentUser && username === currentUser.username) {
      navigate("/profile", { replace: true });
    }
  }, [currentUser, username, navigate]);

  if (profileLoading) {
    return <div className="profile-status">Loading profile...</div>;
  }
  if (!profile) {
    return <div className="profile-status">User not found.</div>;
  }

  return (
    <div className="profile-page">
      <nav className="profile-top-nav">
        <button className="btn-back" onClick={() => navigate(-1)}>
          &larr; Back
        </button>
        <Link to="/feed" className="logo-link">
          <h1 className="logo-small">DOT8</h1>
        </Link>
        <div className="spacer"></div>
      </nav>

      <ProfileHeader
        username={profile.username}
        profilePic={profile.profile_pic}
        bio={profile.bio}
        followersCount={followersCount}
        followingCount={profile.following_count}
        actions={
          <button
            className={`btn-follow ${isFollowing ? "following" : ""}`}
            onClick={toggleFollow}
          >
            {isFollowing ? "Following" : "Follow"}
          </button>
        }
        onFollowersClick={() => followModal.open("followers")}
        onFollowingClick={() => followModal.open("following")}
      />

      {postsLoading ? (
        <p className="no-posts">Loading posts...</p>
      ) : (
        <PostsGrid posts={posts || []} onPostClick={setSelectedPost} />
      )}

      {selectedPost && (
        <div
          className="post-modal-overlay"
          onClick={() => setSelectedPost(null)}
        >
          <div
            className="post-modal-content"
            onClick={(e) => e.stopPropagation()}
          >
            <button className="btn-close" onClick={() => setSelectedPost(null)}>
              ✖
            </button>
            <PostCard post={selectedPost} />
          </div>
        </div>
      )}

      {followModal.modalType && (
        <FollowListModal
          title={
            followModal.modalType === "followers" ? "Followers" : "Following"
          }
          users={followModal.users}
          loading={followModal.loading}
          onClose={followModal.close}
        />
      )}
    </div>
  );
}

export default UserProfile;
