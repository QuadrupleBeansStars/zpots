import React from 'react';

type Props = {
  icon?: string;           // emoji or Material Symbols name
  label: string;
  value: string | number;
  delta?: string;
};

/**
 * White card with mint border, used across owner dashboards.
 */
export function KpiCard({ icon, label, value, delta }: Props) {
  return (
    <div className="kpi-card">
      {icon && <span style={{ fontSize: 18, display: 'block', marginBottom: 4 }}>{icon}</span>}
      <div className="eyebrow">{label}</div>
      <div className="display" style={{ fontSize: 28 }}>{value}</div>
      {delta && <div style={{ fontSize: 12, color: '#2E6B00', marginTop: 2 }}>{delta}</div>}
    </div>
  );
}
