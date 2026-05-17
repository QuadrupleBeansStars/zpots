'use client';
import React, { useEffect, useRef, useState } from 'react';

type Props = {
  delay?: number;             // ms — staggers child reveal
  className?: string;
  children?: React.ReactNode;
};

/**
 * IntersectionObserver-driven fade-up. Fires once at 20% visibility.
 * Children start opacity-0 translate-y-2; reveal to opacity-100 translate-y-0
 * over dur-smooth with ease-precision.
 */
export function RevealOnScroll({ delay = 0, className = '', children }: Props) {
  const ref = useRef<HTMLDivElement>(null);
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    const el = ref.current;
    if (!el || typeof IntersectionObserver === 'undefined') {
      setVisible(true);
      return;
    }
    const io = new IntersectionObserver(
      (entries) => {
        for (const e of entries) {
          if (e.isIntersecting) {
            io.disconnect();
            // Use setTimeout only when a stagger delay is requested
            if (delay > 0) {
              setTimeout(() => setVisible(true), delay);
            } else {
              setVisible(true);
            }
            break;
          }
        }
      },
      { threshold: 0.2 },
    );
    io.observe(el);
    return () => io.disconnect();
  }, [delay]);

  return (
    <div
      ref={ref}
      data-testid="reveal-wrap"
      className={[
        'transition-all duration-smooth ease-precision',
        visible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-2',
        className,
      ].join(' ')}
    >
      {children}
    </div>
  );
}
