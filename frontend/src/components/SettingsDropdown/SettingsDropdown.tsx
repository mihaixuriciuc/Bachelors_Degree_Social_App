import { useState, useRef, useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";
import api from "../../api/api";
import "./SettingsDropdown.scss";

function SettingsDropdown() {
  const navigate = useNavigate();
  const [isOpen, setIsOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);

  // Close dropdown if the user clicks anywhere outside of it
  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (
        dropdownRef.current &&
        !dropdownRef.current.contains(event.target as Node)
      ) {
        setIsOpen(false);
      }
    }
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  const handleLogout = async () => {
    try {
      await api.post("/logout"); // Tells Django to delete the cookies
      navigate("/"); // Redirects to Home
    } catch (err) {
      console.error("Logout failed", err);
    }
  };

  return (
    <div className="settings-container" ref={dropdownRef}>
      <button className="btn-secondary" onClick={() => setIsOpen(!isOpen)}>
        Settings
      </button>

      {isOpen && (
        <div className="dropdown-menu">
          <Link to="/edit-profile" className="dropdown-item">
            Edit Profile
          </Link>
          <Link to="/security" className="dropdown-item">
            Security
          </Link>
          <button
            className="dropdown-item"
            onClick={() => alert("Appearance coming soon!")}
          >
            Appearance
          </button>

          <div className="dropdown-divider"></div>

          <button className="dropdown-item text-danger" onClick={handleLogout}>
            Log out
          </button>
        </div>
      )}
    </div>
  );
}

export default SettingsDropdown;
