import { PostComment } from "../../../interfaces/commentType";
import CommentCard from "../Comment/CommentCard";

interface CommentBoxProps {
  comments: PostComment[];
  loading: boolean;
}

/**
 * Pure presentation component.
 *
 * Before: fetched its own comments and had its own loading state.
 * That meant the parent component (PostCard) had no way to know
 * when new comments were added — it lived inside CommentsBox.
 *
 * Now: receives comments and loading as props. The parent owns the
 * state via useCommentPost(). When a new comment is added, the parent
 * updates its state and we automatically re-render with the new list.
 *
 * This follows the "lifting state up" pattern: state lives at the
 * lowest common ancestor of all components that need it.
 */
function CommentBox({ comments, loading }: CommentBoxProps) {
  if (loading) return <div className="feed-status">Loading comments...</div>;

  return (
    <main className="comment-box-content">
      {comments.length > 0 ? (
        comments.map((comment) => (
          <CommentCard key={comment.id} comment={comment} />
        ))
      ) : (
        <p className="no-posts">
          No comments yet. Be the first to share something!
        </p>
      )}
    </main>
  );
}

export default CommentBox;