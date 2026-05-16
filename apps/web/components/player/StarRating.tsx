'use client';
import { useState } from 'react';

type Props = { value: number; onChange: (n: number) => void };

export function StarRating({ value, onChange }: Props) {
  const [hover, setHover] = useState(0);
  return (
    <div className="flex gap-1 text-3xl" onMouseLeave={() => setHover(0)}>
      {[1, 2, 3, 4, 5].map((n) => {
        const filled = (hover || value) >= n;
        return (
          <button
            key={n}
            type="button"
            onClick={() => onChange(n)}
            onMouseEnter={() => setHover(n)}
            className={filled ? 'text-zpots-lime drop-shadow' : 'text-zpots-mint'}
            aria-label={`${n} star${n > 1 ? 's' : ''}`}
          >
            ★
          </button>
        );
      })}
    </div>
  );
}
