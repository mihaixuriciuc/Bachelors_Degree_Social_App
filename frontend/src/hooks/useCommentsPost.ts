import { useState, useEffect } from "react";
import { Comment } from "../interfaces/commentType";
import { Post } from "../interfaces/postType";
import { commentService } from "../services/commentService";

export const useCommentPost = (post: Post) => {
  const [showComments, setShowComments] = useState(false);
  const [commentText, setCommentText] = useState("");
  const [comments, setComments] = useState<Comment[]>([]); // New state for the list
  const [commentsCount, setCommentsCount] = useState(post.comments_count);
  const [loading, setLoading] = useState(false);

  // Fetch comments when the user toggles the box open
  useEffect(() => {
    if (showComments) {
      setLoading(true);
      commentService
        .getComments(post.id)
        .then((res) => {
          setComments(res.data);
          setLoading(false);
        })
        .catch((err) => {
          console.error("Error fetching comments:", err);
          setLoading(false);
        });
    }
  }, [showComments, post.id]);

  const handleCommentSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!commentText.trim()) return;

    try {
      const response = await commentService.createComment(post.id, commentText);

      // SYNTAX EXPLANATION:
      // We use the functional update (prev => [...prev, new]) to ensure we don't
      // lose comments if the state updates rapidly. We append the new comment
      // returned from the Django server to our local array.
      setComments((prev) => [...prev, response.data]);

      setCommentText("");
      setCommentsCount((prev) => prev + 1);
    } catch (error) {
      console.error("Failed to post comment", error);
    }
  };

  return {
    comments,
    loading,
    commentsCount,
    commentText,
    setCommentText,
    handleCommentSubmit,
    setShowComments,
    showComments,
  };
};
