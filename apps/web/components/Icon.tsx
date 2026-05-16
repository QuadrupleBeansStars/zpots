import React from 'react';

type IconProps = { name: string; className?: string; style?: React.CSSProperties };

/**
 * Material Symbols Rounded icon. Requires the font loaded in layout (see globals.css).
 * Usage: <Icon name="calendar_month" />
 */
export function Icon({ name, className, style }: IconProps) {
  return (
    <span className={`material-symbols-rounded ${className ?? ''}`} style={style}>
      {name}
    </span>
  );
}
