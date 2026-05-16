'use client';
import React from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { Icon } from './Icon';
import { Button } from './Button';

const NAV = [
  { key: 'dashboard', icon: 'dashboard',       label: 'Dashboard',     href: '/owner' },
  { key: 'courts',    icon: 'stadium',         label: 'Venue Manager', href: '/owner/venues' },
  { key: 'slots',     icon: 'calendar_month',  label: 'Slot Control',  href: '/owner/slots' },
  { key: 'pricing',   icon: 'payments',        label: 'Pricing',       href: '/owner/pricing' },
  { key: 'bookings',  icon: 'list_alt',        label: 'Bookings',      href: '/owner/bookings' },
  { key: 'insights',  icon: 'smart_toy',       label: 'AI Insights',   href: '/owner/insights' },
  { key: 'opt',       icon: 'bolt',            label: 'Optimization',  href: '/owner/optimization' },
];

export function OwnerSidebar() {
  const pathname = usePathname();
  return (
    <aside
      style={{
        width: 248,
        minHeight: '100vh',
        background: '#0D1F0D',
        padding: '24px 16px',
        color: '#E8F5E9',
        display: 'flex',
        flexDirection: 'column',
      }}
    >
      <div style={{ display: 'flex', alignItems: 'center', gap: 8, padding: '0 8px 4px' }}>
        <img src="/bolt-glyph.svg" width={22} alt="ZPOTS" />
        <span className="display" style={{ color: '#fff', fontSize: 17, letterSpacing: '0.05em' }}>
          ZPOTS Admin
        </span>
      </div>
      <div
        style={{
          padding: '0 8px 14px',
          fontFamily: 'Lexend',
          fontSize: 9,
          letterSpacing: '0.12em',
          color: '#CFFC00',
          textTransform: 'uppercase',
          marginTop: 2,
        }}
      >
        Elite Venue Partner
      </div>
      <div style={{ height: 1, background: '#2A3E2A', margin: '4px 0 14px' }} />
      {NAV.map((it) => {
        const active = pathname === it.href || (it.href !== '/owner' && pathname.startsWith(it.href));
        return (
          <Link
            key={it.key}
            href={it.href}
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: 10,
              padding: '10px 12px',
              borderRadius: 999,
              marginBottom: 4,
              background: active ? 'linear-gradient(135deg,#cffc00,#b8e000)' : 'transparent',
              color: active ? '#1E4A00' : '#E8F5E9',
              fontWeight: active ? 700 : 500,
              fontSize: 13,
              textDecoration: 'none',
            }}
          >
            <Icon name={it.icon} style={{ fontSize: 18 }} />
            {it.label}
          </Link>
        );
      })}
      <div style={{ flex: 1 }} />
      <Link href="/owner/venues/new" style={{ textDecoration: 'none' }}>
        <Button variant="primary" icon="add_circle" style={{ justifyContent: 'center', padding: '10px 14px', width: '100%' }}>
          Add New Court
        </Button>
      </Link>
      <div style={{ height: 1, background: '#2A3E2A', margin: '14px 0 10px' }} />
      <Link href="/" style={{ display: 'flex', alignItems: 'center', gap: 10, padding: '10px 12px', color: '#A8C4A5', fontSize: 13, textDecoration: 'none' }}>
        <Icon name="logout" style={{ fontSize: 18 }} />Back to home
      </Link>
    </aside>
  );
}
