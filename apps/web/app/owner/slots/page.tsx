import { Button } from '@/components/Button';
import { KpiCard } from '@/components/KpiCard';
import { AITag } from '@/components/Tags';
import { SlotCalendar } from '@/components/owner/SlotCalendar';
import { SLOT_CALENDAR } from '@/lib/owner-mock-data';

export default function SlotsPage() {
  return (
    <div className="flex flex-col gap-6">
      <div className="flex justify-between items-end">
        <div>
          <h1 className="font-display text-3xl font-bold">Slot Control</h1>
          <p className="text-sm text-zpots-muted">Precision management of court inventory. AI is currently forecasting 97% occupancy for weekend prime slots.</p>
        </div>
        <div className="flex items-center gap-3">
          <span className="text-sm text-zpots-muted">May 12–18</span>
          <Button variant="primary" icon="add_circle">Add New Slot</Button>
        </div>
      </div>

      <div className="flex items-center gap-2">
        <AITag>LIVE AI OPTIMIZATION ON</AITag>
      </div>

      <SlotCalendar calendar={SLOT_CALENDAR} />

      <h2 className="font-semibold mt-4">🤖 AI Performance Prediction</h2>
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <KpiCard label="PREDICTED REVENUE" value="฿4,280" delta="↗ +10% vs LW" icon="💰" />
        <KpiCard label="PEAK HOURS"        value="18:00–20:00" delta="Fri, Sat, Sun" icon="🕐" />
        <KpiCard label="OCCUPANCY"         value="88.4%" icon="📊" />
        <KpiCard label="ACTIVE SLOTS"      value="24 Active" delta="View Rewards" icon="📅" />
      </div>
    </div>
  );
}
