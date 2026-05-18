import { useState, useEffect, useRef } from 'react';
import type { Education as EducationType } from '../types';
import { fmtYear } from '../utils/dates';
import { useScrollReveal } from '../hooks/useScrollReveal';
import TypedText from './TypedText';

interface Props {
  items: EducationType[];
  instant: boolean;
}

const TITLE = 'Education';
const TITLE_DELAY = TITLE.length * 45 + 100;
const ITEM_STAGGER = 400;

export default function Education({ items, instant }: Props) {
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
    <section id="education" className="bg-surface" ref={sectionRef}>
      <div className="container">
        <div className="section-header">
          <h2 className="section-title">
            <TypedText text={TITLE} active={isTyping} speed={45} />
          </h2>
        </div>
        <div className="edu-grid">
          {items.map((edu, idx) => {
            const visible = idx < visibleCount;
            const typing = isTyping && idx === visibleCount - 1;
            return (
              <div
                key={idx}
                className="card"
                style={{
                  opacity: visible ? 1 : 0,
                  transform: visible ? 'none' : 'translateY(16px)',
                  transition: 'opacity 0.35s ease, transform 0.35s ease',
                }}
              >
                <div className="edu-degree">
                  <TypedText text={edu.degree} active={typing} speed={26} />
                </div>
                <div className="edu-field">{edu.field_of_study}</div>
                <div className="edu-institution">{edu.institution}</div>
                <div className="edu-dates">{fmtYear(edu.start_date)} – {fmtYear(edu.end_date)}</div>
                {edu.gpa && (
                  <div className="edu-field" style={{ marginTop: '0.375rem' }}>GPA: {edu.gpa}</div>
                )}
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
}
