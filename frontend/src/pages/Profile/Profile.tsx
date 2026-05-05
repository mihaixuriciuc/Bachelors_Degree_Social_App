import { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom"; // 👈 Import Link and useNavigate
import api from "../../api/api";
import { Post } from "../../interfaces/postType";
import { UserProfile } from "../../interfaces/userType";
import ProfileHeader from "../../components/ProfileHeader/ProfileHeader";
import PostsGrid from "../../components/PostsGrid/PostsGrid";
import PostCard from "../../components/PostCard/PostCard";
import "./Profile.scss";

function Profile() {
  const navigate = useNavigate(); // 👈 Initialize navigate
  const [profile, setProfile] = useState<UserProfile | null>(null);
  const [posts, setPosts] = useState<Post[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedPost, setSelectedPost] = useState<Post | null>(null);

  useEffect(() => {
    const fetchProfileData = async () => {
      try {
        const profileRes = await api.get("/account/profile/");
        const postsRes = await api.get("/account/profile/posts/");
        setProfile(profileRes.data);
        setPosts(postsRes.data);
      } catch (err) {
        console.error("Error fetching profile data:", err);
      } finally {
        setLoading(false);
      }
    };

    fetchProfileData();
  }, []);

  if (loading) return <div className="profile-status">Loading profile...</div>;
  if (!profile) return <div className="profile-status">Profile not found.</div>;

  return (
    <div className="profile-page">
      {/* 👇 NEW TOP NAVIGATION 👇 */}
      <nav className="profile-top-nav">
        <button className="btn-back" onClick={() => navigate("/feed")}>
          &larr; Back
        </button>
        <Link to="/feed" className="logo-link">
          <h1 className="logo-small">DOT8</h1>
        </Link>
        <div className="spacer"></div> {/* Keeps the logo perfectly centered */}
      </nav>

      <ProfileHeader profile={profile} />
      <PostsGrid posts={posts} onPostClick={setSelectedPost} />

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
