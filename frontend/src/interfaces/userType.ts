// Matches the fields returned by backend ProfileResponseSerializer.
// All fields the backend exposes need to live here so TypeScript can
// type-check our usage across components.
export interface UserProfile {
  username: string;
  first_name: string;
  last_name: string;
  email: string;
  bio: string | null;
  profile_pic: string | null;
  website: string | null;
}
