import React from 'react';
import { DarkHero } from './DarkHero';

type Props = {
  eyebrow: React.ReactNode;
  headline: React.ReactNode;
  sub?: React.ReactNode;
  children?: React.ReactNode;
  className?: string;
};

/**
 * Split full-page hero. Used by landing, login pages.
 * Left panel: dark hero (eyebrow + headline + sub). Right panel: children (form/cards).
 * Stacks vertically on mobile.
 */
export function SplitHero({ eyebrow, headline, sub, children, className = '' }: Props) {
  return (
    <div className={`grid grid-cols-1 md:grid-cols-[1.2fr_1fr] min-h-screen ${className}`}>
      <DarkHero glow="lime" className="p-8 md:p-13 flex items-center">
        <div>
          <div className="text-label-sm text-lime/70 mb-3">{eyebrow}</div>
          <h1 className="font-geist font-bold text-display-md md:text-display-lg text-white leading-none tracking-tight">
            {headline}
          </h1>
          {sub && (
            <p className="mt-4 text-body-md text-white/60 max-w-md">{sub}</p>
          )}
        </div>
      </DarkHero>
      <div className="bg-surface-low p-8 md:p-13 flex items-center">
        <div className="w-full max-w-md mx-auto">{children}</div>
      </div>
    </div>
  );
}
