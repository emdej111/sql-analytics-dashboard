// First-load placeholder only — refetches keep the previous chart rendered
// at reduced opacity instead of swapping back to this (see ChartCard).
const BAR_HEIGHTS = [40, 65, 50, 80, 60, 90, 45];

export function ChartSkeleton() {
  return (
    <div className="flex h-full animate-pulse items-end gap-2 px-2" aria-hidden="true">
      {BAR_HEIGHTS.map((height, index) => (
        <div key={index} className="flex-1 rounded-t bg-line" style={{ height: `${height}%` }} />
      ))}
    </div>
  );
}
