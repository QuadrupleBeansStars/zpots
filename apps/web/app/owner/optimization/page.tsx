import { OpportunityCard } from '@/components/owner/OpportunityCard';
import { Eyebrow } from '@/components/Tags';
import { formatPrice } from '@/lib/format';

export default function OptimizationPage() {
  return (
    <div className="flex flex-col gap-5">
      <div>
        <h1 className="font-display text-3xl font-bold">Optimization Engine</h1>
        <Eyebrow>AI OPS · PRIORITY INSIGHT</Eyebrow>
      </div>

      <OpportunityCard
        headlineHtml='Open up <em>Friday 21:00</em> to capture <strong>+80% demand</strong>.'
        body='Data from the last 4 weeks shows a consistent search spike for Sunday 8:00 AM – 11:00 AM. Currently, your slots are locked for club training. Releasing 3 courts will likely fill within 12 hours.'
        revenueLift='+80%'
        outcomes={{ weeklyEarnings: 1420, delta: 204, occupancyRate: 92, occupancyDelta: 8 }}
      />

      <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
        <div className="zpots-card p-4">
          <Eyebrow>MARKET BENCHMARK</Eyebrow>
          <p className="text-sm text-zpots-muted mt-2">
            Similar venues in your area are pricing Sunday mornings at <strong>{formatPrice(45)}/hr</strong>.
          </p>
          <div className="text-sm mt-1">Your: <strong>{formatPrice(38)}/hr</strong></div>
        </div>
        <div className="zpots-card p-4">
          <Eyebrow>USER LOYALTY</Eyebrow>
          <p className="text-sm text-zpots-muted mt-2">
            Weekend users are <strong>3.5x</strong> more likely to book a recurring monthly slot.
          </p>
          <div className="text-sm mt-1">High LTV potential</div>
        </div>
        <div className="zpots-card p-4">
          <Eyebrow>LEAD TIME</Eyebrow>
          <p className="text-sm text-zpots-muted mt-2">
            Users are searching for Sunday slots as early as <strong>Wednesday evening</strong>.
          </p>
          <div className="text-sm mt-1 text-zpots-moss">Optimize now →</div>
        </div>
      </div>
    </div>
  );
}
