// hooks/usePostActions.ts
import { useState } from "react";
import { postService } from "../services/postService";
import { Post } from "../interfaces/postType";
import api from "../api/api";

export const usePostActions = (post: Post) => {
  // --- STATE FOR LIKES ---
  const [likesCount, setLikesCount] = useState(post.likes_count);
  const [isLiked, setIsLiked] = useState(post.is_liked);

  // --- STATE FOR COMMENTS ---
  const [showComments, setShowComments] = useState(false);
  const [commentText, setCommentText] = useState("");
  const [commentsCount, setCommentsCount] = useState(post.comments_count);

  // 1. Handle Like Click
  const handleLike = async () => {
    // Optimistic UI Update (Instantly change the screen)
    const newLikedState = !isLiked;
    setIsLiked(newLikedState);
    setLikesCount((prev) => (newLikedState ? prev + 1 : prev - 1));

    try {
      // NOTE: Ensure this URL matches your Django urls.py for nested routers!
      if (newLikedState) {
        await api.post(`/account/posts/${post.id}/likes/`);
      } else {
        await api.delete(`/account/posts/${post.id}/likes/`);
      }
    } catch (error) {
      console.error("Failed to toggle like", error);
      // Revert the UI if the server failed
      setIsLiked(!newLikedState);
      setLikesCount((prev) => (newLikedState ? prev - 1 : prev + 1));
    }
  };

  // 2. Handle Comment Submit
  const handleCommentSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!commentText.trim()) return;

    try {
      // NOTE: Ensure this URL matches your Django urls.py
      await api.post(`/account/posts/${post.id}/comments/`, {
        content: commentText, // Ensure this matches your CommentSerializer field
      });

      setCommentText(""); // Clear the input
      setCommentsCount((prev) => prev + 1); // Optimistically update count
    } catch (error) {
      console.error("Failed to post comment", error);
    }
  };

  const handleShowComments = async () => {};

  return {
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
  };
};
