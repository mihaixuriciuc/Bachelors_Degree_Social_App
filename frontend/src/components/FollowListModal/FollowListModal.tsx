import { Link } from "react-router-dom";
import { UserListItem } from "../../interfaces/userType";
import "./FollowListModal.scss";

interface FollowListModalProps {
  title: string;
  users: UserListItem[];
  loading: boolean;
  onClose: () => void;
}

/**
 * Pure presentation component. Receives the list + loading state from the
 * parent (via useFollowListModal) and just renders it.
 *
 * Each row is a Link to that user's profile. Clicking a row also closes
 * the modal (onClick={onClose}) so you don't return to a stale overlay.
 */
function FollowListModal({
  title,
  users,
  loading,
  onClose,
}: FollowListModalProps) {
  return (
    <div className="follow-modal-overlay" onClick={onClose}>
      {/* stopPropagation keeps clicks inside the box from closing the modal */}
      <div
        className="follow-modal-content"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="follow-modal-header">
          <h3>{title}</h3>
          <button className="btn-close" onClick={onClose}>
            ✖
          </button>
        </div>

        <div className="follow-modal-list">
          {loading ? (
            <p className="list-status">Loading...</p>
          ) : users.length > 0 ? (
            users.map((u) => (
              <Link
                key={u.username}
                to={`/users/${u.username}`}
                className="follow-list-item"
                onClick={onClose}
              >
                <img
                  src={u.profile_pic || "https://via.placeholder.com/45"}
                  alt={u.username}
                  className="item-avatar"
                />
                <div className="item-text">
                  <span className="item-username">{u.username}</span>
                  {u.first_name && (
                    <span className="item-name">{u.first_name}</span>
                  )}
                </div>
              </Link>
            ))
          ) : (
            <p className="list-status">No users to show.</p>
          )}
        </div>
      </div>
    </div>
  );
}

export default FollowListModal;
