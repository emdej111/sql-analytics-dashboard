const compactCurrency = new Intl.NumberFormat("en-US", {
  style: "currency",
  currency: "USD",
  notation: "compact",
  maximumFractionDigits: 1,
});

const fullCurrency = new Intl.NumberFormat("en-US", {
  style: "currency",
  currency: "USD",
  maximumFractionDigits: 2,
});

const compactNumber = new Intl.NumberFormat("en-US", { notation: "compact", maximumFractionDigits: 1 });

export function formatCompactCurrency(value: number): string {
  return compactCurrency.format(value);
}

export function formatCurrency(value: number): string {
  return fullCurrency.format(value);
}

export function formatCompactNumber(value: number): string {
  return compactNumber.format(value);
}

export function formatMonthLabel(isoDate: string): string {
  return new Date(isoDate).toLocaleDateString("en-US", { month: "short", year: "2-digit" });
}
