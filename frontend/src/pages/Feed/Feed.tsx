import { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import PostCard from "../../components/PostCard/PostCard";
import { Post } from "../../interfaces/postType";
import { postService } from "../../services/postService";
import { useAuth } from "../../hooks/useAuth";
import "./Feed.scss";

function Feed() {
  const [posts, setPosts] = useState<Post[]>([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();
  const { logout } = useAuth();

  useEffect(() => {
    postService
      .listFeed()
      .then((res) => {
        setPosts(res.data);
      })
      .catch((err) => {
        console.error("Error fetching posts:", err);
      })
      .finally(() => setLoading(false));
  }, []);

  const handleLogout = async () => {
    await logout();
    navigate("/");
  };

  if (loading) return <div className="feed-status">Loading feed...</div>;

  return (
    <div className="feed-page">
      <nav className="feed-nav">
        <h1 className="logo-small">DOT8</h1>
        <div className="nav-actions">
          <Link to="/profile" className="btn-profile">
            Profile
          </Link>
          <button className="btn-logout" onClick={handleLogout}>
            Log out
          </button>
        </div>
      </nav>

      <main className="feed-content">
        {posts.length > 0 ? (
          posts.map((post) => <PostCard key={post.id} post={post} />)
        ) : (
          <p className="no-posts">
            No posts yet. Be the first to share something!
          </p>
        )}
      </main>
    </div>
  );
}

export default Feed;
