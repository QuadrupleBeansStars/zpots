'use client';
import React from 'react';

type Props = {
  className?: string;
  speed?: number;           // pixels per second; default 40
  children?: React.ReactNode;
};

/**
 * Horizontal marquee. Pauses on hover. Reduced-motion: stops.
 * Content is duplicated inline so the loop is seamless.
 */
export function Ticker({ className = '', speed = 40, children }: Props) {
  return (
    <div className={`overflow-hidden whitespace-nowrap relative ${className}`}>
      <style>{`
        @keyframes ticker-scroll {
          from { transform: translateX(0); }
          to   { transform: translateX(-50%); }
        }
        .ticker-track {
          display: inline-flex;
          animation: ticker-scroll linear infinite;
          animation-duration: var(--ticker-dur, 30s);
        }
        .ticker-track:hover { animation-play-state: paused; }
        @media (prefers-reduced-motion: reduce) {
          .ticker-track { animation: none; }
        }
      `}</style>
      <div
        className="ticker-track"
        style={{ ['--ticker-dur' as string]: `${Math.max(8, 2000 / speed)}s` }}
      >
        <span className="px-8">{children}</span>
        <span className="px-8" aria-hidden>{children}</span>
      </div>
    </div>
  );
}
