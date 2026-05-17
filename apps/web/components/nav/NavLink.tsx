'use client';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import React from 'react';

type Props = {
  href: string;
  exact?: boolean;
  children: React.ReactNode;
};

/**
 * Top-nav link. Active when pathname matches `href` (exact when `exact`,
 * prefix-match otherwise). Active state: lime underline 2px, 4px below.
 */
export function NavLink({ href, exact = false, children }: Props) {
  const pathname = usePathname();
  const active = exact ? pathname === href : pathname === href || pathname.startsWith(href + '/');
  return (
    <Link
      href={href}
      aria-current={active ? 'page' : undefined}
      className={[
        'relative px-3 py-2 text-body-sm font-geist transition-colors duration-quick ease-precision focus-ring rounded-kp-chip',
        active ? 'text-ink-900 font-semibold' : 'text-ink-700/70 hover:text-ink-900',
      ].join(' ')}
    >
      {children}
      {active && (
        <span
          aria-hidden
          className="absolute left-3 right-3 bg-lime"
          style={{ bottom: '-6px', height: '2px', borderRadius: '2px' }}
        />
      )}
    </Link>
  );
}
