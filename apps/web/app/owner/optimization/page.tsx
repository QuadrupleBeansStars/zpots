import { OpportunityCard } from '@/components/owner/OpportunityCard';
import { Eyebrow } from '@/components/Tags';
import { formatPrice } from '@/lib/format';
import { PageHero } from '@/components/primitives/PageHero';
import { RevealOnScroll } from '@/components/primitives/RevealOnScroll';

export default function OptimizationPage() {
  return (
    <div className="flex flex-col gap-5">
      <PageHero
        eyebrow="AI OPS · PRIORITY INSIGHT"
        headline="Optimization engine."
        sub="Surfaced opportunities your venues should act on this week."
      />

      <RevealOnScroll delay={80}>
        <OpportunityCard
          headlineHtml='Open up <em>Friday 21:00</em> to capture <strong>+80% demand</strong>.'
          body='Data from the last 4 weeks shows a consistent search spike for Sunday 8:00 AM – 11:00 AM. Currently, your slots are locked for club training. Releasing 3 courts will likely fill within 12 hours.'
          revenueLift='+80%'
          outcomes={{ weeklyEarnings: 1420, delta: 204, occupancyRate: 92, occupancyDelta: 8 }}
        />
      </RevealOnScroll>

      <RevealOnScroll delay={160}>
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
          <div className="bg-white rounded-kp-card shadow-float p-4">
            <Eyebrow>MARKET BENCHMARK</Eyebrow>
            <h3 className="font-geist font-semibold text-title-sm text-ink-900 mt-1">Market Benchmark</h3>
            <p className="text-label-sm text-ink-700/60 mt-2">
              Similar venues in your area are pricing Sunday mornings at <strong className="text-ink-900">{formatPrice(45)}/hr</strong>.
            </p>
            <div className="font-geist-mono tabular-nums text-body-sm text-ink-900 mt-1">Your: <strong>{formatPrice(38)}/hr</strong></div>
          </div>
          <div className="bg-white rounded-kp-card shadow-float p-4">
            <Eyebrow>USER LOYALTY</Eyebrow>
            <h3 className="font-geist font-semibold text-title-sm text-ink-900 mt-1">User Loyalty</h3>
            <p className="text-label-sm text-ink-700/60 mt-2">
              Weekend users are <strong className="text-ink-900">3.5x</strong> more likely to book a recurring monthly slot.
            </p>
            <div className="text-body-sm text-ink-900 mt-1">High LTV potential</div>
          </div>
          <div className="bg-white rounded-kp-card shadow-float p-4">
            <Eyebrow>LEAD TIME</Eyebrow>
            <h3 className="font-geist font-semibold text-title-sm text-ink-900 mt-1">Lead Time</h3>
            <p className="text-label-sm text-ink-700/60 mt-2">
              Users are searching for Sunday slots as early as <strong className="text-ink-900">Wednesday evening</strong>.
            </p>
            <div className="text-label-sm text-lime-deep mt-1">Optimize now →</div>
          </div>
        </div>
      </RevealOnScroll>
    </div>
  );
}
