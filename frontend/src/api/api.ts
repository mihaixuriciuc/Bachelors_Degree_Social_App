import axios from "axios";

// 1. Helper function to find a specific cookie by its name
function getCookie(name: string): string | null {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) {
    return parts.pop()?.split(";").shift() || null;
  }
  return null;
}

// 2. Create the central Axios instance
const api = axios.create({
  baseURL: "http://localhost:8000/api/v1",
  withCredentials: true, // This tells the browser to always send/receive our cookies 🍪
  headers: {
    "Content-Type": "application/json",
  },
});

// 3. The Interceptor: Our automatic security guard 🛡️
api.interceptors.request.use(
  (config) => {
    // Django only needs CSRF tokens for "unsafe" methods that change data
    const unsafeMethods = ["post", "put", "patch", "delete"];

    if (config.method && unsafeMethods.includes(config.method.toLowerCase())) {
      const csrfToken = getCookie("csrftoken");
      if (csrfToken) {
        config.headers["X-CSRFToken"] = csrfToken; // Attach the token!
      }
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  },
);

export default api;
