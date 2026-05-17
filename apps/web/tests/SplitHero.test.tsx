import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import { SplitHero } from '@/components/primitives/SplitHero';

describe('SplitHero', () => {
  it('renders eyebrow, headline, sub, and children', () => {
    render(
      <SplitHero eyebrow="LOGIN" headline="Welcome" sub="Click to enter">
        <p data-testid="form">form here</p>
      </SplitHero>
    );
    expect(screen.getByText('LOGIN')).toBeInTheDocument();
    expect(screen.getByText('Welcome')).toBeInTheDocument();
    expect(screen.getByText('Click to enter')).toBeInTheDocument();
    expect(screen.getByTestId('form')).toBeInTheDocument();
  });
});
