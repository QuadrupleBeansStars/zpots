import { KpiCard } from '@/components/KpiCard';
import { AITag } from '@/components/Tags';
import { SlotCalendar } from '@/components/owner/SlotCalendar';
import { SLOT_CALENDAR } from '@/lib/owner-mock-data';
import { PageHero } from '@/components/primitives/PageHero';
import { RevealOnScroll } from '@/components/primitives/RevealOnScroll';

export default function SlotsPage() {
  return (
    <div className="flex flex-col gap-6">
      <PageHero
        eyebrow="SLOT CONTROL · MAY 12–18"
        headline="Precision schedule."
        sub="AI is forecasting 97% occupancy for weekend prime slots. Tune the inventory below."
        cta={
          <button className="inline-flex items-center gap-2 px-5 py-2.5 rounded-kp-pill bg-lime text-ink-900 font-geist font-semibold text-label-sm transition-colors duration-quick ease-precision hover:bg-lime/90 focus-ring">
            + Add New Slot
          </button>
        }
      />

      <RevealOnScroll>
        <div className="flex items-center gap-2">
          <AITag>LIVE AI OPTIMIZATION ON</AITag>
        </div>
      </RevealOnScroll>

      <RevealOnScroll delay={80}>
        <SlotCalendar calendar={SLOT_CALENDAR} />
      </RevealOnScroll>

      <RevealOnScroll delay={160}>
        <h2 className="font-geist font-semibold text-title-md text-ink-900">AI Performance Prediction</h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mt-3">
          <KpiCard label="PREDICTED REVENUE" value="฿4,280" delta="↗ +10% vs LW" icon="💰" />
          <KpiCard label="PEAK HOURS"        value="18:00–20:00" delta="Fri, Sat, Sun" icon="🕐" />
          <KpiCard label="OCCUPANCY"         value="88.4%" icon="📊" />
          <KpiCard label="ACTIVE SLOTS"      value="24 Active" delta="View Rewards" icon="📅" />
        </div>
      </RevealOnScroll>
    </div>
  );
}
