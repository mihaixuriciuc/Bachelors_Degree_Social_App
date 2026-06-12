// The shape DRF's PageNumberPagination returns for a list endpoint.
// Generic <T> so it works for paginated posts, comments, anything.
export interface Paginated<T> {
  count: number; // total number of items across all pages
  next: string | null; // URL of the next page, or null if this is the last
  previous: string | null; // URL of the previous page, or null if first
  results: T[]; // the items on THIS page
}
