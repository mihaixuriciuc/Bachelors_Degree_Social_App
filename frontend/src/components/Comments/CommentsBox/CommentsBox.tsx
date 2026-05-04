import { Comment } from "../../../interfaces/commentType";
import CommentCard from "../Comment/CommentCard";
import { CommentBoxProps } from "../../../interfaces/commentType";
// We change the props to accept the data directly from the hook

function CommentBox({ comments, loading }: CommentBoxProps) {
  if (loading) return <div className="loading-small">Loading comments...</div>;

  return (
    <main className="comment-box-content">
      {comments.length > 0 ? (
        comments.map((comment) => (
          <CommentCard key={comment.id} comment={comment} />
        ))
      ) : (
        <p className="no-posts">No comments yet.</p>
      )}
    </main>
  );
}

export default CommentBox;
