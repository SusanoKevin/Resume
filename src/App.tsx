import { useState, useCallback } from 'react';
import { useResume } from './hooks/useResume';
import { useTheme } from './hooks/useTheme';
import Nav from './components/Nav';
import Hero from './components/Hero';
import Experience from './components/Experience';
import Education from './components/Education';
import Certifications from './components/Certifications';
import Skills from './components/Skills';
import Projects from './components/Projects';
import Contact from './components/Contact';

export default function App() {
  const { data, loading, error } = useResume();
  const { theme, toggleTheme } = useTheme();
  const [jumpedSections, setJumpedSections] = useState<Set<string>>(new Set());

  const handleSectionJump = useCallback((sectionId: string) => {
    setJumpedSections(prev => new Set([...prev, sectionId]));
  }, []);

  const instant = (id: string) => jumpedSections.has(id);

  if (loading) return (
    <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: '100vh', color: 'var(--text-secondary)' }}>
      Loading…
    </div>
  );

  if (error || !data) return (
    <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: '100vh', color: '#f87171' }}>
      Failed to load resume data.
    </div>
  );

  return (
    <>
      <Nav personal={data.personal} theme={theme} toggleTheme={toggleTheme} onSectionJump={handleSectionJump} />
      <main>
        <Hero personal={data.personal} />
        <Experience items={data.experience} instant={instant('experience')} />
        <Education items={data.education} instant={instant('education')} />
        <Certifications items={data.certifications} instant={instant('certifications')} />
        <Skills skills={data.skills} instant={instant('skills')} />
        <Projects items={data.projects} instant={instant('projects')} />
        <Contact personal={data.personal} instant={instant('contact')} />
      </main>
    </>
  );
}
