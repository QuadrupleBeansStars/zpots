import { render, screen, act } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';

import { CountUp } from '@/components/primitives/CountUp';

describe('CountUp', () => {
  it('eventually renders the target value', async () => {
    vi.useFakeTimers();
    render(<CountUp value={128} />);
    await act(async () => {
      vi.advanceTimersByTime(500);
    });
    expect(screen.getByTestId('countup').textContent).toBe('128');
    vi.useRealTimers();
  });

  it('formats currency with the ฿ prefix', async () => {
    vi.useFakeTimers();
    render(<CountUp value={64500} format="currency" />);
    await act(async () => {
      vi.advanceTimersByTime(500);
    });
    expect(screen.getByTestId('countup').textContent).toContain('฿');
    expect(screen.getByTestId('countup').textContent).toContain('64');
    vi.useRealTimers();
  });
});
