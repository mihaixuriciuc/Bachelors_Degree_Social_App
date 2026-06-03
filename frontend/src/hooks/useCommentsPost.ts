import { useEffect, useState } from "react";
import { Post } from "../interfaces/postType";
import { PostComment } from "../interfaces/commentType";
import { commentService } from "../services/commentService";

/**
 * Owns ALL comment state for a single post:
 *  - the list of comments (fetched lazily)
 *  - the loading state during fetch
 *  - the input text the user is typing
 *  - the count displayed on the button
 *  - whether the comments section is open
 *
 * Previously, this hook only handled the input + count, and CommentsBox
 * fetched the comments itself. That meant when a new comment was posted,
 * CommentsBox didn't know about it — you had to refresh the page to see it.
 *
 * Now everything lives in one place. When handleCommentSubmit succeeds,
 * we prepend the new comment to the local list (optimistic update) and
 * the CommentsBox re-renders automatically because it just receives the
 * list as a prop.
 *
 * The lazy-fetch (only loading comments when the user opens the section)
 * is important for the feed page — without it, loading the feed would
 * fetch comments for every visible post, even if the user never opens any.
 */
export const useCommentPost = (post: Post) => {
  const [showComments, setShowComments] = useState(false);
  const [commentText, setCommentText] = useState("");
  const [commentsCount, setCommentsCount] = useState(post.comments_count);
  const [comments, setComments] = useState<PostComment[]>([]);
  const [loading, setLoading] = useState(false);
  const [hasFetched, setHasFetched] = useState(false);

  // Only fetch the first time the user opens the comments section.
  // Subsequent toggles use the cached list.
  useEffect(() => {
    if (showComments && !hasFetched) {
      setLoading(true);
      commentService
        .getComments(post.id)
        .then((res) => {
          setComments(res.data);
          setHasFetched(true);
        })
        .catch((err) => {
          console.error("Error fetching comments:", err);
        })
        .finally(() => setLoading(false));
    }
  }, [showComments, hasFetched, post.id]);

  const handleCommentSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!commentText.trim()) return;

    try {
      const res = await commentService.createComment(post.id, commentText);
      // Optimistic update: insert the new comment at the top of the list
      // immediately, so the user sees it without waiting for a refetch.
      setComments((prev) => [res.data, ...prev]);
      setCommentText("");
      setCommentsCount((prev) => prev + 1);
    } catch (error) {
      console.error("Failed to post comment", error);
    }
  };

  return {
    showComments,
    setShowComments,
    comments,
    loading,
    commentsCount,
    commentText,
    setCommentText,
    handleCommentSubmit,
  };
};
