import api from "../api/api";

export const commentService = {
  createComment: (postId: number, content: string) =>
    api.post(`/account/posts/${postId}/comments/`, { content }),
  getComments: (postId: number) =>
    api.get(`/account/posts/${postId}/comments/`),
};
