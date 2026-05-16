'use client';
import React from 'react';
import { OwnerSidebar } from '@/components/OwnerSidebar';
import { KpiCard } from '@/components/KpiCard';
import { UtilizationBars } from '@/components/charts/UtilizationBars';
import { StatusBadge, Chip, AITag } from '@/components/Tags';
import { Button } from '@/components/Button';

const UTIL = { Mon: 65, Tue: 72, Wed: 58, Thu: 80, Fri: 91, Sat: 88, Sun: 45 };

export default function OwnerDashboardPage() {
  return (
    <div style={{ display: 'flex', background: '#F2F9EE', minHeight: '100vh' }}>
      <OwnerSidebar />
      <main style={{ flex: 1, padding: '26px 32px' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-end', marginBottom: 18 }}>
          <div>
            <h1 className="display" style={{ fontSize: 30 }}>Venue Performance</h1>
            <p style={{ color: '#3d4455', fontSize: 13, marginTop: 2 }}>Real-time metrics for your Bangkok facilities.</p>
          </div>
          <Button variant="primary" icon="add_circle">Add Court</Button>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4,1fr)', gap: 12, marginBottom: 18 }}>
          <KpiCard icon="📅" label="TOTAL BOOKINGS" value="128" delta="↗ +12%" />
          <KpiCard icon="💰" label="TOTAL REVENUE" value="฿64.5k" delta="October 2026" />
          <KpiCard icon="📊" label="AVG UTILIZATION" value="72%" delta="⊡ Stable" />
          <KpiCard icon="⭐" label="TOP RATED" value="Court 3" delta="4.8 · 142 reviews" />
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: '1.5fr 1fr', gap: 16 }}>
          <div className="zpots-card" style={{ padding: 20 }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <h3 className="display" style={{ fontSize: 16 }}>Utilization Trends</h3>
              <div style={{ display: 'flex', gap: 4 }}>
                <Chip selected>Weekly</Chip>
                <Chip>Daily</Chip>
                <Chip>Monthly</Chip>
              </div>
            </div>
            <UtilizationBars data={UTIL} />
          </div>
          <div className="zpots-card-lime" style={{ padding: 20 }}>
            <AITag>AI REVENUE OPTIMIZER</AITag>
            <p style={{ fontSize: 13, color: '#1a2600', marginTop: 8 }}>
              Demand for <b>Friday Evening</b> is up by <b>30%</b>. Raise prices for 18:00–21:00 slots to maximize revenue.
            </p>
            <Button variant="primary" style={{ marginTop: 14 }}>Apply Now</Button>
          </div>
        </div>
      </main>
    </div>
  );
}
