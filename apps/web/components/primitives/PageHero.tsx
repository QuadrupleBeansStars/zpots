import React from 'react';
import { DarkHero } from './DarkHero';

type Props = {
  eyebrow: React.ReactNode;
  headline: React.ReactNode;
  sub?: React.ReactNode;
  cta?: React.ReactNode;
  className?: string;
};

/**
 * Page-level hero with KP-style structure: eyebrow date stamp, big headline,
 * optional sub-line, optional right-aligned CTA. Wraps DarkHero.
 */
export function PageHero({ eyebrow, headline, sub, cta, className = '' }: Props) {
  return (
    <DarkHero glow="lime" className={`px-6 md:px-8 py-8 md:py-10 ${className}`}>
      <div className="flex flex-col md:flex-row md:items-end md:justify-between gap-6">
        <div className="flex-1 min-w-0">
          <div className="text-label-sm text-lime/70 mb-2">{eyebrow}</div>
          <h1 className="font-geist font-bold text-display-md md:text-display-lg text-white leading-none tracking-tight">
            {headline}
          </h1>
          {sub && (
            <p className="mt-3 text-body-sm md:text-body-md text-white/60 max-w-2xl">
              {sub}
            </p>
          )}
        </div>
        {cta && <div className="flex-shrink-0">{cta}</div>}
      </div>
    </DarkHero>
  );
}
