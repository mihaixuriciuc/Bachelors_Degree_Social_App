// Matches the dashboard_stats endpoint.
export interface DashboardStats {
  flagged_count: number;
  total_users: number;
  events_today: number;
  events_week: number;
  events_by_type: { event_type: string; count: number }[];
}

// One reason in a user's score breakdown.
export interface FlagReason {
  reason: string;
  points: number;
}

// Matches FlaggedUserSerializer — a row in the flagged-accounts table.
export interface FlaggedUser {
  id: number;
  username: string;
  email: string;
  bot_risk_score: number;
  is_flagged: boolean;
  flag_reasons: FlagReason[]; // the breakdown of why this score
  date_joined: string;
  is_active: boolean;
  post_count: number;
  comment_count: number;
  follower_count: number;
}

// Matches BotEventSerializer — a row in the events log.
export interface BotEventItem {
  id: number;
  username: string | null;
  event_type: string;
  event_label: string;
  ip_address: string | null;
  detail: string;
  created_at: string;
}
