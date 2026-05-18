import { useState, useEffect } from 'react';

interface Props {
  text: string;
  /** When true: animate typing. When false: show full text instantly. */
  active: boolean;
  /** Milliseconds per character */
  speed?: number;
}

export default function TypedText({ text, active, speed = 28 }: Props) {
  const [chars, setChars] = useState(() => (active ? 0 : text.length));

  useEffect(() => {
    if (!active) {
      setChars(text.length);
      return;
    }
    setChars(0);
    let i = 0;
    const id = setInterval(() => {
      i++;
      setChars(i);
      if (i >= text.length) clearInterval(id);
    }, speed);
    return () => clearInterval(id);
  }, [active, text, speed]);

  const done = chars >= text.length;

  return (
    <>
      {text.slice(0, chars)}
      {active && !done && <span className="typed-cursor" aria-hidden="true" />}
    </>
  );
}
