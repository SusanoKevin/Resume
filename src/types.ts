export interface Personal {
  name: string;
  title: string;
  email: string;
  location: string;
  summary: string;
  linkedin_url: string;
  github_url: string;
  website_url: string;
}

export interface Experience {
  position: string;
  company: string;
  location: string;
  start_date: string;
  end_date: string | null;
  current: boolean;
  description: string;
  achievements: string[];
}

export interface Education {
  institution: string;
  degree: string;
  field_of_study: string;
  start_date: string;
  end_date: string;
  gpa: string;
  description: string;
}

export interface Certification {
  name: string;
  issuer: string;
  date: string;
}

export interface Skill {
  name: string;
  category: string;
  proficiency: number;
}

export interface Project {
  name: string;
  description: string;
  technologies: string[];
  github_url: string;
  live_url: string;
  start_date: string | null;
  end_date: string | null;
  featured: boolean;
}

export interface ResumeData {
  personal: Personal;
  experience: Experience[];
  education: Education[];
  certifications: Certification[];
  skills: Skill[];
  projects: Project[];
}

export type SkillsByCategory = Record<string, Skill[]>;

export function groupByCategory(skills: Skill[]): SkillsByCategory {
  return skills.reduce<SkillsByCategory>((acc, skill) => {
    const cat = skill.category;
    return { ...acc, [cat]: [...(acc[cat] ?? []), skill] };
  }, {});
}
