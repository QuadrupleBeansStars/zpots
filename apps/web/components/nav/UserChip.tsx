'use client';
import React from 'react';

import { Icon } from '@/components/Icon';

type Props = {
  name: string;
  role: 'player' | 'owner';
};

/**
 * Avatar + name chip in the top-right of the nav. Phase 4 NextAuth will
 * make this open a dropdown; in 5a it's a static visual element.
 */
export function UserChip({ name, role }: Props) {
  const initial = name.charAt(0).toUpperCase();
  return (
    <div className="flex items-center gap-2 px-1">
      <div
        aria-label={`${name} (${role})`}
        className="w-8 h-8 rounded-kp-pill bg-ink-900 text-lime grid place-items-center text-body-sm font-geist font-semibold"
      >
        {initial}
      </div>
      <div className="hidden md:block">
        <div className="text-body-sm font-geist text-ink-900 leading-tight">{name}</div>
        <div className="text-label-sm text-ink-700/60 leading-tight">{role}</div>
      </div>
      <Icon name="expand_more" style={{ fontSize: 18, color: '#272e42' }} />
    </div>
  );
}
