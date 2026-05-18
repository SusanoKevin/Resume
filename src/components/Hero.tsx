import { useState, useEffect } from 'react';
import type { Personal } from '../types';

interface Props {
  personal: Personal;
}

export default function Hero({ personal }: Props) {
  const [title, setTitle] = useState('');
  const [done, setDone] = useState(false);

  useEffect(() => {
    const text = personal.title;
    let i = 0;
    const id = setInterval(() => {
      setTitle(text.slice(0, i + 1));
      i++;
      if (i >= text.length) {
        clearInterval(id);
        setDone(true);
      }
    }, 80);
    return () => clearInterval(id);
  }, [personal.title]);

  return (
    <section id="hero" className="hero-section">
      <div className="container">
        <div className="hero-content">
          <h1 className="hero-name">{personal.name}</h1>
          <p className="hero-title-wrap">
            <span>{title}</span>
            <span className={`hero-cursor${done ? ' done' : ''}`} aria-hidden="true" />
          </p>
          <p className="hero-summary">{personal.summary}</p>
          <div className="hero-meta">
            <span className="hero-meta-item">
              <i className="fas fa-map-marker-alt" aria-hidden="true" />
              {personal.location}
            </span>
            <a href={`mailto:${personal.email}`} className="hero-meta-item">
              <i className="fas fa-envelope" aria-hidden="true" />
              {personal.email}
            </a>
          </div>
          <div className="hero-social">
            {personal.linkedin_url && (
              <a
                href={personal.linkedin_url}
                target="_blank"
                rel="noopener noreferrer"
                className="hero-btn hero-btn-primary"
              >
                <i className="fab fa-linkedin" aria-hidden="true" /> LinkedIn
              </a>
            )}
            {personal.github_url && (
              <a
                href={personal.github_url}
                target="_blank"
                rel="noopener noreferrer"
                className="hero-btn hero-btn-outline"
              >
                <i className="fab fa-github" aria-hidden="true" /> GitHub
              </a>
            )}
            {personal.website_url && (
              <a
                href={personal.website_url}
                target="_blank"
                rel="noopener noreferrer"
                className="hero-btn hero-btn-outline"
              >
                <i className="fas fa-globe" aria-hidden="true" /> Website
              </a>
            )}
          </div>
        </div>
      </div>
    </section>
  );
}
