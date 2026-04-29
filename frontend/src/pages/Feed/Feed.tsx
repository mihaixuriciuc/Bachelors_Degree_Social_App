import { useEffect, useState } from "react";
import api from "../../api/api";
import PostCard from "../../components/PostCard/PostCard";
import "./Feed.scss";

function Feed() {
  const [posts, setPosts] = useState([]);
  const [loading, setLoading] = useState(true);

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
        <button
          className="btn-logout"
          onClick={() => {
            /* handle logout */
          }}
        >
          Log out
        </button>
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
