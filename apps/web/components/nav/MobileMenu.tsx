'use client';
import Link from 'next/link';
import React from 'react';
import { Icon } from '@/components/Icon';

type Item = { href: string; label: string };

type Props = {
  open: boolean;
  onClose: () => void;
  items: Item[];
  cta?: { href: string; label: string };
};

export function MobileMenu({ open, onClose, items, cta }: Props) {
  if (!open) return null;
  return (
    <div className="fixed inset-0 z-50 bg-ink-900/95 backdrop-blur-2xl flex flex-col p-8">
      <div className="flex justify-end">
        <button
          type="button"
          onClick={onClose}
          aria-label="Close menu"
          className="p-2 focus-ring rounded-kp-chip text-white"
        >
          <Icon name="close" style={{ fontSize: 28 }} />
        </button>
      </div>
      <nav className="flex-1 flex flex-col justify-center gap-6">
        {items.map((it) => (
          <Link
            key={it.href}
            href={it.href}
            onClick={onClose}
            className="text-display-md font-geist font-bold text-white hover:text-lime transition-colors duration-quick ease-precision focus-ring"
          >
            {it.label}
          </Link>
        ))}
      </nav>
      {cta && (
        <Link
          href={cta.href}
          onClick={onClose}
          className="block w-full text-center px-5 py-4 bg-lime text-ink-900 font-geist font-semibold rounded-kp-pill focus-ring"
        >
          {cta.label}
        </Link>
      )}
    </div>
  );
}
