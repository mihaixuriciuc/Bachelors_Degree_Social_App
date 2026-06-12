import { useEffect, useState } from "react";

/**
 * Returns a "debounced" version of a value — one that only updates after
 * the value has stopped changing for `delay` milliseconds.
 *
 * Why this exists: a search box that fires an API request on every keystroke
 * sends way too many requests. Typing "alice" would fire 5 requests.
 * Debouncing waits until you STOP typing, then fires once.
 *
 * How it works: every time `value` changes, we start a timer. If `value`
 * changes again before the timer finishes, the cleanup function cancels the
 * old timer and starts a fresh one. The debounced value only updates when a
 * timer actually completes — i.e. when you've paused.
 *
 * Generic <T> so it works for any type (string, number, object).
 */
export function useDebounce<T>(value: T, delay: number = 300): T {
  const [debouncedValue, setDebouncedValue] = useState<T>(value);

  useEffect(() => {
    // Start a timer to update the debounced value after `delay` ms.
    const timer = setTimeout(() => {
      setDebouncedValue(value);
    }, delay);

    // Cleanup: if `value` changes before the timer fires, cancel it.
    // This is what resets the countdown on every keystroke.
    return () => clearTimeout(timer);
  }, [value, delay]);

  return debouncedValue;
}
