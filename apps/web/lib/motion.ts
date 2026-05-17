'use client';
import { useEffect, useState } from 'react';

/**
 * Duration constants in milliseconds. Mirror --dur-* CSS variables.
 * Use these in JS-driven animations (CountUp, NumberFlip).
 */
export const DUR = {
  instant: 120,
  quick:   220,
  smooth:  360,
  lush:    720,
} as const;

export const REDUCED_DUR = {
  instant: 1,
  quick:   1,
  smooth:  1,
  lush:    80,
} as const;

/**
 * React hook — returns true when the user has prefers-reduced-motion enabled.
 * SSR-safe: returns false on first render, updates after mount.
 */
export function useReducedMotion(): boolean {
  const [reduced, setReduced] = useState(false);
  useEffect(() => {
    const mq = window.matchMedia('(prefers-reduced-motion: reduce)');
    setReduced(mq.matches);
    const onChange = (e: MediaQueryListEvent) => setReduced(e.matches);
    mq.addEventListener('change', onChange);
    return () => mq.removeEventListener('change', onChange);
  }, []);
  return reduced;
}

/**
 * Pick the right duration based on reduced-motion preference.
 */
export function pickDur(key: keyof typeof DUR, reduced: boolean): number {
  return reduced ? REDUCED_DUR[key] : DUR[key];
}
