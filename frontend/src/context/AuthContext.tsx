import React, { createContext, useState, useEffect, ReactNode } from "react";

interface User {
  username: string;
}

interface AuthContextType {
  user: User | null;
  loading: boolean;
  setUser: (user: User | null) => void;
}

export const AuthContext = createContext<AuthContextType | undefined>(
  undefined,
);

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  // This effect runs once when the app loads to check if the user is already logged in
  useEffect(() => {
    const checkAuth = async () => {
      try {
        // You'll eventually create a simple 'me' or 'profile' endpoint in Django
        // for this to call. For now, we set loading to false.
        setLoading(false);
      } catch (error) {
        setLoading(false);
      }
    };
    checkAuth();
  }, []);

  return (
    <AuthContext.Provider value={{ user, loading, setUser }}>
      {children}
    </AuthContext.Provider>
  );
};
