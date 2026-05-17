import { Button } from '@/components/Button';
import { AITag, Eyebrow } from '@/components/Tags';
import { formatPrice } from '@/lib/format';
import { DarkHero } from '@/components/primitives/DarkHero';
import { CountUp } from '@/components/primitives/CountUp';

type Props = {
  headlineHtml: string;
  body: string;
  revenueLift: string;
  outcomes: { weeklyEarnings: number; delta: number; occupancyRate: number; occupancyDelta: number };
};

export function OpportunityCard({ headlineHtml, body, revenueLift, outcomes }: Props) {
  return (
    <div className="grid grid-cols-1 lg:grid-cols-[1.5fr_1fr] gap-5">
      <DarkHero glow="lime" className="p-6">
        <AITag>LIVE OPPORTUNITY</AITag>
        <h2 className="font-geist font-bold text-display-sm text-white mt-2" dangerouslySetInnerHTML={{ __html: headlineHtml }} />
        <div className="font-geist-mono tabular-nums text-display-md font-bold text-lime mt-3">{revenueLift}</div>
        <Eyebrow>REVENUE LIFT</Eyebrow>

        <div className="bg-white/10 rounded-kp-card p-3 mt-4">
          <p className="text-body-sm text-white/80">{body}</p>
        </div>
        <div className="flex gap-2 mt-4">
          <Button variant="primary" icon="check_circle">Adjust Slots Now</Button>
          <Button variant="secondary">Dismiss Insight</Button>
        </div>
      </DarkHero>

      <div className="bg-white rounded-kp-card shadow-float p-5">
        <Eyebrow>PREDICTED OUTCOMES</Eyebrow>
        <div className="mt-3">
          <div className="text-label-sm text-ink-700/60 font-geist">WEEKLY EARNINGS</div>
          <div className="font-geist-mono tabular-nums text-display-sm font-bold text-ink-900 flex items-baseline gap-2 mt-1">
            <CountUp value={outcomes.weeklyEarnings} format="currency" />
            <span className="text-label-sm text-lime-deep">+{formatPrice(outcomes.delta)}</span>
          </div>
        </div>
        <div className="mt-4">
          <div className="text-label-sm text-ink-700/60 font-geist">OCCUPANCY RATE</div>
          <div className="font-geist-mono tabular-nums text-display-sm font-bold text-ink-900 flex items-baseline gap-2 mt-1">
            <CountUp value={outcomes.occupancyRate} format="percent" />
            <span className="text-label-sm text-lime-deep">↑ {outcomes.occupancyDelta}%</span>
          </div>
        </div>
      </div>
    </div>
  );
}
