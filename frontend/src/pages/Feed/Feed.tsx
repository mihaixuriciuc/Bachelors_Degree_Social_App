import { useEffect, useState } from "react";
import api from "../../api/api";
import PostCard from "../../components/PostCard/PostCard";
import "./Feed.scss";
import { Link } from "react-router-dom"; // ADD THIS IMPORT
import { useNavigate } from "react-router-dom";

function Feed() {
  const [posts, setPosts] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    // Replace with your actual backend endpoint from urls.py
    api
      .get("/account/posts/")
      .then((res) => {
        setPosts(res.data);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Error fetching posts:", err);
        setLoading(false);
      });
  }, []);

  if (loading) return <div className="feed-status">Loading feed...</div>;

  return (
    <div className="feed-page">
      <nav className="feed-nav">
        <h1 className="logo-small">DOT8</h1>

        {/* REPLACE existing btn-logout WITH this nav-actions div */}
        <div className="nav-actions">
          <Link to="/profile" className="btn-profile">
            Profile
          </Link>
          <button
            className="btn-logout"
            onClick={async () => {
              try {
                await api.post("/logout"); // Tells Django to delete the cookies
                navigate("/"); // Redirects to Home
              } catch (err) {
                console.error("Logout failed", err);
              }
            }}
          >
            Log out
          </button>
        </div>
      </nav>

      <main className="feed-content">
        {posts.length > 0 ? (
          posts.map((post: any) => <PostCard key={post.id} post={post} />)
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
