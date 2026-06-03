import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { Post } from "../../interfaces/postType";
import ProfileHeader from "../../components/ProfileHeader/ProfileHeader";
import PostsGrid from "../../components/PostsGrid/PostsGrid";
import PostCard from "../../components/PostCard/PostCard";
import { useFetch } from "../../hooks/useFetch";
import { profileService } from "../../services/profileService";
import { postService } from "../../services/postService";
import "./Profile.scss";

function Profile() {
  const navigate = useNavigate();
  const [selectedPost, setSelectedPost] = useState<Post | null>(null);

  // Two parallel fetches — both run on mount, both have their own
  // loading state. We render the page once the profile is ready;
  // the posts grid will show its own loading state if needed.
  const { data: profile, loading: profileLoading } = useFetch(() =>
    profileService.getMine(),
  );
  const { data: posts, loading: postsLoading } = useFetch(() =>
    postService.listMine(),
  );

  if (profileLoading) {
    return <div className="profile-status">Loading profile...</div>;
  }
  if (!profile) {
    return <div className="profile-status">Profile not found.</div>;
  }

  return (
    <div className="profile-page">
      <nav className="profile-top-nav">
        <button className="btn-back" onClick={() => navigate("/feed")}>
          &larr; Back
        </button>
        <Link to="/feed" className="logo-link">
          <h1 className="logo-small">DOT8</h1>
        </Link>
        <div className="spacer"></div>
      </nav>

      <ProfileHeader profile={profile} />

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
    </div>
  );
}

export default Profile;
