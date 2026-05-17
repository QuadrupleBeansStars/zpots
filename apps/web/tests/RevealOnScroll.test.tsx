import { render, screen, act } from '@testing-library/react';
import { describe, it, expect, beforeEach, vi } from 'vitest';

import { RevealOnScroll } from '@/components/primitives/RevealOnScroll';

// Capture the callback so we can fire it manually.
let observerCallback: IntersectionObserverCallback | null = null;

beforeEach(() => {
  observerCallback = null;
  class MockIO {
    callback: IntersectionObserverCallback;
    constructor(cb: IntersectionObserverCallback) {
      this.callback = cb;
      observerCallback = cb;
    }
    observe = vi.fn();
    unobserve = vi.fn();
    disconnect = vi.fn();
    takeRecords = vi.fn(() => []);
    root = null;
    rootMargin = '';
    thresholds = [];
  }
  // @ts-expect-error — test-time global
  global.IntersectionObserver = MockIO;
});

describe('RevealOnScroll', () => {
  it('children start hidden, become visible after intersection', () => {
    render(
      <RevealOnScroll>
        <p data-testid="content">hi</p>
      </RevealOnScroll>,
    );

    const wrap = screen.getByTestId('reveal-wrap');
    expect(wrap.className).toContain('opacity-0');

    // Fire the intersection callback.
    act(() => {
      observerCallback?.(
        [{ isIntersecting: true, intersectionRatio: 0.5 } as IntersectionObserverEntry],
        {} as IntersectionObserver,
      );
    });

    // Re-query after state update.
    expect(screen.getByTestId('reveal-wrap').className).not.toContain('opacity-0');
  });

  it('renders children regardless of visibility', () => {
    render(
      <RevealOnScroll>
        <p data-testid="content">visible-text</p>
      </RevealOnScroll>,
    );
    expect(screen.getByTestId('content').textContent).toBe('visible-text');
  });
});
