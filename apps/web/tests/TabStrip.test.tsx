import { render, screen, fireEvent } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import { TabStrip } from '@/components/primitives/TabStrip';

describe('TabStrip', () => {
  it('renders all tabs and marks active with aria-selected', () => {
    render(
      <TabStrip
        active="utilization"
        onChange={() => {}}
        tabs={[
          { key: 'utilization', label: 'UTILIZATION ↗' },
          { key: 'revenue', label: 'REVENUE' },
        ]}
      />
    );
    const active = screen.getByText('UTILIZATION ↗').closest('button');
    expect(active).toHaveAttribute('aria-selected', 'true');
  });

  it('calls onChange when a tab is clicked', () => {
    const onChange = vi.fn();
    render(
      <TabStrip
        active="a"
        onChange={onChange}
        tabs={[
          { key: 'a', label: 'A' },
          { key: 'b', label: 'B' },
        ]}
      />
    );
    fireEvent.click(screen.getByText('B'));
    expect(onChange).toHaveBeenCalledWith('b');
  });
});
