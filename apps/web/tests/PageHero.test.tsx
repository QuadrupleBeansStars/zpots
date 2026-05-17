import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import { PageHero } from '@/components/primitives/PageHero';

describe('PageHero', () => {
  it('renders eyebrow + headline + sub', () => {
    render(
      <PageHero eyebrow="LIVE" headline="128 bookings" sub="great day" />
    );
    expect(screen.getByText('LIVE')).toBeInTheDocument();
    expect(screen.getByText('128 bookings')).toBeInTheDocument();
    expect(screen.getByText('great day')).toBeInTheDocument();
  });

  it('renders the optional CTA slot', () => {
    render(
      <PageHero
        eyebrow="x"
        headline="y"
        sub="z"
        cta={<button>Add Court</button>}
      />
    );
    expect(screen.getByText('Add Court')).toBeInTheDocument();
  });
});
