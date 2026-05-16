export function formatPrice(thb: number): string {
  return `฿${thb.toLocaleString('en-US')}`;
}

export function formatDateShort(iso: string): string {
  const d = new Date(`${iso}T00:00:00`);
  const weekday = d.toLocaleDateString('en-GB', { weekday: 'short' });
  const day = d.getDate();
  const month = d.toLocaleDateString('en-GB', { month: 'short' });
  return `${weekday}, ${day} ${month}`;
}

export function formatDateFull(iso: string): string {
  const d = new Date(`${iso}T00:00:00`);
  return d.toLocaleDateString('en-US', {
    weekday: 'long', year: 'numeric', month: 'long', day: 'numeric',
  });
}

export function formatTimeRange(startHHMM: string, endHHMM: string): string {
  return `${startHHMM} – ${endHHMM}`;
}
