import { useState, useEffect } from 'react';
import type { ResumeData } from '../types';

interface UseResumeResult {
  data: ResumeData | null;
  loading: boolean;
  error: string | null;
}

export function useResume(): UseResumeResult {
  const [data, setData] = useState<ResumeData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const url = `${import.meta.env.BASE_URL}resume.json`;
    fetch(url)
      .then(res => {
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        return res.json() as Promise<ResumeData>;
      })
      .then(json => {
        setData(json);
        setLoading(false);
      })
      .catch(err => {
        setError(err instanceof Error ? err.message : 'Unknown error');
        setLoading(false);
      });
  }, []);

  return { data, loading, error };
}
