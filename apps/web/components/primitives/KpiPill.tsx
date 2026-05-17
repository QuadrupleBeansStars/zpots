import React from 'react';

type Props = {
  label: string;
  value: React.ReactNode;
  className?: string;
};

/**
 * Compact KPI for the dark hero's right side or anywhere a small lime-on-ink
 * data chip is needed.
 */
export function KpiPill({ label, value, className = '' }: Props) {
  return (
    <div className={`inline-flex flex-col gap-0.5 px-3 py-2 bg-ink-800 rounded-kp-chip ${className}`}>
      <span className="text-label-sm text-white/50">{label}</span>
      <span className="font-geist-mono text-body-md text-lime tabular-nums">{value}</span>
    </div>
  );
}
