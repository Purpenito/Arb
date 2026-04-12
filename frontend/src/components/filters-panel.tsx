'use client'

interface Props {
  search: string
  onSearch: (v: string) => void
  minNet: number
  onMinNet: (v: number) => void
  onlyFunding: boolean
  onOnlyFunding: (v: boolean) => void
}

export function FiltersPanel({ search, onSearch, minNet, onMinNet, onlyFunding, onOnlyFunding }: Props) {
  return (
    <aside className="panel">
      <h3>Filters</h3>
      <label>
        Ticker search
        <input value={search} onChange={(e) => onSearch(e.target.value.toUpperCase())} placeholder="BTC" />
      </label>
      <label>
        Min net profit %
        <input type="number" value={minNet} onChange={(e) => onMinNet(Number(e.target.value))} step="0.01" />
      </label>
      <label className="row">
        <input type="checkbox" checked={onlyFunding} onChange={(e) => onOnlyFunding(e.target.checked)} />
        Only opportunities with funding
      </label>
    </aside>
  )
}
