import { Post } from "../../../interfaces/postType";
import { useCommentPost } from "../../../hooks/useCommentsPost";
import { CommentsHandler } from "../../../interfaces/commentType";
import "./CommentsTextField.scss";

function CommentsTextField({
  post,
  commentText,
  setCommentText,
  handleCommentSubmit,
}: CommentsHandler) {
  return (
    <div>
      <form className="comment-form" onSubmit={handleCommentSubmit}>
        <input
          type="text"
          placeholder="Write a comment..."
          value={commentText}
          onChange={(e) => setCommentText(e.target.value)}
          className="comment-input"
        />
        <button
          type="submit"
          className="btn-submit-comment"
          disabled={!commentText.trim()}
        >
          Post
        </button>
      </form>
    </div>
  );
}

export default CommentsTextField;
