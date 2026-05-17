'use client';
import React from 'react';

/**
 * Simple Tailwind/CSS bar chart for utilization.
 * In production, swap for Recharts <BarChart> for hover tooltips etc.
 */
export function UtilizationBars({ data }: { data: Record<string, number> }) {
  const max = Math.max(...Object.values(data));
  return (
    <>
      <style>{`
        @keyframes bar-rise {
          from { transform: scaleY(0); }
          to   { transform: scaleY(1); }
        }
      `}</style>
      <div style={{ display: 'flex', alignItems: 'flex-end', gap: 12, height: 180, padding: '14px 8px 0' }}>
        {Object.entries(data).map(([day, val], i) => (
          <div key={day} style={{ flex: 1, display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 6 }}>
            <div
              style={{
                width: '100%',
                height: (val / max) * 140,
                background: 'linear-gradient(180deg, #cffc00 0%, #b8e600 100%)',
                borderRadius: '8px 8px 0 0',
                position: 'relative',
                transformOrigin: 'bottom',
                animation: `bar-rise 360ms cubic-bezier(0.34,1.56,0.64,1) both`,
                animationDelay: `${i * 40}ms`,
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
    </>
  );
}
