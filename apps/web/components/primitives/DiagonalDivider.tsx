import React from 'react';

type Props = {
  from?: string;            // CSS color above the diagonal
  to?: string;              // CSS color below the diagonal
  angle?: number;           // degrees — default 4
  className?: string;
};

/**
 * Diagonal transition between two surface colors. SVG-based so it scales
 * cleanly. Sits in normal flow at full width × 40px height.
 */
export function DiagonalDivider({
  from = '#f6f6ff',
  to = '#eef0ff',
  angle = 4,
  className = '',
}: Props) {
  // Compute the y offset on each side from the angle.
  const offset = Math.tan((angle * Math.PI) / 180) * 50;
  const polyTop = `0,0 100,0 100,${50 - offset} 0,${50 + offset}`;
  const polyBot = `0,${50 + offset} 100,${50 - offset} 100,100 0,100`;

  return (
    <svg
      viewBox="0 0 100 100"
      preserveAspectRatio="none"
      className={`block w-full h-10 ${className}`}
      aria-hidden
    >
      <polygon points={polyTop} fill={from} />
      <polygon points={polyBot} fill={to} />
    </svg>
  );
}
