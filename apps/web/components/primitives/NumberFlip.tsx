'use client';
import React, { useEffect, useState } from 'react';

type Props = {
  value: number;
  className?: string;
};

/**
 * Odometer-style flip per digit. The sports-tech signature variant of CountUp.
 * Each digit is a span that animates on change.
 *
 * The CSS keyframe is inline so this component is self-contained and doesn't
 * need to be registered in globals.css.
 */
export function NumberFlip({ value, className = '' }: Props) {
  const [prev, setPrev] = useState(value);
  useEffect(() => {
    setPrev(value);
  }, [value]);

  const digits = String(Math.round(value)).split('');

  return (
    <>
      <style>{`
        @keyframes flip-digit {
          0% { transform: rotateX(0deg); opacity: 1; }
          50% { transform: rotateX(90deg); opacity: 0.5; }
          100% { transform: rotateX(0deg); opacity: 1; }
        }
        .flip-digit { display:inline-block; animation: flip-digit var(--dur-smooth, 360ms) var(--ease-precision, cubic-bezier(0.16,1,0.3,1)); }
        @media (prefers-reduced-motion: reduce) { .flip-digit { animation: none; } }
      `}</style>
      <span className={`font-geist-mono tabular-nums ${className}`}>
        {digits.map((d, i) => (
          <span
            key={`${prev}-${i}-${d}`}
            data-testid="flip-digit"
            className="flip-digit"
          >
            {d}
          </span>
        ))}
      </span>
    </>
  );
}
