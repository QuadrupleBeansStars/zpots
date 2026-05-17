import React from 'react';

import { NOISE_URL } from '@/lib/noise';

type Props = {
  glow?: 'none' | 'lime';
  className?: string;
  children?: React.ReactNode;
};

/**
 * Editorial dark hero card. Used by every page's title region in 5b+.
 * `glow="lime"` adds a radial lime gradient anchored top-right.
 */
export function DarkHero({ glow = 'lime', className = '', children }: Props) {
  return (
    <div
      className={`relative overflow-hidden bg-ink-900 text-white rounded-kp-card shadow-lift ${className}`}
      style={{
        backgroundImage: NOISE_URL,
        backgroundBlendMode: 'overlay',
        backgroundSize: '160px 160px',
        backgroundColor: '#15192a',
      }}
    >
      {glow === 'lime' && (
        <div
          aria-hidden
          className="absolute pointer-events-none"
          style={{
            top: '-20%',
            right: '-10%',
            width: '380px',
            height: '380px',
            background: 'radial-gradient(circle, rgba(207,252,0,0.35) 0%, rgba(207,252,0,0) 70%)',
          }}
        />
      )}
      <div className="relative">{children}</div>
    </div>
  );
}
