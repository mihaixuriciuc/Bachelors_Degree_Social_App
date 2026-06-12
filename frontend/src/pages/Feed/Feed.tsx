import { useNavigate, Link } from "react-router-dom";
import PostCard from "../../components/PostCard/PostCard";
import SearchBar from "../../components/SearchBar/SearchBar";
import { useAuth } from "../../hooks/useAuth";
import { useInfiniteFeed } from "../../hooks/useInfiniteFeed";
import { useInfiniteScroll } from "../../hooks/useInfiniteScroll";
import "./Feed.scss";

function Feed() {
  const navigate = useNavigate();
  const { logout } = useAuth();

  const { posts, loading, hasMore, loadMore, removePost } = useInfiniteFeed();

  // The sentinel ref goes on an invisible div at the bottom of the list.
  // When it scrolls into view, loadMore fires. We only keep observing while
  // there are more pages (hasMore).
  const sentinelRef = useInfiniteScroll(loadMore, hasMore);

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

        {/* Empty state — only show once we've finished loading and found nothing */}
        {!loading && posts.length === 0 && (
          <p className="no-posts">
            No posts yet. Be the first to share something!
          </p>
        )}

        {/* Loading indicator for any page fetch */}
        {loading && <p className="feed-status">Loading...</p>}

        {/* The invisible sentinel. When it scrolls into view, the next
            page loads. Rendered only while there are more pages. */}
        {hasMore && <div ref={sentinelRef} style={{ height: "1px" }} />}

        {/* End-of-feed message */}
        {!hasMore && posts.length > 0 && (
          <p className="feed-status">You're all caught up.</p>
        )}
      </main>
    </div>
  );
}

export default Feed;
