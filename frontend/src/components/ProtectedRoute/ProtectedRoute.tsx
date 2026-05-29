import { Navigate } from "react-router-dom";
import { ReactNode } from "react";
import { useAuth } from "../../hooks/useAuth";

/**
 * Wraps any route that requires a logged-in user.
 *
 * Without this, the only thing stopping an anonymous user from visiting
 * /feed or /profile is that the API calls would fail with 401. They'd
 * still see the layout briefly before errors fire — confusing UX.
 *
 * With this wrapper, anonymous users get sent to /signin immediately.
 *
 * Usage in App.tsx:
 *   <Route path="/feed" element={
 *     <ProtectedRoute><Feed /></ProtectedRoute>
 *   } />
 */
export function ProtectedRoute({ children }: { children: ReactNode }) {
  const { user, loading } = useAuth();

  // While AuthContext is checking who you are, show a placeholder.
  // Without this, the redirect below would fire before the API call
  // finishes — kicking real users out to /signin every page load.
  if (loading) {
    return <div className="page-loader">Loading...</div>;
  }

  if (!user) {
    // `replace` swaps the URL in history so the back button doesn't
    // bring the user back to the protected page they just got bounced from.
    return <Navigate to="/signin" replace />;
  }

  return <>{children}</>;
}
