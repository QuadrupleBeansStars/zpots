'use client';
import React from 'react';

/**
 * Simple Tailwind/CSS bar chart for utilization.
 * In production, swap for Recharts <BarChart> for hover tooltips etc.
 */
export function UtilizationBars({ data }: { data: Record<string, number> }) {
  const max = Math.max(...Object.values(data));
  return (
    <div style={{ display: 'flex', alignItems: 'flex-end', gap: 12, height: 180, padding: '14px 8px 0' }}>
      {Object.entries(data).map(([day, val]) => (
        <div key={day} style={{ flex: 1, display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 6 }}>
          <div
            style={{
              width: '100%',
              height: (val / max) * 140,
              background: val >= 80 ? 'linear-gradient(to top,#2E6B00,#CFFC00)' : '#2E6B00',
              borderRadius: '8px 8px 0 0',
              position: 'relative',
            }}
          >
            <div
              style={{
                position: 'absolute',
                top: -18,
                left: '50%',
                transform: 'translateX(-50%)',
                fontSize: 11,
                color: '#3d5040',
                fontWeight: 600,
              }}
            >
              {val}%
            </div>
          </div>
          <div style={{ fontSize: 11, color: '#3d4455', fontFamily: 'Lexend' }}>{day}</div>
        </div>
      ))}
    </div>
  );
}
