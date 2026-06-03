import { createContext, useState, useEffect, ReactNode } from "react";
import { authService } from "../services/authService";
import { profileService } from "../services/profileService";
import { UserProfile } from "../interfaces/userType";

interface AuthContextType {
  user: UserProfile | null;
  loading: boolean;
  refreshUser: () => Promise<void>;
  logout: () => Promise<void>;
}

export const AuthContext = createContext<AuthContextType | undefined>(
  undefined,
);

/**
 * Centralizes authentication state for the whole app.
 *
 * The old version had an empty useEffect that just set loading=false.
 * The `user` state was never populated, so other components couldn't
 * tell who was logged in.
 *
 * Now:
 *  - On app mount, we call profileService.getMine() to hydrate the user.
 *  - If it fails (401), user stays null — that means "not logged in".
 *  - logout() is centralized here so Feed, SettingsDropdown, and anywhere
 *    else can call it without duplicating the API + clear-state logic.
 *  - refreshUser() lets SignInForm trigger a refetch after login succeeds.
 */
export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [user, setUser] = useState<UserProfile | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  const refreshUser = async () => {
    try {
      const res = await profileService.getMine();
      setUser(res.data);
    } catch {
      // 401 or network error = treat as not logged in.
      setUser(null);
    }
  };

  const logout = async () => {
    try {
      await authService.logout();
    } finally {
      // Always clear local state even if the request fails.
      // Otherwise a network error would leave the UI thinking the user
      // is still logged in.
      setUser(null);
    }
  };

  useEffect(() => {
    refreshUser().finally(() => setLoading(false));
  }, []);

  return (
    <AuthContext.Provider value={{ user, loading, refreshUser, logout }}>
      {children}
    </AuthContext.Provider>
  );
};
