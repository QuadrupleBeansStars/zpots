'use client';
import React, { useEffect, useRef, useState } from 'react';

import { DUR, useReducedMotion } from '@/lib/motion';

type Format = 'number' | 'currency' | 'percent';

type Props = {
  value: number;
  format?: Format;
  duration?: number;        // override; defaults to DUR.smooth
  className?: string;
};

function formatValue(n: number, format: Format): string {
  if (format === 'currency') {
    return '฿' + Math.round(n).toLocaleString();
  }
  if (format === 'percent') {
    return Math.round(n) + '%';
  }
  return Math.round(n).toLocaleString();
}

const FRAME_MS = 16;

/**
 * Tween from 0 → `value` using ease-precision. Honors prefers-reduced-motion
 * (snaps instantly under reduced). Renders inside a tabular-nums span so
 * digits don't dance.
 */
export function CountUp({ value, format = 'number', duration, className = '' }: Props) {
  const reduced = useReducedMotion();
  const [display, setDisplay] = useState(reduced ? value : 0);
  const timerRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  useEffect(() => {
    if (reduced) {
      setDisplay(value);
      return;
    }
    const dur = duration ?? DUR.smooth;
    const startTime = Date.now();

    const tick = () => {
      const elapsed = Date.now() - startTime;
      const t = Math.min(1, elapsed / dur);
      // ease-precision approx: cubic-bezier(0.16, 1, 0.3, 1) ≈ 1 - (1 - t)^3
      const eased = 1 - Math.pow(1 - t, 3);
      if (t < 1) {
        setDisplay(value * eased);
        timerRef.current = setTimeout(tick, FRAME_MS);
      } else {
        setDisplay(value);
      }
    };

    timerRef.current = setTimeout(tick, 0);
    return () => {
      if (timerRef.current !== null) clearTimeout(timerRef.current);
    };
  }, [value, duration, reduced]);

  return (
    <span data-testid="countup" className={`font-geist-mono tabular-nums ${className}`}>
      {formatValue(display, format)}
    </span>
  );
}
