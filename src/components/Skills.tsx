import { useState, useMemo, useRef } from 'react';
import type { Skill } from '../types';
import { groupByCategory } from '../types';
import { useScrollReveal } from '../hooks/useScrollReveal';
import TypedText from './TypedText';

interface Props { skills: Skill[]; instant: boolean; }

function SkillBar({ skill, animate }: { skill: Skill; animate: boolean }) {
  return (
    <div className="skill-item">
      <div className="skill-header">
        <span className="skill-name">{skill.name}</span>
        <span className="skill-pct">{skill.proficiency}%</span>
      </div>
      <div className="skill-track">
        <div className="skill-bar-fill" style={{ width: animate ? `${skill.proficiency}%` : '0%' }} />
      </div>
    </div>
  );
}

export default function Skills({ skills, instant }: Props) {
  const [activeTab, setActiveTab] = useState('All');
  const sectionRef = useRef<HTMLDivElement>(null);
  const isVisible = useScrollReveal(sectionRef, 0.15);
  const isTyping = isVisible && !instant;

  const grouped = useMemo(() => groupByCategory(skills), [skills]);
  const categories = useMemo(() => ['All', ...Object.keys(grouped)], [grouped]);
  const visible = activeTab === 'All' ? skills : (grouped[activeTab] ?? []);

  return (
    <section id="skills" className="bg-surface">
      <div className="container">
        <div className="section-header">
          <h2 className="section-title"><TypedText text="Skills" active={isTyping} speed={45} /></h2>
        </div>
        <div className="skill-tabs">
          {categories.map(cat => (
            <button key={cat} className={`tab-btn${activeTab === cat ? ' active' : ''}`} onClick={() => setActiveTab(cat)}>
              {cat}
            </button>
          ))}
        </div>
        <div ref={sectionRef} className="skills-grid">
          {visible.map(skill => <SkillBar key={skill.name} skill={skill} animate={isVisible} />)}
        </div>
      </div>
    </section>
  );
}
