// The logged-in user's OWN profile (matches ProfileResponseSerializer).
export interface UserProfile {
  username: string;
  first_name: string;
  last_name: string;
  email: string;
  bio: string | null;
  profile_pic: string | null;
  website: string | null;
  followers_count: number;
  following_count: number;
}

// Another user's profile (matches PublicProfileSerializer).
// No email (privacy), but adds is_following so we know which button to show.
export interface PublicProfile {
  username: string;
  first_name: string;
  last_name: string;
  bio: string | null;
  profile_pic: string | null;
  website: string | null;
  followers_count: number;
  following_count: number;
  is_following: boolean;
}

// A compact user row for follower/following lists (matches UserListItemSerializer).
export interface UserListItem {
  username: string;
  first_name: string;
  profile_pic: string | null;
}
