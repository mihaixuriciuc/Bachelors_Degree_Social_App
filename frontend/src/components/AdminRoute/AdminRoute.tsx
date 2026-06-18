import { Navigate } from "react-router-dom";
import { ReactNode } from "react";
import { useAuth } from "../../hooks/useAuth";

/**
 * Like ProtectedRoute, but also requires the user to be staff (is_staff).
 *
 * - Not logged in  → redirect to /signin
 * - Logged in but not staff → redirect to /feed (they have no business here)
 * - Logged in and staff → render the dashboard
 *
 * This is the frontend half of the admin gate. The backend enforces it too
 * (IsAdminUser on every endpoint), so even if someone bypassed this, the API
 * would still return 403. Never rely on frontend checks alone for security —
 * this is just for UX (not showing a page that would fail anyway).
 */
export function AdminRoute({ children }: { children: ReactNode }) {
  const { user, loading } = useAuth();

  if (loading) {
    return <div className="page-loader">Loading...</div>;
  }

  if (!user) {
    return <Navigate to="/signin" replace />;
  }

  if (!user.is_staff) {
    return <Navigate to="/feed" replace />;
  }

  return <>{children}</>;
}
