import React, { type ElementType, type HTMLAttributes } from 'react';

type GlassPanelProps<T extends ElementType = 'div'> = {
  as?: T;
  className?: string;
  children?: React.ReactNode;
} & Omit<HTMLAttributes<HTMLElement>, 'className' | 'children'>;

/**
 * Glassmorphic surface — used by TopNav, floating menus, hover overlays.
 * Wraps `bg-white/60 backdrop-blur-2xl shadow-float`.
 */
export function GlassPanel<T extends ElementType = 'div'>({
  as,
  className = '',
  children,
  ...rest
}: GlassPanelProps<T>) {
  const Tag = (as || 'div') as ElementType;
  return (
    <Tag
      className={`bg-white/60 backdrop-blur-2xl shadow-float ${className}`}
      {...rest}
    >
      {children}
    </Tag>
  );
}
