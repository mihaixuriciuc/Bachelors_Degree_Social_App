import api from "../api/api";
import { Post } from "../interfaces/postType";
import { Paginated } from "../interfaces/paginatedType";

export const postService = {
  // The feed is now paginated. It returns { count, next, previous, results }.
  // `page` defaults to 1 (the first page).
  listFeed: (page: number = 1) =>
    api.get<Paginated<Post>>(`/account/posts/?page=${page}`),

  // The profile grids use a function-based view, so these stay plain arrays.
  listMine: () => api.get<Post[]>("/account/profile/posts/"),

  create: (formData: FormData) =>
    api.post<Post>("/account/posts/", formData, {
      headers: { "Content-Type": "multipart/form-data" },
    }),

  remove: (postId: number) => api.delete(`/account/posts/${postId}/`),

  likePost: (postId: number) => api.post(`/account/posts/${postId}/likes/`),

  unlikePost: (postId: number) => api.delete(`/account/posts/${postId}/likes/`),
};
