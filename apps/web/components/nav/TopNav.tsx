'use client';
import React, { useState } from 'react';
import Link from 'next/link';
import { MobileMenu } from './MobileMenu';

import { GlassPanel } from '@/components/primitives/GlassPanel';
import { Icon } from '@/components/Icon';
import { currentUser, currentOwner } from '@/lib/auth-stub';
import { NavLink } from './NavLink';
import { UserChip } from './UserChip';

type Role = 'player' | 'owner';

const PLAYER_NAV = [
  { href: '/player', label: 'Home', exact: true },
  { href: '/player/search', label: 'Search' },
  { href: '/player/bookings', label: 'My Bookings' },
];

const OWNER_NAV = [
  { href: '/owner', label: 'Dashboard', exact: true },
  { href: '/owner/venues', label: 'Courts' },
  { href: '/owner/slots', label: 'Slots' },
  { href: '/owner/pricing', label: 'Pricing' },
  { href: '/owner/bookings', label: 'Bookings' },
  { href: '/owner/insights', label: 'AI' },
];

type Props = { role: Role };

/**
 * Unified glass top nav. Replaces PlayerTopBar (kept around, unused) and
 * OwnerSidebar (kept around, unused) until 5c/5d delete them.
 */
export function TopNav({ role }: Props) {
  const nav = role === 'player' ? PLAYER_NAV : OWNER_NAV;
  const user = role === 'player' ? currentUser : currentOwner;
  const ctaHref = role === 'player' ? '/player/search' : '/owner/venues/new';
  const ctaLabel = role === 'player' ? 'Find courts' : '+ Add Court';
  const [mobileOpen, setMobileOpen] = useState(false);
  const mobileItems = nav.map((it) => ({ href: it.href, label: it.label }));

  return (
    <GlassPanel as="header" className="sticky top-0 z-40 h-16 px-5 md:px-8 flex items-center gap-6 border-b border-surface-med">
      <Link href={role === 'player' ? '/player' : '/owner'} className="flex items-center gap-2 focus-ring rounded-kp-chip">
        <img src="/bolt-glyph.svg" width={22} height={22} alt="" />
        <span className="font-geist font-semibold text-title-md text-ink-900 tracking-wide">
          ZPOTS
        </span>
        <span className="hidden md:inline text-label-sm text-ink-700/50 ml-1">
          {role === 'player' ? 'PLAYER' : 'BUSINESS'}
        </span>
      </Link>

      <nav className="hidden md:flex flex-1 items-center gap-1" aria-label={`${role} navigation`}>
        {nav.map((it) => (
          <NavLink key={it.href} href={it.href} exact={it.exact}>{it.label}</NavLink>
        ))}
      </nav>

      <div className="hidden md:block flex-1 md:flex-none" />

      <Link
        href={ctaHref}
        className="hidden md:inline-flex items-center gap-1 px-4 py-2 bg-lime text-ink-900 font-geist font-semibold text-body-sm rounded-kp-pill transition-transform duration-quick ease-precision hover:scale-[1.02] active:bg-lime-press focus-ring"
      >
        {ctaLabel}
      </Link>

      <UserChip name={user.name} role={role} />

      <button
        type="button"
        onClick={() => setMobileOpen(true)}
        className="md:hidden ml-auto p-2 focus-ring rounded-kp-chip"
        aria-label="Open menu"
      >
        <Icon name="menu" style={{ fontSize: 22, color: '#272e42' }} />
      </button>
      <MobileMenu
        open={mobileOpen}
        onClose={() => setMobileOpen(false)}
        items={mobileItems}
        cta={{ href: ctaHref, label: ctaLabel }}
      />
    </GlassPanel>
  );
}
