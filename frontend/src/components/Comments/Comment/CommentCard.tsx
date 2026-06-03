import { PostComment } from "../../../interfaces/commentType";
import "./Comment.scss";

function CommentCard({ comment }: { comment: PostComment }) {
  const date = new Date(comment.created_at).toLocaleDateString();

  return (
    <div className="comment-object">
      <div className="comment-header">
        <span className="author">{comment.author}</span>
        <span className="date">{date}</span>
      </div>
      <div>
        <p className="comment-content">{comment.content}</p>
      </div>
    </div>
  );
}

export default CommentCard;
