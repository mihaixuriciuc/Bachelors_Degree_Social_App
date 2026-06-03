import { Post } from "../../interfaces/postType";
import { usePostActions } from "../../hooks/usePostActions";
import { useCommentPost } from "../../hooks/useCommentsPost";
import CommentsTextField from "../Comments/CommentsTextField/CommentsTextField";
import CommentBox from "../Comments/CommentsBox/CommentsBox";
import "./PostCard.scss";

function PostCard({ post }: { post: Post }) {
  const date = new Date(post.created_at).toLocaleDateString();

  const { isLiked, likesCount, handleLike } = usePostActions(post);

  // useCommentPost now returns everything related to comments:
  // the list, loading state, count, input value, submit handler,
  // and the show/hide toggle.
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

  return (
    <div className="post-card">
      <div className="post-header">
        <span className="author">{post.author}</span>
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
