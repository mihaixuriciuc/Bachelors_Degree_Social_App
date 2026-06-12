import { useEffect, useState, useCallback } from "react";
import { Post } from "../interfaces/postType";
import { postService } from "../services/postService";

/**
 * Owns the infinite-scroll feed state:
 *  - posts: the accumulated list across all loaded pages
 *  - loading: whether a page request is currently in flight
 *  - hasMore: whether there are more pages to load (from the API's `next` field)
 *
 * loadMore() fetches the next page and APPENDS it to the existing list.
 * The first page loads automatically on mount.
 */
export const useInfiniteFeed = () => {
  const [posts, setPosts] = useState<Post[]>([]);
  const [page, setPage] = useState(1);
  const [hasMore, setHasMore] = useState(true);
  const [loading, setLoading] = useState(false);

  const loadMore = useCallback(async () => {
    if (loading || !hasMore) return;

    setLoading(true);
    try {
      const res = await postService.listFeed(page);

      setPosts((prev) => {
        // Build a set of IDs we already have, so we never add a duplicate.
        const existingIds = new Set(prev.map((p) => p.id));
        const newPosts = res.data.results.filter((p) => !existingIds.has(p.id));
        return [...prev, ...newPosts];
      });

      setHasMore(res.data.next !== null);
      setPage((prev) => prev + 1);
    } catch (err) {
      console.error("Failed to load feed page", err);
    } finally {
      setLoading(false);
    }
  }, [page, hasMore, loading]);

  // Load the first page once when the hook mounts.
  useEffect(() => {
    loadMore();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  // Used by the delete feature: remove a post from the list locally
  // without re-fetching everything.
  const removePost = (postId: number) => {
    setPosts((prev) => prev.filter((p) => p.id !== postId));
  };

  return { posts, loading, hasMore, loadMore, removePost };
};
