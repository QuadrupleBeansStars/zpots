import React from 'react';

import { TopNav } from './nav/TopNav';

type Props = {
  role: 'player' | 'owner';
  children?: React.ReactNode;
};

/**
 * Shared page shell. Top nav at the top, page content in a centered main.
 * Layouts mount BookingsHydrator + ChatWidget around this; that stays in
 * the per-role layout file (not here) so PageShell stays role-agnostic.
 */
export function PageShell({ role, children }: Props) {
  return (
    <>
      <TopNav role={role} />
      <main className="max-w-[1400px] mx-auto px-5 md:px-8 py-8">
        {children}
      </main>
    </>
  );
}
