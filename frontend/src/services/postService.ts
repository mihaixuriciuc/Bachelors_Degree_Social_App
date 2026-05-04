// services/postService.ts
import api from "../api/api"; // your axios instance

export const postService = {
  likePost: (postId: number) => api.post(`/account/posts/${postId}/likes/`),

  unlikePost: (postId: number) => api.delete(`/account/posts/${postId}/likes/`),

};
