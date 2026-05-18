import { useState, useEffect, useRef } from 'react';
import type { Certification } from '../types';
import { fmtMonthYear } from '../utils/dates';
import { useScrollReveal } from '../hooks/useScrollReveal';
import TypedText from './TypedText';

interface Props { items: Certification[]; instant: boolean; }

const TITLE = 'Certifications';
const TITLE_DELAY = TITLE.length * 45 + 100;

export default function Certifications({ items, instant }: Props) {
  if (items.length === 0) return null;
  const sectionRef = useRef<HTMLElement>(null);
  const isVisible = useScrollReveal(sectionRef, 0.1);
  const isTyping = isVisible && !instant;
  const [visibleCount, setVisibleCount] = useState(() => (instant ? items.length : 0));

  useEffect(() => {
    if (instant) { setVisibleCount(items.length); return; }
    if (!isVisible) return;
    const timers = items.map((_, i) =>
      setTimeout(() => setVisibleCount(v => Math.max(v, i + 1)), TITLE_DELAY + i * 400));
    return () => timers.forEach(clearTimeout);
  }, [isVisible, instant, items]);

  return (
    <section id="certifications" ref={sectionRef}>
      <div className="container">
        <div className="section-header">
          <h2 className="section-title"><TypedText text={TITLE} active={isTyping} speed={45} /></h2>
        </div>
        <div className="cert-grid">
          {items.map((cert, idx) => {
            const visible = idx < visibleCount;
            return (
              <div key={idx} className="card"
                style={{ opacity: visible ? 1 : 0, transform: visible ? 'none' : 'translateY(16px)', transition: 'opacity 0.35s ease, transform 0.35s ease' }}>
                <div className="cert-icon"><i className="fas fa-award" aria-hidden="true" /></div>
                <div className="cert-name"><TypedText text={cert.name} active={isTyping && idx === visibleCount - 1} speed={26} /></div>
                <div className="cert-issuer">{cert.issuer}</div>
                <div className="cert-date">{fmtMonthYear(cert.date)}</div>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
}
