import { useEffect, useState, DependencyList } from "react";

interface FetchState<T> {
  data: T | null;
  loading: boolean;
  error: Error | null;
}

/**
 * Generic data-fetching hook.
 *
 * Before this existed, every page had the same shape:
 *
 *   const [data, setData] = useState(null);
 *   const [loading, setLoading] = useState(true);
 *   useEffect(() => {
 *     api.get("/some/url").then(...).catch(...).finally(...);
 *   }, []);
 *
 * That's 8 lines repeated in EditProfile, Security, Feed, Profile —
 * a textbook DRY violation. Now those pages do:
 *
 *   const { data, loading } = useFetch(() => profileService.getMine());
 *
 * The `cancelled` flag prevents the "can't set state on unmounted component"
 * warning when the user navigates away mid-fetch — a subtle bug your old
 * code had in every page.
 *
 * The generic <T> means TypeScript knows the type of `data` based on what
 * the fetcher returns. No `any` needed.
 */
export function useFetch<T>(
  fetcher: () => Promise<{ data: T }>,
  deps: DependencyList = [],
): FetchState<T> {
  const [state, setState] = useState<FetchState<T>>({
    data: null,
    loading: true,
    error: null,
  });

  useEffect(() => {
    let cancelled = false;
    setState((prev) => ({ ...prev, loading: true }));

    fetcher()
      .then((res) => {
        if (!cancelled) {
          setState({ data: res.data, loading: false, error: null });
        }
      })
      .catch((err) => {
        if (!cancelled) {
          setState({ data: null, loading: false, error: err });
        }
      });

    return () => {
      cancelled = true;
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, deps);

  return state;
}
