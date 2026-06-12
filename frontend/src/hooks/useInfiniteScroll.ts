import { useEffect, useRef } from "react";

/**
 * Calls `onIntersect` whenever the returned ref element scrolls into view.
 *
 * You place the returned ref on an invisible "sentinel" div at the bottom of
 * your list. When the user scrolls down far enough that the sentinel becomes
 * visible, IntersectionObserver fires and we call onIntersect (which loads
 * the next page).
 *
 * IntersectionObserver is a browser API that watches an element and tells you
 * when it enters or leaves the viewport. It's far more efficient than the old
 * approach of listening to every scroll event and measuring positions.
 *
 * `enabled` lets the caller switch the observer off — e.g. when there are no
 * more pages to load, we stop observing so it doesn't keep firing.
 */
export function useInfiniteScroll(onIntersect: () => void, enabled: boolean) {
  const sentinelRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    const node = sentinelRef.current;
    if (!node || !enabled) return;

    // The observer watches the sentinel. entries[0].isIntersecting is true
    // when the sentinel is visible in the viewport.
    const observer = new IntersectionObserver(
      (entries) => {
        if (entries[0].isIntersecting) {
          onIntersect();
        }
      },
      // rootMargin "200px" means: fire when the sentinel is within 200px of
      // entering the viewport, so the next page loads slightly BEFORE the
      // user hits the very bottom (feels smoother).
      { rootMargin: "200px" },
    );

    observer.observe(node);

    // Cleanup: stop observing when the component unmounts or deps change.
    return () => observer.disconnect();
  }, [onIntersect, enabled]);

  return sentinelRef;
}
