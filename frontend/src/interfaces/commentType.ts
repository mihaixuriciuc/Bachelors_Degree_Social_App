import { Post } from "./postType";

// Renamed from `Comment` to `PostComment` so it doesn't shadow the
// built-in DOM `Comment` type (representing HTML comments like <!-- -->).
export interface PostComment {
  id: number;
  author: string;
  content: string;
  created_at: string;
  post_id: number;
}

export interface CommentsHandler {
  post: Post;
  commentText: string;
  setCommentText: (newText: string) => void;
  handleCommentSubmit: (e: React.FormEvent) => void;
}

// CommentBoxProps was removed — it referenced the global `Comment` type
// (HTML comments) by accident, which was unrelated to post comments.
// CommentBox now declares its own props inline because they're trivial.
