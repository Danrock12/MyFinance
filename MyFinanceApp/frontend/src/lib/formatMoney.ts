export function formatMoney(val: number | null | undefined): string {
  if (val == null) return '';
  return `$${val.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
}