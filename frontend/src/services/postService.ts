import api from "../api/api";
import { Post } from "../interfaces/postType";

// Post-related API calls. The old version only had like/unlike.
// Now everything that touches /posts goes through this service.
export const postService = {
  listFeed: () => api.get<Post[]>("/account/posts/"),

  listMine: () => api.get<Post[]>("/account/profile/posts/"),

  create: (formData: FormData) =>
    api.post<Post>("/account/posts/", formData, {
      headers: { "Content-Type": "multipart/form-data" },
    }),

  likePost: (postId: number) => api.post(`/account/posts/${postId}/likes/`),

  unlikePost: (postId: number) => api.delete(`/account/posts/${postId}/likes/`),
};
