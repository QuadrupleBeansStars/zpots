import { Button } from '@/components/Button';
import { AITag, Eyebrow } from '@/components/Tags';
import { formatPrice } from '@/lib/format';

type Props = {
  headlineHtml: string;
  body: string;
  revenueLift: string;
  outcomes: { weeklyEarnings: number; delta: number; occupancyRate: number; occupancyDelta: number };
};

export function OpportunityCard({ headlineHtml, body, revenueLift, outcomes }: Props) {
  return (
    <div className="grid grid-cols-1 lg:grid-cols-[1.5fr_1fr] gap-5">
      <div className="zpots-card p-6">
        <AITag>LIVE OPPORTUNITY</AITag>
        <h2 className="font-display text-3xl font-bold mt-2" dangerouslySetInnerHTML={{ __html: headlineHtml }} />
        <div className="font-display text-5xl font-bold text-zpots-moss mt-3">{revenueLift}</div>
        <Eyebrow>REVENUE LIFT</Eyebrow>

        <div className="zpots-card-surface p-3 mt-4">
          <p className="text-sm">{body}</p>
        </div>
        <div className="flex gap-2 mt-4">
          <Button variant="primary" icon="check_circle">Adjust Slots Now</Button>
          <Button variant="secondary">Dismiss Insight</Button>
        </div>
      </div>

      <div className="zpots-card-lime p-5">
        <span className="font-eyebrow text-[10px] uppercase tracking-wider" style={{ color: '#1a2600' }}>
          PREDICTED OUTCOMES
        </span>
        <div className="mt-3">
          <div className="text-xs" style={{ color: '#1a2600' }}>WEEKLY EARNINGS</div>
          <div className="font-display text-3xl font-bold flex items-baseline gap-2" style={{ color: '#1a2600' }}>
            {formatPrice(outcomes.weeklyEarnings)}
            <span className="text-xs">+{formatPrice(outcomes.delta)}</span>
          </div>
        </div>
        <div className="mt-4">
          <div className="text-xs" style={{ color: '#1a2600' }}>OCCUPANCY RATE</div>
          <div className="font-display text-3xl font-bold flex items-baseline gap-2" style={{ color: '#1a2600' }}>
            {outcomes.occupancyRate}%
            <span className="text-xs">↑ {outcomes.occupancyDelta}%</span>
          </div>
        </div>
      </div>
    </div>
  );
}
