import api from "../api/api";

interface SignUpPayload {
  username: string;
  email: string;
  password: string;
  confirm_password: string;
  first_name?: string;
  last_name?: string;
}

interface SignInPayload {
  username: string;
  password: string;
}

// All auth-related API calls in one place.
// Components import `authService` and call methods on it — they never
// touch the `api` instance directly. If the backend URL ever changes,
// you update one line here instead of grep-ing through 10 components.
export const authService = {
  signUp: (data: SignUpPayload) => api.post("/signUp/", data),

  signIn: (data: SignInPayload) => api.post("/signIn/", data),

  logout: () => api.post("/logout/"),

  activate: (uid: string, token: string) =>
    api.post(`/activate/${uid}/${token}/`),

  requestPasswordReset: (email: string) =>
    api.post("/password-reset/request/", { email }),

  confirmPasswordReset: (uid: string, token: string, newPassword: string) =>
    api.post(`/password-reset/confirm/${uid}/${token}/`, {
      new_password: newPassword,
    }),
};