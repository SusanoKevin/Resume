import { useState, useEffect, useRef } from 'react';
import type { Project } from '../types';
import { fmtMonthYear } from '../utils/dates';
import { useScrollReveal } from '../hooks/useScrollReveal';
import TypedText from './TypedText';

interface Props { items: Project[]; instant: boolean; }

const TITLE = 'Projects';
const TITLE_DELAY = TITLE.length * 45 + 100;

export default function Projects({ items, instant }: Props) {
  const sectionRef = useRef<HTMLElement>(null);
  const isVisible = useScrollReveal(sectionRef, 0.1);
  const isTyping = isVisible && !instant;
  const [visibleCount, setVisibleCount] = useState(() => (instant ? items.length : 0));

  useEffect(() => {
    if (instant) { setVisibleCount(items.length); return; }
    if (!isVisible) return;
    const timers = items.map((_, i) =>
      setTimeout(() => setVisibleCount(v => Math.max(v, i + 1)), TITLE_DELAY + i * 450));
    return () => timers.forEach(clearTimeout);
  }, [isVisible, instant, items]);

  return (
    <section id="projects" ref={sectionRef}>
      <div className="container">
        <div className="section-header">
          <h2 className="section-title"><TypedText text={TITLE} active={isTyping} speed={45} /></h2>
        </div>
        <div className="projects-grid">
          {items.map((project, idx) => {
            const visible = idx < visibleCount;
            return (
              <div key={idx} className="card project-card"
                style={{ opacity: visible ? 1 : 0, transform: visible ? 'none' : 'translateY(16px)', transition: 'opacity 0.35s ease, transform 0.35s ease' }}>
                <div className="project-card-header">
                  <div className="project-name">
                    <TypedText text={project.name} active={isTyping && idx === visibleCount - 1} speed={26} />
                  </div>
                  {project.featured && <span className="featured-badge">Featured</span>}
                </div>
                <p className="project-description">{project.description}</p>
                {project.technologies.length > 0 && (
                  <div className="badge-list">
                    {project.technologies.map(tech => <span key={tech} className="badge">{tech}</span>)}
                  </div>
                )}
                <div className="project-footer">
                  {project.start_date && (
                    <span className="project-date">
                      {fmtMonthYear(project.start_date)}{project.end_date ? ` – ${fmtMonthYear(project.end_date)}` : ' – Present'}
                    </span>
                  )}
                  <div className="project-links">
                    {project.github_url && (
                      <a href={project.github_url} target="_blank" rel="noopener noreferrer" className="project-link">
                        <i className="fab fa-github" aria-hidden="true" /> GitHub
                      </a>
                    )}
                    {project.live_url && (
                      <a href={project.live_url} target="_blank" rel="noopener noreferrer" className="project-link">
                        <i className="fas fa-external-link-alt" aria-hidden="true" /> Live
                      </a>
                    )}
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
}
