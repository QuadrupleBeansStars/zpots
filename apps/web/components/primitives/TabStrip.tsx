'use client';
import React from 'react';

type Tab = { key: string; label: React.ReactNode };

type Props = {
  active: string;
  tabs: Tab[];
  onChange: (key: string) => void;
  className?: string;
};

/**
 * Pill-tab strip — lime fill on active, neutral text on inactive.
 * Used by the dashboard's UTIL / REVENUE / NO-SHOW selector.
 */
export function TabStrip({ active, tabs, onChange, className = '' }: Props) {
  return (
    <div role="tablist" className={`flex flex-wrap gap-2 ${className}`}>
      {tabs.map((t) => {
        const isActive = t.key === active;
        return (
          <button
            key={t.key}
            type="button"
            role="tab"
            aria-selected={isActive}
            onClick={() => onChange(t.key)}
            className={[
              'px-4 py-2 rounded-kp-pill text-label-sm font-geist transition-colors duration-quick ease-precision focus-ring',
              isActive
                ? 'bg-lime text-ink-900 font-semibold'
                : 'bg-surface-low text-ink-700 hover:bg-surface-med',
            ].join(' ')}
          >
            {t.label}
          </button>
        );
      })}
    </div>
  );
}
