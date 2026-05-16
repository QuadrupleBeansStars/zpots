import { formatPrice } from '@/lib/format';

type Props = {
  total: number;
  delta: string;
  breakdown: { label: string; amount: number; highlight?: boolean }[];
};

export function RevenueBanner({ total, delta, breakdown }: Props) {
  return (
    <div className="rounded-card p-6 text-white" style={{ background: 'linear-gradient(135deg, #1a3a2a, #2E6B00)' }}>
      <div className="flex justify-between items-start">
        <div>
          <span className="font-eyebrow text-[10px] uppercase tracking-wider" style={{ color: 'rgba(255,255,255,0.7)' }}>
            TOTAL REVENUE TODAY
          </span>
          <div className="font-display text-5xl font-bold mt-1">{formatPrice(total)}</div>
          <div className="text-xs mt-1 opacity-80">📈 {delta}</div>
        </div>
      </div>
      <div className="flex gap-3 mt-5 flex-wrap">
        {breakdown.map((b) => (
          <div
            key={b.label}
            className="rounded-card px-4 py-2"
            style={{ background: b.highlight ? 'rgba(207,252,0,0.3)' : 'rgba(255,255,255,0.15)' }}
          >
            <div className="text-[10px] opacity-70">{b.label}</div>
            <div className="font-display font-bold">{formatPrice(b.amount)}</div>
          </div>
        ))}
      </div>
    </div>
  );
}
