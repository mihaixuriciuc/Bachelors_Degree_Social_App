import { useEffect, useState } from "react";
import { PublicProfile } from "../interfaces/userType";
import { userService } from "../services/userService";

/**
 * Owns the follow state for the profile being viewed.
 *
 * It takes the fetched `profile` (which may be null while loading) and
 * syncs its local `isFollowing` / `followersCount` from it once it arrives.
 *
 * toggleFollow does an OPTIMISTIC update: it flips the UI immediately,
 * then calls the API. If the API call fails, it reverts. This makes the
 * button feel instant even on a slow connection.
 */
export const useFollow = (
  username: string | undefined,
  profile: PublicProfile | null,
) => {
  const [isFollowing, setIsFollowing] = useState(false);
  const [followersCount, setFollowersCount] = useState(0);

  // When the profile finishes loading, seed our local state from it.
  useEffect(() => {
    if (profile) {
      setIsFollowing(profile.is_following);
      setFollowersCount(profile.followers_count);
    }
  }, [profile]);

  const toggleFollow = async () => {
    if (!username) return;

    const wasFollowing = isFollowing;

    // Optimistic: update the UI before the request finishes.
    setIsFollowing(!wasFollowing);
    setFollowersCount((count) => (wasFollowing ? count - 1 : count + 1));

    try {
      if (wasFollowing) {
        await userService.unfollow(username);
      } else {
        await userService.follow(username);
      }
    } catch (err) {
      console.error("Follow toggle failed", err);
      // Revert on failure.
      setIsFollowing(wasFollowing);
      setFollowersCount((count) => (wasFollowing ? count + 1 : count - 1));
    }
  };

  return { isFollowing, followersCount, toggleFollow };
};
