import { useState } from "react";
import api from "../../api/api";
import "./PostCard.scss";
import { Post } from "../../interfaces/postType";
import { usePostActions } from "../../hooks/usePostActions";

function PostCard({ post }: { post: Post }) {
  const date = new Date(post.created_at).toLocaleDateString();

  const {
    isLiked,
    likesCount,
    commentsCount,
    commentText,
    setCommentText,
    handleLike,
    handleCommentSubmit,
    setCommentsCount,
    setShowComments,
    showComments,
  } = usePostActions(post);
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
        {/* Dynamic Class for Liked State */}
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

      {/* The Comment Input Box (Toggles on/off) */}
      {showComments && (
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
      )}
    </div>
  );
}

export default PostCard;
