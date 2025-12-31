import type React from 'react';
import { useState } from 'react';

/**
 * HR Portal Home Page
 * Minimal 2x2 quadrant menu with outline-only iconography and calm focus states.
 */
function App() {
  const [logoLoaded, setLogoLoaded] = useState(true);

  const menuItems = [
    {
      title: 'Employees',
      description: 'People directory, profiles, and org visibility',
      icon: <UsersIcon />,
      position: 'tl' as const,
      href: '?page=employees',
      tooltip: 'View and manage employee records',
    },
    {
      title: 'Onboarding',
      description: 'Guided journeys for new joiners and managers',
      icon: <ClipboardIcon />,
      position: 'tr' as const,
      href: '?page=onboarding',
      tooltip: 'Track new hire onboarding progress',
    },
    {
      title: 'External Users',
      description: 'Secure access for recruiters and contractors',
      icon: <GlobeIcon />,
      position: 'bl' as const,
      href: '?page=external',
      tooltip: 'Manage external recruiters and contractors',
    },
    {
      title: 'Admin',
      description: 'Controls, approvals, and escalation visibility',
      icon: <ShieldIcon />,
      position: 'br' as const,
      href: '?page=admin',
      tooltip: 'Access administrative functions',
    },
  ];

  return (
    <div className="page-shell min-h-screen overflow-hidden bg-white">
      <main className="relative max-w-6xl mx-auto px-6 py-10 lg:py-14 page-transition">
        <header className="text-center mb-12 space-y-4">
          <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full border border-slate-200 text-sm text-slate-700">
            <span className="inline-flex h-2 w-2 rounded-full bg-emerald-500" />
            Systems live
          </div>

          <div className="space-y-2">
            {logoLoaded ? (
              <img
                src="/attached_assets/logo_1765648544636_1766742634201.png"
                alt="Baynunah"
                className="h-12 mx-auto"
                onError={() => setLogoLoaded(false)}
              />
            ) : (
              <h1 className="text-3xl font-semibold text-gray-900 tracking-wider">baynunah</h1>
            )}
            <div>
              <h2 className="text-2xl font-semibold text-gray-900 tracking-tight">HR portal</h2>
              <p className="text-gray-600 mt-2 max-w-2xl mx-auto leading-relaxed">
                Simple access to the four core areas. Clean outlines, steady focus states, and clear intent with zero visual noise.
              </p>
            </div>
          </div>
        </header>

        <section className="grid grid-cols-1 lg:grid-cols-[280px_1fr] gap-10 items-start">
          <div className="minimal-panel p-6 rounded-2xl space-y-4">
            <div className="space-y-1">
              <p className="text-sm font-semibold text-slate-700 uppercase tracking-[0.2em]">Orientation</p>
              <h3 className="text-xl font-semibold text-gray-900">Your daily HR console</h3>
            </div>
            <p className="text-gray-600 leading-relaxed">
              Everything is pared back to essentials: white space, light borders, and outline-only icons so you can see what matters fast.
            </p>
            <div className="flex flex-col gap-2 text-sm text-gray-700">
              <div className="hint-tile minimal-hint">Use <kbd>Tab</kbd> + <kbd>Enter</kbd> to move between quadrants.</div>
              <div className="hint-tile minimal-hint">Hover or focus to reveal the action line.</div>
              <div className="hint-tile minimal-hint">All links stay within the secure HR perimeter.</div>
            </div>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-6 justify-items-center">
            {menuItems.map((item) => (
              <MenuButton key={item.title} {...item} />
            ))}
          </div>
        </section>

        <footer className="mt-12 text-center text-sm text-gray-500 tracking-wider">
          Conceptualised by Baynunah | HR | IS
        </footer>
      </main>
    </div>
  );
}

interface MenuButtonProps {
  title: string;
  description: string;
  icon: React.ReactNode;
  position: 'tl' | 'tr' | 'bl' | 'br';
  href: string;
  tooltip?: string;
}

function MenuButton({ title, description, icon, position, href, tooltip }: MenuButtonProps) {
  const [isHovered, setIsHovered] = useState(false);

  const radiusStyles = {
    tl: '160px 8px 8px 8px',
    tr: '8px 160px 8px 8px',
    bl: '8px 8px 8px 160px',
    br: '8px 8px 160px 8px',
  }[position];

  const baseStyle: React.CSSProperties = {
    borderRadius: radiusStyles,
    textDecoration: 'none',
  };

  return (
    <a
      href={href}
      className="menu-card flex flex-col justify-between cursor-pointer focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-slate-500"
      style={baseStyle}
        onMouseEnter={() => setIsHovered(true)}
        onMouseLeave={() => setIsHovered(false)}
        title={tooltip}
        aria-label={`Navigate to ${title}`}
      >
        <div className="menu-card__top">
          <div className={`icon-ring ${isHovered ? 'icon-ring--active' : ''}`} aria-hidden>
            {icon}
          </div>
          <span className="menu-card__badge">{position.toUpperCase()} access</span>
        </div>
        <div className="space-y-1">
          <span className="menu-card__title">{title}</span>
          <p className="menu-card__description">{description}</p>
        </div>
        <div className="menu-card__cta">
          <span>{isHovered ? 'Go' : 'Open'}</span>
          <span className="menu-card__chevron" aria-hidden>
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
              <path d="M5 12h14" />
              <path d="M13 5l7 7-7 7" />
            </svg>
          </span>
        </div>
      </a>
    );
  }

function UsersIcon() {
  return (
    <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
      <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/>
      <circle cx="9" cy="7" r="4"/>
      <path d="M23 21v-2a4 4 0 0 0-3-3.87"/>
      <path d="M16 3.13a4 4 0 0 1 0 7.75"/>
    </svg>
  );
}

function ClipboardIcon() {
  return (
    <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
      <path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/>
      <rect x="8" y="2" width="8" height="4" rx="1" ry="1"/>
      <path d="M9 12h6"/>
      <path d="M9 16h6"/>
    </svg>
  );
}

function GlobeIcon() {
  return (
    <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
      <circle cx="12" cy="12" r="10"/>
      <line x1="2" y1="12" x2="22" y2="12"/>
      <path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/>
    </svg>
  );
}

function ShieldIcon() {
  return (
    <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
      <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
      <path d="M9 12l2 2 4-4"/>
    </svg>
  );
}

export default App;
