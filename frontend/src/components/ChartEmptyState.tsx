interface ChartEmptyStateProps {
  message?: string;
}

export function ChartEmptyState({ message = "No data for this range" }: ChartEmptyStateProps) {
  return <div className="flex h-full items-center justify-center text-sm text-ink-muted">{message}</div>;
}
