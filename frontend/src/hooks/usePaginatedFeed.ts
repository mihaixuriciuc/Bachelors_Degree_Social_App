import { useEffect, useRef, useState, useCallback } from "react";
import { AxiosError } from "axios";
import { Post } from "../interfaces/postType";
import { postService } from "../services/postService";

/**
 * Owns the paginated feed state for the "Load More" button.
 *
 * Instead of keeping the page number in React state (which causes stale-
 * closure bugs where loadMore captures an old page value), we keep it in a
 * ref. A ref always holds the latest value and reading/writing it doesn't
 * depend on the render cycle — so loadMore always knows the real next page.
 *
 * `loadingRef` does the same job for the "is a request already running?"
 * guard, so two fast clicks can't both fire.
 */
export const usePaginatedFeed = () => {
  const [posts, setPosts] = useState<Post[]>([]);
  const [hasMore, setHasMore] = useState(true);
  const [loading, setLoading] = useState(false);

  // The next page to request. Starts at 1. Lives in a ref so it's always
  // current regardless of render timing.
  const nextPageRef = useRef(1);
  // Guards against overlapping requests without relying on the `loading`
  // state (which updates asynchronously).
  const loadingRef = useRef(false);
  // Ensures the initial auto-load only ever runs once, even under React
  // Strict Mode which intentionally double-invokes effects in development.
  const didInitialLoad = useRef(false);

  const loadMore = useCallback(async () => {
    // Hard guards using refs (synchronous, always current).
    if (loadingRef.current) return;

    loadingRef.current = true;
    setLoading(true);

    try {
      const pageToFetch = nextPageRef.current;
      const res = await postService.listFeed(pageToFetch);

      setPosts((prev) => {
        const existingIds = new Set(prev.map((p) => p.id));
        const newPosts = res.data.results.filter((p) => !existingIds.has(p.id));
        return [...prev, ...newPosts];
      });

      // Advance to the next page and update whether more remain.
      nextPageRef.current = pageToFetch + 1;
      setHasMore(res.data.next !== null);
    } catch (err) {
      // DRF returns 404 for a page past the last one — that means "no more".
      if (err instanceof AxiosError && err.response?.status === 404) {
        setHasMore(false);
      } else {
        console.error("Failed to load feed page", err);
      }
    } finally {
      loadingRef.current = false;
      setLoading(false);
    }
  }, []); // No deps — loadMore never goes stale because it reads from refs.

  // Load the first page once on mount.
  useEffect(() => {
    if (didInitialLoad.current) return;
    didInitialLoad.current = true;
    loadMore();
  }, [loadMore]);

  const removePost = (postId: number) => {
    setPosts((prev) => prev.filter((p) => p.id !== postId));
  };

  return { posts, loading, hasMore, loadMore, removePost };
};
