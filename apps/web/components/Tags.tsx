import React from 'react';
import { Icon } from './Icon';

/**
 * AI-accent tag. Small-caps label with a lime dot.
 * <AITag>AI-POWERED DISCOVERY</AITag>
 */
export function AITag({ children, onDark }: { children: React.ReactNode; onDark?: boolean }) {
  return <span className={`ai-tag${onDark ? ' on-dark' : ''}`}>{children}</span>;
}

type Status = 'confirmed' | 'active' | 'completed' | 'cancelled' | 'maintenance' | 'progress';
export function StatusBadge({ status, children }: { status: Status; children: React.ReactNode }) {
  return <span className={`status-badge status-${status}`}>{children}</span>;
}

export function Chip({ selected, onClick, children }: { selected?: boolean; onClick?: () => void; children: React.ReactNode }) {
  return (
    <span className={`chip ${selected ? 'chip-selected' : 'chip-default'}`} onClick={onClick}>
      {children}
    </span>
  );
}

export function Eyebrow({ children, className }: { children: React.ReactNode; className?: string }) {
  return <span className={`eyebrow ${className ?? ''}`}>{children}</span>;
}
