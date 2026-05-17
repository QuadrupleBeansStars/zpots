import { render, screen, fireEvent } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';

vi.mock('next/navigation', () => ({
  usePathname: () => '/player',
}));

import { MobileMenu } from '@/components/nav/MobileMenu';

describe('MobileMenu', () => {
  it('renders nav links when open', () => {
    render(
      <MobileMenu
        open={true}
        onClose={() => {}}
        items={[{ href: '/a', label: 'A' }, { href: '/b', label: 'B' }]}
      />
    );
    expect(screen.getByText('A')).toBeInTheDocument();
    expect(screen.getByText('B')).toBeInTheDocument();
  });
  it('does not render when closed', () => {
    render(
      <MobileMenu
        open={false}
        onClose={() => {}}
        items={[{ href: '/a', label: 'A' }]}
      />
    );
    expect(screen.queryByText('A')).toBeNull();
  });
  it('calls onClose when close button clicked', () => {
    const onClose = vi.fn();
    render(
      <MobileMenu open={true} onClose={onClose} items={[]} />
    );
    fireEvent.click(screen.getByLabelText('Close menu'));
    expect(onClose).toHaveBeenCalled();
  });
});
