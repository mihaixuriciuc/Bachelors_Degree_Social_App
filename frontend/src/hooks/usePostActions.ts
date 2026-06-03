import { useState } from "react";
import { Post } from "../interfaces/postType";
import { postService } from "../services/postService";

export const usePostActions = (post: Post) => {
  const [likesCount, setLikesCount] = useState(post.likes_count);
  const [isLiked, setIsLiked] = useState(post.is_liked);

  const handleLike = async () => {
    // Optimistic UI: update the screen immediately, then sync with the server.
    // If the server fails, we revert.
    const newLikedState = !isLiked;
    setIsLiked(newLikedState);
    setLikesCount((prev) => (newLikedState ? prev + 1 : prev - 1));

    try {
      if (newLikedState) {
        await postService.likePost(post.id);
      } else {
        await postService.unlikePost(post.id);
      }
    } catch (error) {
      console.error("Failed to toggle like", error);
      // Revert on failure
      setIsLiked(!newLikedState);
      setLikesCount((prev) => (newLikedState ? prev - 1 : prev + 1));
    }
  };

  return {
    isLiked,
    likesCount,
    handleLike,
  };
};
