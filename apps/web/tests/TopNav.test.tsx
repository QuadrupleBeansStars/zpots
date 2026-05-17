import { render, screen } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';

vi.mock('next/navigation', () => ({
  usePathname: () => '/owner',
}));

import { TopNav } from '@/components/nav/TopNav';

describe('TopNav', () => {
  it('role="player" renders player nav items', () => {
    render(<TopNav role="player" />);
    expect(screen.getByText('Home')).toBeInTheDocument();
    expect(screen.getByText('Search')).toBeInTheDocument();
    expect(screen.getByText('My Bookings')).toBeInTheDocument();
    expect(screen.queryByText('Dashboard')).toBeNull();
  });

  it('role="owner" renders owner nav items', () => {
    render(<TopNav role="owner" />);
    expect(screen.getByText('Dashboard')).toBeInTheDocument();
    expect(screen.getByText('Courts')).toBeInTheDocument();
    expect(screen.getByText('Slots')).toBeInTheDocument();
    expect(screen.queryByText('Search')).toBeNull();
  });

  it('marks the matching link with aria-current="page"', () => {
    // mock returns '/owner', so Dashboard should be current
    render(<TopNav role="owner" />);
    expect(screen.getByText('Dashboard').closest('a')).toHaveAttribute('aria-current', 'page');
  });
});
