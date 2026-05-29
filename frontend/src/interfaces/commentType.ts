import { Post } from "../interfaces/postType";

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

export interface CommentBoxProps {
  comments: Comment[];
  loading: boolean;
}
