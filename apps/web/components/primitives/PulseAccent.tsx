'use client';
import React from 'react';

type Props = {
  className?: string;
  children?: React.ReactNode;
};

/**
 * Continuous lime halo around child. Used for AI callouts.
 * Reduced-motion: collapses to a static 1px lime ring.
 */
export function PulseAccent({ className = '', children }: Props) {
  return (
    <>
      <style>{`
        @keyframes pulse-accent {
          0%, 100% { box-shadow: 0 0 0 0 rgba(207, 252, 0, 0.0); }
          50%      { box-shadow: 0 0 0 12px rgba(207, 252, 0, 0.0), 0 0 24px rgba(207, 252, 0, 0.55); }
        }
        .pulse-accent { animation: pulse-accent 2s ease-in-out infinite; }
        @media (prefers-reduced-motion: reduce) {
          .pulse-accent { animation: none; box-shadow: 0 0 0 1px rgba(207,252,0,0.6); }
        }
      `}</style>
      <span className={`pulse-accent inline-block rounded-kp-card ${className}`}>
        {children}
      </span>
    </>
  );
}
