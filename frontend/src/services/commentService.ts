import api from "../api/api";
import { PostComment } from "../interfaces/commentType";

export const commentService = {
  getComments: (postId: number) =>
    api.get<PostComment[]>(`/account/posts/${postId}/comments/`),

  createComment: (postId: number, content: string) =>
    api.post<PostComment>(`/account/posts/${postId}/comments/`, { content }),  // a post request, here post comment is the is used 
};
