// hooks/usePostActions.ts
import { useState } from "react";
import { postService } from "../services/postService";
import { Post } from "../interfaces/postType";
import api from "../api/api";
import { commentService } from "../services/commentService";

export const usePostActions = (post: Post) => {
  // --- STATE FOR LIKES ---
  const [likesCount, setLikesCount] = useState(post.likes_count);
  const [isLiked, setIsLiked] = useState(post.is_liked);

  // 1. Handle Like Click
  const handleLike = async () => {
    // Optimistic UI Update (Instantly change the screen)
    const newLikedState = !isLiked;
    setIsLiked(newLikedState);
    setLikesCount((prev) => (newLikedState ? prev + 1 : prev - 1));

    try {
      // NOTE: Ensure this URL matches your Django urls.py for nested routers!
      if (newLikedState) {
        await postService.likePost(post.id);
      } else {
        await postService.unlikePost(post.id);
      }
    } catch (error) {
      console.error("Failed to toggle like", error);
      // Revert the UI if the server failed
      setIsLiked(!newLikedState);
      setLikesCount((prev) => (newLikedState ? prev - 1 : prev + 1));
    }
  };

  // 2. Handle Comment Submit

  return {
    isLiked,
    likesCount,
    handleLike,
  };
};
