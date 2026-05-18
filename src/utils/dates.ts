const MONTHS = [
  'January', 'February', 'March', 'April', 'May', 'June',
  'July', 'August', 'September', 'October', 'November', 'December',
];

export function fmtMonthYear(dateStr: string | null | undefined): string {
  if (!dateStr) return 'Present';
  const [year, month] = dateStr.split('-');
  const idx = parseInt(month, 10) - 1;
  return `${MONTHS[idx] ?? ''} ${year}`.trim();
}

export function fmtYear(dateStr: string): string {
  return dateStr.split('-')[0];
}
