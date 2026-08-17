import { CalendarIcon, MapPinIcon, XIcon } from "./icons";

interface TerritoryOption {
  id: number;
  name: string;
}

interface FilterBarProps {
  startDate: string | null;
  endDate: string | null;
  territoryId: number | null;
  territories: TerritoryOption[];
  onStartDateChange: (value: string | null) => void;
  onEndDateChange: (value: string | null) => void;
  onTerritoryChange: (value: number | null) => void;
}

const inputClass =
  "mt-1 rounded-lg border border-line bg-surface px-3 py-1.5 text-sm text-ink outline-none transition-colors focus:border-accent focus:ring-2 focus:ring-accent/20";

export function FilterBar({
  startDate,
  endDate,
  territoryId,
  territories,
  onStartDateChange,
  onEndDateChange,
  onTerritoryChange,
}: FilterBarProps) {
  const hasActiveFilters = startDate !== null || endDate !== null || territoryId !== null;

  const clearFilters = () => {
    onStartDateChange(null);
    onEndDateChange(null);
    onTerritoryChange(null);
  };

  return (
    <div className="rounded-xl border border-line bg-surface p-4 shadow-sm sm:p-5">
      <div className="flex flex-wrap items-end gap-4">
        <label className="flex min-w-36 flex-1 flex-col text-xs font-semibold uppercase tracking-wide text-ink-muted sm:flex-none">
          <span className="flex items-center gap-1.5">
            <CalendarIcon className="h-3.5 w-3.5" />
            From
          </span>
          <input
            type="date"
            value={startDate ?? ""}
            max={endDate ?? undefined}
            onChange={(event) => onStartDateChange(event.target.value || null)}
            className={inputClass}
          />
        </label>

        <label className="flex min-w-36 flex-1 flex-col text-xs font-semibold uppercase tracking-wide text-ink-muted sm:flex-none">
          <span className="flex items-center gap-1.5">
            <CalendarIcon className="h-3.5 w-3.5" />
            To
          </span>
          <input
            type="date"
            value={endDate ?? ""}
            min={startDate ?? undefined}
            onChange={(event) => onEndDateChange(event.target.value || null)}
            className={inputClass}
          />
        </label>

        <label className="flex min-w-40 flex-1 flex-col text-xs font-semibold uppercase tracking-wide text-ink-muted sm:flex-none">
          <span className="flex items-center gap-1.5">
            <MapPinIcon className="h-3.5 w-3.5" />
            Territory
          </span>
          <select
            value={territoryId ?? ""}
            onChange={(event) => onTerritoryChange(event.target.value ? Number(event.target.value) : null)}
            className={inputClass}
          >
            <option value="">All territories</option>
            {territories.map((territory) => (
              <option key={territory.id} value={territory.id}>
                {territory.name}
              </option>
            ))}
          </select>
        </label>

        {hasActiveFilters && (
          <button
            type="button"
            onClick={clearFilters}
            className="mb-0.5 flex items-center gap-1 rounded-full bg-accent-soft px-3 py-1.5 text-xs font-semibold text-accent transition-colors hover:bg-accent hover:text-white"
          >
            <XIcon className="h-3 w-3" />
            Clear filters
          </button>
        )}
      </div>
    </div>
  );
}
