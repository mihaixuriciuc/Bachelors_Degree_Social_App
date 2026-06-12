import api from "../api/api";
import { Post } from "../interfaces/postType";
import { PublicProfile, UserListItem } from "../interfaces/userType";

// Everything related to OTHER users: their profile, their posts,
// following/unfollowing them, and their follower/following lists.
export const userService = {
  getProfile: (username: string) =>
    api.get<PublicProfile>(`/users/${username}/`),

  // Note: posts live under /account/ because they belong to the posts app.
  getPosts: (username: string) =>
    api.get<Post[]>(`/account/users/${username}/posts/`),

  follow: (username: string) => api.post(`/users/${username}/follow/`),

  unfollow: (username: string) => api.delete(`/users/${username}/follow/`),

  getFollowers: (username: string) =>
    api.get<UserListItem[]>(`/users/${username}/followers/`),

  getFollowing: (username: string) =>
    api.get<UserListItem[]>(`/users/${username}/following/`),
  search: (query: string) =>
    api.get<UserListItem[]>(`/users/search/?q=${encodeURIComponent(query)}`),
};
