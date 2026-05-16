'use client';
import React from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { Icon } from './Icon';

const NAV = [
  { key: 'explore', label: 'Explore', icon: 'explore', href: '/' },
  { key: 'bookings', label: 'Bookings', icon: 'calendar_month', href: '/bookings' },
  { key: 'insights', label: 'Insights', icon: 'insights', href: '/insights' },
];

export function PlayerTopBar() {
  const pathname = usePathname();
  return (
    <div
      style={{
        display: 'flex',
        alignItems: 'center',
        gap: 24,
        padding: '14px 32px',
        background: '#fff',
        borderBottom: '1px solid #E3F0DE',
      }}
    >
      <Link href="/" style={{ display: 'flex', alignItems: 'center', gap: 8, textDecoration: 'none' }}>
        <img src="/bolt-glyph.svg" width={22} height={22} alt="ZPOTS" />
        <span className="display" style={{ fontSize: 20, letterSpacing: '0.05em', color: '#1C2526' }}>
          ZPOTS
        </span>
      </Link>
      <div style={{ flex: 1, display: 'flex', gap: 4, marginLeft: 24 }}>
        {NAV.map((it) => {
          const active = pathname === it.href || (it.href !== '/' && pathname.startsWith(it.href));
          return (
            <Link
              key={it.key}
              href={it.href}
              style={{
                padding: '8px 14px',
                borderRadius: 999,
                fontSize: 14,
                color: active ? '#1E4A00' : '#3d4455',
                fontWeight: active ? 600 : 500,
                background: active ? '#F2F9EE' : 'transparent',
                display: 'inline-flex',
                alignItems: 'center',
                gap: 6,
                textDecoration: 'none',
              }}
            >
              <Icon name={it.icon} style={{ fontSize: 18 }} />
              {it.label}
            </Link>
          );
        })}
      </div>
      <button style={{ width: 36, height: 36, borderRadius: 999, background: '#F2F9EE' }}>
        <Icon name="notifications" style={{ fontSize: 18, color: '#2E6B00' }} />
      </button>
      <button style={{ width: 36, height: 36, borderRadius: 999, background: '#CFFC00' }}>
        <Icon name="person" style={{ fontSize: 18, color: '#1E4A00' }} />
      </button>
    </div>
  );
}
