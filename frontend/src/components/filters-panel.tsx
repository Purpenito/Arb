'use client'

import { ReactNode } from 'react'
import { ArbitrageType } from '@/types/signal'

export interface DashboardFilters {
  search: string
  longExchanges: string[]
  shortExchanges: string[]
  whitelistCoins: string
  blacklistCoins: string
  minVolume: number
  maxVolume: number
  minNet: number
  maxNet: number
  minFundingEdge: number
  arbitrageType: 'all' | ArbitrageType
  onlyProfitable: boolean
  onlyFunding: boolean
  refreshMs: number
}

interface Props {
  exchanges: string[]
  value: DashboardFilters
  onChange: (patch: Partial<DashboardFilters>) => void
}

function FilterField({ title, hint, children }: { title: string; hint: string; children: ReactNode }) {
  return (
    <div className="filter-field">
      <div className="filter-title">{title}</div>
      <div className="filter-hint">{hint}</div>
      {children}
    </div>
  )
}

export function FiltersPanel({ exchanges, value, onChange }: Props) {
  return (
    <section className="filters-top">
      <div className="hint-banner">
        <div>
          <div className="filter-title">Доступ к сканеру</div>
          <div className="filter-hint">Настрой фильтры и получай только релевантные арбитражные сигналы.</div>
        </div>
        <button className="primary-btn">Перейти к тарифам</button>
      </div>

      <div className="filter-grid">
        <FilterField title="Поиск тикера" hint="Быстрый поиск по монете/паре">
          <input placeholder="BTCUSDT" value={value.search} onChange={(e) => onChange({ search: e.target.value.toUpperCase() })} />
        </FilterField>
        <FilterField title="Тип арбитража" hint="Spot/Futures/Funding">
          <select value={value.arbitrageType} onChange={(e) => onChange({ arbitrageType: e.target.value as DashboardFilters['arbitrageType'] })}>
            <option value="all">Все типы</option>
            <option value="spot_futures">Spot → Futures</option>
            <option value="futures_futures">Futures → Futures</option>
            <option value="funding">Funding</option>
          </select>
        </FilterField>
        <FilterField title="Биржи для LONG / покупки" hint="Фильтр по входящей стороне">
          <select multiple value={value.longExchanges} onChange={(e) => onChange({ longExchanges: [...e.currentTarget.selectedOptions].map((o) => o.value) })}>
            {exchanges.map((exchange) => <option key={`l-${exchange}`}>{exchange}</option>)}
          </select>
        </FilterField>
        <FilterField title="Биржи для SHORT / продажи" hint="Фильтр по исходящей стороне">
          <select multiple value={value.shortExchanges} onChange={(e) => onChange({ shortExchanges: [...e.currentTarget.selectedOptions].map((o) => o.value) })}>
            {exchanges.map((exchange) => <option key={`s-${exchange}`}>{exchange}</option>)}
          </select>
        </FilterField>

        <FilterField title="Белый список монет" hint="Например: BTC, ETH, SOL">
          <input placeholder="BTC,ETH,SOL" value={value.whitelistCoins} onChange={(e) => onChange({ whitelistCoins: e.target.value.toUpperCase() })} />
        </FilterField>
        <FilterField title="Черный список монет" hint="Исключить монеты из выдачи">
          <input placeholder="DOGE,PEPE" value={value.blacklistCoins} onChange={(e) => onChange({ blacklistCoins: e.target.value.toUpperCase() })} />
        </FilterField>
        <FilterField title="Мин. сумма сделки, USDT" hint="Минимальный размер исполнения">
          <input type="number" value={value.minVolume} onChange={(e) => onChange({ minVolume: Number(e.target.value) })} />
        </FilterField>
        <FilterField title="Макс. сумма сделки, USDT" hint="Ограничение сверху по размеру">
          <input type="number" value={value.maxVolume} onChange={(e) => onChange({ maxVolume: Number(e.target.value) })} />
        </FilterField>

        <FilterField title="Мин. профит, %" hint="Нижний порог по net profit">
          <input type="number" value={value.minNet} step="0.01" onChange={(e) => onChange({ minNet: Number(e.target.value) })} />
        </FilterField>
        <FilterField title="Макс. профит, %" hint="Верхний порог по net profit">
          <input type="number" value={value.maxNet} step="0.01" onChange={(e) => onChange({ maxNet: Number(e.target.value) })} />
        </FilterField>
        <FilterField title="Мин. funding edge, %" hint="Минимальное funding преимущество">
          <input type="number" value={value.minFundingEdge} step="0.001" onChange={(e) => onChange({ minFundingEdge: Number(e.target.value) })} />
        </FilterField>
        <FilterField title="Частота обновления" hint="Интервал обновления таблицы">
          <select value={value.refreshMs} onChange={(e) => onChange({ refreshMs: Number(e.target.value) })}>
            <option value={1000}>1 секунда</option>
            <option value={2000}>2 секунды</option>
            <option value={5000}>5 секунд</option>
            <option value={10000}>10 секунд</option>
          </select>
        </FilterField>
      </div>

      <div className="toggle-row">
        <label><input type="checkbox" checked={value.onlyProfitable} onChange={(e) => onChange({ onlyProfitable: e.target.checked })} /> Только прибыльные сигналы</label>
        <label><input type="checkbox" checked={value.onlyFunding} onChange={(e) => onChange({ onlyFunding: e.target.checked })} /> Только funding opportunities</label>
        <button className="ghost">Расширенные настройки</button>
      </div>
    </section>
  )
}
