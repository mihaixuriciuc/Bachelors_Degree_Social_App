import { useState, useRef, useEffect } from "react";
import { Link } from "react-router-dom";
import { useUserSearch } from "../../hooks/useUserSearch";
import "./SearchBar.scss";

function SearchBar() {
  const { query, setQuery, results, loading, clear } = useUserSearch();
  const [isOpen, setIsOpen] = useState(false);
  const containerRef = useRef<HTMLDivElement>(null);

  // Close the dropdown when clicking anywhere outside the search box.
  // Same pattern as SettingsDropdown.
  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (
        containerRef.current &&
        !containerRef.current.contains(event.target as Node)
      ) {
        setIsOpen(false);
      }
    }
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  // When the user picks a result, clear the box and close the dropdown.
  const handleSelect = () => {
    clear();
    setIsOpen(false);
  };

  // Show the dropdown only when the box is focused/open AND there's a query.
  const showDropdown = isOpen && query.trim().length > 0;

  return (
    <div className="search-bar" ref={containerRef}>
      <input
        type="text"
        className="search-input"
        placeholder="Search users..."
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        onFocus={() => setIsOpen(true)}
      />

      {showDropdown && (
        <div className="search-dropdown">
          {loading ? (
            <p className="search-status">Searching...</p>
          ) : results.length > 0 ? (
            results.map((user) => (
              <Link
                key={user.username}
                to={`/users/${user.username}`}
                className="search-result-item"
                onClick={handleSelect}
              >
                <img
                  src={user.profile_pic || "https://via.placeholder.com/35"}
                  alt={user.username}
                  className="result-avatar"
                />
                <div className="result-text">
                  <span className="result-username">{user.username}</span>
                  {user.first_name && (
                    <span className="result-name">{user.first_name}</span>
                  )}
                </div>
              </Link>
            ))
          ) : (
            <p className="search-status">No users found.</p>
          )}
        </div>
      )}
    </div>
  );
}

export default SearchBar;
