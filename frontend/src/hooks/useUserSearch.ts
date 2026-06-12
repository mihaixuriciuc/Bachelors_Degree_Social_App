import { useEffect, useState } from "react";
import { UserListItem } from "../interfaces/userType";
import { userService } from "../services/userService";
import { useDebounce } from "./useDebounce";

/**
 * Owns all the state for the user search box:
 *  - query: what the user is currently typing
 *  - results: the matching users from the backend
 *  - loading: whether a request is in flight
 *
 * It debounces the query so the API is only hit after the user pauses typing.
 */
export const useUserSearch = () => {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<UserListItem[]>([]);
  const [loading, setLoading] = useState(false);

  // The debounced query updates 300ms after the user stops typing.
  const debouncedQuery = useDebounce(query, 300);

  useEffect(() => {
    const trimmed = debouncedQuery.trim();

    // Empty query → clear results, don't hit the API.
    if (!trimmed) {
      setResults([]);
      setLoading(false);
      return;
    }

    // cancelled guards against a race: if the user types again and a new
    // search starts before this one finishes, we ignore the stale response.
    let cancelled = false;
    setLoading(true);

    userService
      .search(trimmed)
      .then((res) => {
        if (!cancelled) setResults(res.data);
      })
      .catch((err) => {
        if (!cancelled) {
          console.error("Search failed", err);
          setResults([]);
        }
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });

    return () => {
      cancelled = true;
    };
  }, [debouncedQuery]);

  // clear() resets everything — used when the user picks a result or closes.
  const clear = () => {
    setQuery("");
    setResults([]);
  };

  return { query, setQuery, results, loading, clear };
};
