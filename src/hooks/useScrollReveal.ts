import { useState, useEffect, type RefObject } from 'react';

export function useScrollReveal(
  ref: RefObject<Element | null>,
  threshold = 0.25,
): boolean {
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    const el = ref.current;
    if (!el) return;

    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setIsVisible(true);
          observer.disconnect();
        }
      },
      { threshold },
    );

    observer.observe(el);
    return () => observer.disconnect();
  }, [ref, threshold]);

  return isVisible;
}
