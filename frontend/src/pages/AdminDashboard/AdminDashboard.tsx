import { useEffect, useState, useCallback } from "react";
import { Link } from "react-router-dom";
import {
  DashboardStats,
  FlaggedUser,
  BotEventItem,
} from "../../interfaces/botDetectionType";
import { botDetectionService } from "../../services/botDetectionService";
import "./AdminDashboard.scss";

function AdminDashboard() {
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [flagged, setFlagged] = useState<FlaggedUser[]>([]);
  const [events, setEvents] = useState<BotEventItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [recomputing, setRecomputing] = useState(false);
  const [showAll, setShowAll] = useState(false);
  // Which user's reasons are expanded. null = none open.
  const [expandedId, setExpandedId] = useState<number | null>(null);

  const loadAll = useCallback(async () => {
    setLoading(true);
    try {
      const [statsRes, flaggedRes, eventsRes] = await Promise.all([
        botDetectionService.getStats(),
        botDetectionService.getFlagged(showAll),
        botDetectionService.getEvents(),
      ]);
      setStats(statsRes.data);
      setFlagged(flaggedRes.data);
      setEvents(eventsRes.data);
    } catch (err) {
      console.error("Failed to load dashboard", err);
    } finally {
      setLoading(false);
    }
  }, [showAll]);

  useEffect(() => {
    loadAll();
  }, [loadAll]);

  const handleRecompute = async () => {
    setRecomputing(true);
    try {
      await botDetectionService.recompute();
      await loadAll();
    } catch (err) {
      console.error("Recompute failed", err);
    } finally {
      setRecomputing(false);
    }
  };

  const handleClearFlag = async (userId: number) => {
    try {
      await botDetectionService.clearFlag(userId);
      setFlagged((prev) => prev.filter((u) => u.id !== userId));
    } catch (err) {
      console.error("Clear flag failed", err);
    }
  };
  const handleDeleteUser = async (userId: number, username: string) => {
    const confirmed = window.confirm(
      `Permanently delete "${username}"? This removes the account and all ` +
        `their posts, comments, and activity. This cannot be undone.`,
    );
    if (!confirmed) return;

    try {
      await botDetectionService.deleteUser(userId);
      // Remove from the table immediately.
      setFlagged((prev) => prev.filter((u) => u.id !== userId));
    } catch (err) {
      console.error("Delete failed", err);
    }
  };

  // Toggle the expanded reasons row.
  const toggleExpand = (userId: number) => {
    setExpandedId((current) => (current === userId ? null : userId));
  };

  // Map the risk tier to a CSS class for color-coding.
  const tierClass = (level: string) => {
    if (level === "likely_bot") return "tier-bot";
    if (level === "suspicious") return "tier-suspicious";
    return "tier-clean";
  };

  const tierLabel = (level: string) => {
    if (level === "likely_bot") return "Likely Bot";
    if (level === "suspicious") return "Suspicious";
    return "Clean";
  };

  return (
    <div className="admin-dashboard">
      <nav className="admin-nav">
        <h1 className="admin-logo">DOT8 — Admin</h1>
        <div className="admin-nav-actions">
          <button
            className="btn-recompute"
            onClick={handleRecompute}
            disabled={recomputing}
          >
            {recomputing ? "Recomputing..." : "↻ Recompute Scores"}
          </button>
          <Link to="/feed" className="btn-back-feed">
            Back to Feed
          </Link>
        </div>
      </nav>

      {loading ? (
        <p className="dashboard-status">Loading dashboard...</p>
      ) : (
        <div className="dashboard-content">
          {/* SECTION 1 — Overview stats */}
          <section className="stats-grid">
            <div className="stat-card">
              <span className="stat-value">{stats?.flagged_count ?? 0}</span>
              <span className="stat-label">Flagged Accounts</span>
            </div>
            <div className="stat-card">
              <span className="stat-value">{stats?.total_users ?? 0}</span>
              <span className="stat-label">Total Users</span>
            </div>
            <div className="stat-card">
              <span className="stat-value">{stats?.events_today ?? 0}</span>
              <span className="stat-label">Events (24h)</span>
            </div>
            <div className="stat-card">
              <span className="stat-value">{stats?.events_week ?? 0}</span>
              <span className="stat-label">Events (7d)</span>
            </div>
          </section>

          {/* Event-type breakdown */}
          {stats && stats.events_by_type.length > 0 && (
            <section className="breakdown">
              <h2>Events by Type</h2>
              <div className="breakdown-bars">
                {stats.events_by_type.map((row) => {
                  const max = Math.max(
                    ...stats.events_by_type.map((r) => r.count),
                  );
                  const width = max > 0 ? (row.count / max) * 100 : 0;
                  return (
                    <div key={row.event_type} className="breakdown-row">
                      <span className="breakdown-label">{row.event_type}</span>
                      <div className="breakdown-bar-track">
                        <div
                          className="breakdown-bar-fill"
                          style={{ width: `${width}%` }}
                        />
                      </div>
                      <span className="breakdown-count">{row.count}</span>
                    </div>
                  );
                })}
              </div>
            </section>
          )}

          {/* SECTION 2 — Flagged accounts table */}
          <section className="flagged-section">
            <div className="section-header">
              <h2>{showAll ? "All Accounts" : "Flagged Accounts"}</h2>
              <button
                className="btn-toggle"
                onClick={() => setShowAll((v) => !v)}
              >
                {showAll ? "Show flagged only" : "Show all accounts"}
              </button>
            </div>

            {flagged.length === 0 ? (
              <p className="empty-state">No accounts to show.</p>
            ) : (
              <table className="flagged-table">
                <thead>
                  <tr>
                    <th></th>
                    <th>Username</th>
                    <th>Score</th>
                    <th>Posts</th>
                    <th>Comments</th>
                    <th>Followers</th>
                    <th>Joined</th>
                    <th>Action</th>
                  </tr>
                </thead>
                <tbody>
                  {flagged.map((u) => (
                    <>
                      <tr
                        key={u.id}
                        className="clickable-row"
                        onClick={() => toggleExpand(u.id)}
                      >
                        <td className="expand-cell">
                          {u.flag_reasons && u.flag_reasons.length > 0
                            ? expandedId === u.id
                              ? "▼"
                              : "▶"
                            : ""}
                        </td>
                        <td>
                          <Link
                            to={`/users/${u.username}`}
                            className="user-link"
                            onClick={(e) => e.stopPropagation()}
                          >
                            {u.username}
                          </Link>
                        </td>
                        <td>
                          <span
                            className={`score-badge ${tierClass(u.risk_level)}`}
                          >
                            {u.bot_risk_score}
                          </span>
                        </td>
                        <td>
                          <span
                            className={`tier-pill ${tierClass(u.risk_level)}`}
                          >
                            {tierLabel(u.risk_level)}
                          </span>
                        </td>
                        <td>{u.post_count}</td>
                        <td>{u.comment_count}</td>
                        <td>{u.follower_count}</td>
                        <td>{new Date(u.date_joined).toLocaleDateString()}</td>
                        <td>
                          <div className="action-buttons">
                            <button
                              className="btn-clear"
                              onClick={(e) => {
                                e.stopPropagation();
                                handleClearFlag(u.id);
                              }}
                            >
                              Clear Flag
                            </button>
                            <button
                              className="btn-delete"
                              onClick={(e) => {
                                e.stopPropagation();
                                handleDeleteUser(u.id, u.username);
                              }}
                            >
                              Delete
                            </button>
                          </div>
                        </td>
                      </tr>

                      {/* Expanded reasons row */}
                      {expandedId === u.id &&
                        u.flag_reasons &&
                        u.flag_reasons.length > 0 && (
                          <tr key={`${u.id}-reasons`} className="reasons-row">
                            <td colSpan={8}>
                              <div className="reasons-box">
                                <span className="reasons-title">
                                  Why this score:
                                </span>
                                <ul className="reasons-list">
                                  {u.flag_reasons.map((r, i) => (
                                    <li key={i}>
                                      <span className="reason-text">
                                        {r.reason}
                                      </span>
                                      <span className="reason-points">
                                        +{r.points}
                                      </span>
                                    </li>
                                  ))}
                                </ul>
                              </div>
                            </td>
                          </tr>
                        )}
                    </>
                  ))}
                </tbody>
              </table>
            )}
          </section>

          {/* SECTION 3 — Recent events log */}
          <section className="events-section">
            <h2>Recent Events</h2>
            {events.length === 0 ? (
              <p className="empty-state">No events logged yet.</p>
            ) : (
              <table className="events-table">
                <thead>
                  <tr>
                    <th>Type</th>
                    <th>User</th>
                    <th>IP</th>
                    <th>Detail</th>
                    <th>Time</th>
                  </tr>
                </thead>
                <tbody>
                  {events.map((e) => (
                    <tr key={e.id}>
                      <td>
                        <span className="event-type">{e.event_label}</span>
                      </td>
                      <td>{e.username || "—"}</td>
                      <td>{e.ip_address || "—"}</td>
                      <td className="event-detail">{e.detail || "—"}</td>
                      <td>{new Date(e.created_at).toLocaleString()}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
          </section>
        </div>
      )}
    </div>
  );
}

export default AdminDashboard;
