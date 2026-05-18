import { useState, useRef, type FormEvent } from 'react';
import type { Personal } from '../types';
import { useScrollReveal } from '../hooks/useScrollReveal';
import TypedText from './TypedText';

interface Props { personal: Personal; instant: boolean; }
type FormStatus = 'idle' | 'success' | 'error';

export default function Contact({ personal, instant }: Props) {
  const [status, setStatus] = useState<FormStatus>('idle');
  const sectionRef = useRef<HTMLElement>(null);
  const isVisible = useScrollReveal(sectionRef, 0.1);
  const isTyping = isVisible && !instant;

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const form = e.currentTarget;
    try {
      const res = await fetch('https://formspree.io/f/YOUR_FORM_ID', {
        method: 'POST', body: new FormData(form), headers: { Accept: 'application/json' },
      });
      setStatus(res.ok ? 'success' : 'error');
      if (res.ok) form.reset();
    } catch { setStatus('error'); }
  };

  const formVisible = isVisible;

  return (
    <section id="contact" className="bg-surface" ref={sectionRef}>
      <div className="container">
        <div className="section-header">
          <h2 className="section-title"><TypedText text="Contact" active={isTyping} speed={45} /></h2>
          <p className="section-subtitle" style={{ opacity: formVisible ? 1 : 0, transition: 'opacity 0.4s ease 0.3s' }}>
            Reach me at <a href={`mailto:${personal.email}`}>{personal.email}</a>
          </p>
        </div>
        <form className="contact-form" onSubmit={handleSubmit}
          style={{ opacity: formVisible ? 1 : 0, transform: formVisible ? 'none' : 'translateY(16px)', transition: 'opacity 0.4s ease 0.4s, transform 0.4s ease 0.4s' }}>
          <div className="form-group">
            <label className="form-label" htmlFor="cf-name">Name</label>
            <input id="cf-name" name="name" className="form-input" type="text" required />
          </div>
          <div className="form-group">
            <label className="form-label" htmlFor="cf-email">Email</label>
            <input id="cf-email" name="email" className="form-input" type="email" required />
          </div>
          <div className="form-group">
            <label className="form-label" htmlFor="cf-message">Message</label>
            <textarea id="cf-message" name="message" className="form-textarea" required />
          </div>
          {status === 'success' && <p className="form-status form-status-success">Message sent!</p>}
          {status === 'error' && <p className="form-status form-status-error">Something went wrong. Please try again.</p>}
          <button type="submit" className="form-submit">Send Message</button>
        </form>
      </div>
    </section>
  );
}
