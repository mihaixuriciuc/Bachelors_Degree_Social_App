import { useState } from "react";
import { UserListItem } from "../interfaces/userType";
import { userService } from "../services/userService";

/**
 * Manages the followers/following modal.
 *
 * Both the own Profile page and the UserProfile page show the same kind of
 * list, so this hook lives in one place and is shared by both (DRY).
 *
 * The list is fetched lazily — only when the modal is actually opened —
 * so visiting a profile doesn't load every follower up front.
 */
export const useFollowListModal = (username: string | undefined) => {
  const [modalType, setModalType] = useState<"followers" | "following" | null>(
    null,
  );
  const [users, setUsers] = useState<UserListItem[]>([]);
  const [loading, setLoading] = useState(false);

  const open = async (type: "followers" | "following") => {
    if (!username) return;

    setModalType(type);
    setLoading(true);
    setUsers([]);

    try {
      const res =
        type === "followers"
          ? await userService.getFollowers(username)
          : await userService.getFollowing(username);
      setUsers(res.data);
    } catch (err) {
      console.error("Failed to load follow list", err);
    } finally {
      setLoading(false);
    }
  };

  const close = () => setModalType(null);

  return { modalType, users, loading, open, close };
};
