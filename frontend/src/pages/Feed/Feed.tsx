import { useNavigate, Link } from "react-router-dom";
import PostCard from "../../components/PostCard/PostCard";
import SearchBar from "../../components/SearchBar/SearchBar";
import { useAuth } from "../../hooks/useAuth";
import { usePaginatedFeed } from "../../hooks/usePaginatedFeed";
import "./Feed.scss";

function Feed() {
  const navigate = useNavigate();
  const { logout, user } = useAuth();

  const { posts, loading, hasMore, loadMore, removePost } = usePaginatedFeed();

  const handleLogout = async () => {
    await logout();
    navigate("/");
  };

  return (
    <div className="feed-page">
      <nav className="feed-nav">
        <h1 className="logo-small">DOT8</h1>

        <SearchBar />

        <div className="nav-actions">
          {user?.is_staff && (
            <Link to="/admin" className="btn-dashboard">
              Dashboard
            </Link>
          )}

          <Link to="/profile" className="btn-profile">
            Profile
          </Link>
          <button className="btn-logout" onClick={handleLogout}>
            Log out
          </button>
        </div>
      </nav>

      <main className="feed-content">
        {posts.map((post) => (
          <PostCard key={post.id} post={post} onDeleted={removePost} />
        ))}

        {/* Empty state — only after the first load finishes with no posts */}
        {!loading && posts.length === 0 && (
          <p className="no-posts">
            No posts yet. Be the first to share something!
          </p>
        )}

        {/* Load More button — shown while there are more pages to fetch. */}
        {hasMore && posts.length > 0 && (
          <button
            className="btn-load-more"
            onClick={loadMore}
            disabled={loading}
          >
            {loading ? "Loading..." : "Load More Posts"}
          </button>
        )}

        {/* First-load spinner (before any posts exist yet) */}
        {loading && posts.length === 0 && (
          <p className="feed-status">Loading...</p>
        )}

        {/* End-of-feed message */}
        {!hasMore && posts.length > 0 && (
          <p className="feed-status">You're all caught up.</p>
        )}
      </main>
    </div>
  );
}

export default Feed;
