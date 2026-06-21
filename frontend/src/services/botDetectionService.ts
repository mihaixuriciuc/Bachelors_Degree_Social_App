import api from "../api/api";
import {
  DashboardStats,
  FlaggedUser,
  BotEventItem,
} from "../interfaces/botDetectionType";

// All the admin dashboard API calls. Every endpoint behind here is
// staff-only on the backend (IsAdminUser), so a non-admin calling these
// would get a 403.
export const botDetectionService = {
  getStats: () => api.get<DashboardStats>("/bot-detection/stats/"),

  // showAll=true returns every user with their score, not just flagged ones.
  getFlagged: (showAll: boolean = false) =>
    api.get<FlaggedUser[]>(`/bot-detection/flagged/?all=${showAll}`),

  getEvents: () => api.get<BotEventItem[]>("/bot-detection/events/"),

  recompute: () => api.post("/bot-detection/recompute/"),

  clearFlag: (userId: number) =>
    api.post(`/bot-detection/clear-flag/${userId}/`),

  deleteUser: (userId: number) => api.delete(`/users/${userId}/delete/`),
};
