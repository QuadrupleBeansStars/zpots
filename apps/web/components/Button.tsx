import React from 'react';
import { Icon } from './Icon';

type Variant = 'primary' | 'secondary' | 'ghost' | 'dark-lime';
type Props = React.ButtonHTMLAttributes<HTMLButtonElement> & {
  variant?: Variant;
  icon?: string;
};

const variantClass: Record<Variant, string> = {
  primary: 'btn btn-primary',
  secondary: 'btn btn-secondary',
  ghost: 'btn btn-ghost',
  'dark-lime': 'btn btn-dark-lime',
};

export function Button({ variant = 'primary', icon, children, className, ...rest }: Props) {
  return (
    <button className={`${variantClass[variant]} ${className ?? ''}`} {...rest}>
      {icon && <Icon name={icon} style={{ fontSize: 18 }} />}
      {children}
    </button>
  );
}
