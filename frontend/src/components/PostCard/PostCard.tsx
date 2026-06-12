import { Link } from "react-router-dom";
import { Post } from "../../interfaces/postType";
import { usePostActions } from "../../hooks/usePostActions";
import { useCommentPost } from "../../hooks/useCommentsPost";
import { useAuth } from "../../hooks/useAuth";
import { postService } from "../../services/postService";
import CommentsTextField from "../Comments/CommentsTextField/CommentsTextField";
import CommentBox from "../Comments/CommentsBox/CommentsBox";
import "./PostCard.scss";

interface PostCardProps {
  post: Post;
  // Optional callback so the parent (Feed, Profile) can remove this post
  // from its list when it's deleted. Optional because some places that
  // render a PostCard (like the post modal) don't manage a list.
  onDeleted?: (postId: number) => void;
}

function PostCard({ post, onDeleted }: PostCardProps) {
  const date = new Date(post.created_at).toLocaleDateString();
  const { user } = useAuth();

  const { isLiked, likesCount, handleLike } = usePostActions(post);

  const {
    comments,
    loading,
    commentsCount,
    commentText,
    setCommentText,
    handleCommentSubmit,
    setShowComments,
    showComments,
  } = useCommentPost(post);

  // Show the delete button only on the current user's own posts.
  // post.author is a username string, so we compare against the logged-in
  // user's username.
  const isOwnPost = user?.username === post.author;

  const handleDelete = async () => {
    // A simple confirmation so a misclick doesn't destroy a post.
    const confirmed = window.confirm(
      "Are you sure you want to delete this post? This cannot be undone.",
    );
    if (!confirmed) return;

    try {
      await postService.remove(post.id);
      // Tell the parent to remove this post from its list.
      onDeleted?.(post.id);
    } catch (err) {
      console.error("Failed to delete post", err);
      alert("Could not delete the post. Please try again.");
    }
  };

  return (
    <div className="post-card">
      <div className="post-header">
        <Link to={`/users/${post.author}`} className="author">
          {post.author}
        </Link>
        <span className="date">{date}</span>
      </div>

      <div className="post-body">
        <h2 className="post-title">{post.title}</h2>
        <p className="post-content">{post.content}</p>
        {post.image && (
          <div className="post-image-container">
            <img src={post.image} alt={post.title} className="post-image" />
          </div>
        )}
      </div>

      <div className="post-footer">
        <button
          className={`btn-action ${isLiked ? "liked" : ""}`}
          onClick={handleLike}
        >
          {isLiked ? "❤️ Liked" : "🤍 Like"}{" "}
          {likesCount > 0 && `(${likesCount})`}
        </button>

        <button
          className="btn-action"
          onClick={() => setShowComments(!showComments)}
        >
          💬 Comment {commentsCount > 0 && `(${commentsCount})`}
        </button>

        {isOwnPost && (
          <button className="btn-action btn-delete" onClick={handleDelete}>
            🗑️ Delete
          </button>
        )}
      </div>

      {showComments && (
        <div>
          <CommentBox comments={comments} loading={loading} />
          <CommentsTextField
            post={post}
            commentText={commentText}
            setCommentText={setCommentText}
            handleCommentSubmit={handleCommentSubmit}
          />
        </div>
      )}
    </div>
  );
}

export default PostCard;
