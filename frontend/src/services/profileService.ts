import api from "../api/api";
import { UserProfile } from "../interfaces/userType";

interface UpdateSecurityPayload {
  first_name?: string;
  last_name?: string;
  username?: string;
  email?: string;
  new_password?: string;
  confirm_password?: string;
}

// Profile-related API calls.
// Notice that GET and PATCH live at slightly different URLs because the
// backend mounts them in different apps:
//   GET    /account/profile/        → apps.posts.urls (account-scoped)
//   PATCH  /profile/update/         → apps.user.urls
//   PATCH  /security/update/        → apps.user.urls
// Components don't need to know any of this — they just call the methods.
export const profileService = {
  getMine: () => api.get<UserProfile>("/account/profile/"), // only gets data, paranthesis empty, then the get with the interface so i know how the data looks like

  updateMine: (formData: FormData) =>
    api.patch<UserProfile>("/profile/update/", formData, {
      headers: { "Content-Type": "multipart/form-data" },
    }),

  updateSecurity: (payload: UpdateSecurityPayload) =>
    api.patch("/security/update/", payload),
};
