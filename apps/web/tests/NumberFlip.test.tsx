import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';

import { NumberFlip } from '@/components/primitives/NumberFlip';

describe('NumberFlip', () => {
  it('renders one span per digit, in order', () => {
    render(<NumberFlip value={128} />);
    const digits = screen.getAllByTestId('flip-digit');
    expect(digits.map((d) => d.textContent)).toEqual(['1', '2', '8']);
  });

  it('renders an empty container for value 0', () => {
    render(<NumberFlip value={0} />);
    const digits = screen.getAllByTestId('flip-digit');
    expect(digits.map((d) => d.textContent)).toEqual(['0']);
  });
});
