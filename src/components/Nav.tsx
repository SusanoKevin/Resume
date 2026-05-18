import { useState, useEffect } from 'react';
import type { Personal } from '../types';

const SECTIONS = [
  { href: '#experience',     label: 'Experience' },
  { href: '#education',      label: 'Education' },
  { href: '#certifications', label: 'Certifications' },
  { href: '#skills',         label: 'Skills' },
  { href: '#projects',       label: 'Projects' },
  { href: '#contact',        label: 'Contact' },
];

interface Props {
  personal: Personal;
  theme: 'dark' | 'light';
  toggleTheme: () => void;
  onSectionJump: (sectionId: string) => void;
}

export default function Nav({ personal, theme, toggleTheme, onSectionJump }: Props) {
  const [active, setActive] = useState('');

  useEffect(() => {
    const els = SECTIONS.map(s => document.querySelector(s.href)).filter(Boolean) as Element[];
    const observer = new IntersectionObserver(
      entries => { entries.forEach(e => { if (e.isIntersecting) setActive('#' + e.target.id); }); },
      { rootMargin: '-40% 0px -40% 0px', threshold: 0 },
    );
    els.forEach(el => observer.observe(el));
    return () => observer.disconnect();
  }, []);

  const firstName = personal.name.split(' ').slice(0, 2).join(' ');

  return (
    <nav>
      <div className="container nav-inner">
        <a href="#hero" className="nav-brand">{firstName}</a>
        <div className="nav-links">
          {SECTIONS.map(({ href, label }) => (
            <a key={href} href={href} className={active === href ? 'active' : ''}
              onClick={() => onSectionJump(href.slice(1))}>
              {label}
            </a>
          ))}
        </div>
        <div className="nav-actions">
          <button className="theme-toggle" onClick={toggleTheme}
            aria-label={theme === 'dark' ? 'Switch to light mode' : 'Switch to dark mode'}>
            <i className={`fas fa-${theme === 'dark' ? 'sun' : 'moon'}`} />
          </button>
        </div>
      </div>
    </nav>
  );
}
