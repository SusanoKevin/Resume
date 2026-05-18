import { useState, useEffect, useRef } from 'react';
import type { Experience as ExperienceType } from '../types';
import { fmtMonthYear } from '../utils/dates';
import { useScrollReveal } from '../hooks/useScrollReveal';
import TypedText from './TypedText';

interface Props {
  items: ExperienceType[];
  instant: boolean;
}

const TITLE = 'Experience';
const TITLE_DELAY = TITLE.length * 45 + 100;
const ITEM_STAGGER = 500;

export default function Experience({ items, instant }: Props) {
  const sectionRef = useRef<HTMLElement>(null);
  const isVisible = useScrollReveal(sectionRef, 0.1);
  const isTyping = isVisible && !instant;

  const [visibleCount, setVisibleCount] = useState(() => (instant ? items.length : 0));

  useEffect(() => {
    if (instant) { setVisibleCount(items.length); return; }
    if (!isVisible) return;

    const timers = items.map((_, i) =>
      setTimeout(() => setVisibleCount(v => Math.max(v, i + 1)), TITLE_DELAY + i * ITEM_STAGGER),
    );
    return () => timers.forEach(clearTimeout);
  }, [isVisible, instant, items]);

  return (
    <section id="experience" ref={sectionRef}>
      <div className="container">
        <div className="section-header">
          <h2 className="section-title">
            <TypedText text={TITLE} active={isTyping} speed={45} />
          </h2>
        </div>
        <div className="timeline">
          {items.map((job, idx) => {
            const visible = idx < visibleCount;
            const typing = isTyping && idx === visibleCount - 1;
            return (
              <div
                key={idx}
                className="timeline-item"
                style={{
                  opacity: visible ? 1 : 0,
                  transform: visible ? 'none' : 'translateY(16px)',
                  transition: 'opacity 0.35s ease, transform 0.35s ease',
                }}
              >
                <div className="timeline-dot" />
                <div className="timeline-position">
                  <TypedText text={job.position} active={typing} speed={24} />
                </div>
                <div className="timeline-meta">
                  <span className="timeline-company">{job.company}</span>
                  <span className="timeline-sep">·</span>
                  <span>{job.location}</span>
                  <span className="timeline-sep">·</span>
                  <span>{fmtMonthYear(job.start_date)} – {fmtMonthYear(job.end_date)}</span>
                  {job.current && <span className="timeline-badge">Current</span>}
                </div>
                <p className="timeline-description">{job.description}</p>
                {job.achievements.length > 0 && (
                  <ul className="timeline-achievements">
                    {job.achievements.map((a, i) => (
                      <li key={i} className="timeline-achievement">{a}</li>
                    ))}
                  </ul>
                )}
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
}
