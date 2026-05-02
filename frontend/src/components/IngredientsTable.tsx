import { useMemo, useState } from 'react'
import {
  ColumnDef,
  ColumnFiltersState,
  flexRender,
  getCoreRowModel,
  getFilteredRowModel,
  getSortedRowModel,
  SortingState,
  useReactTable,
  ColumnPinningState,
} from '@tanstack/react-table'

type Ingredient = any

export function IngredientsTable({ data }: { data: Ingredient[] }) {
  const [sorting, setSorting] = useState<SortingState>([])
  const [filters, setFilters] = useState<ColumnFiltersState>([])
  const [pinning, setPinning] = useState<ColumnPinningState>({ left: ['name'], right: [] })

  const columns = useMemo<ColumnDef<Ingredient>[]>(() => [
    { accessorKey: 'name', header: 'Ingredient', enablePinning: true, cell: info => info.getValue() },
    { accessorKey: 'category', header: 'Category', enablePinning: true },
    { accessorKey: 'unit', header: 'Unit', enablePinning: true },
    { accessorKey: 'quantity', header: 'Qty', enablePinning: true },
    { accessorKey: 'calories', header: 'Calories', enablePinning: true },
    { accessorKey: 'protein_g', header: 'Protein', enablePinning: true },
    { accessorKey: 'carbs_g', header: 'Carbs', enablePinning: true },
    { accessorKey: 'fat_g', header: 'Fat', enablePinning: true },
    { accessorKey: 'fiber_g', header: 'Fiber', enablePinning: true },
    { accessorKey: 'sugar_g', header: 'Sugar', enablePinning: true },
    { accessorKey: 'sodium_mg', header: 'Sodium', enablePinning: true },
    { accessorKey: 'price', header: 'Price', enablePinning: true },
    { accessorKey: 'source', header: 'Source', enablePinning: true },
    { accessorKey: 'source_fdc_id', header: 'FDC ID', enablePinning: true },
    { accessorKey: 'manual_overrides', header: 'Manual', enablePinning: true, cell: info => String(info.getValue()) },
  ], [])

  const table = useReactTable({
    data,
    columns,
    state: { sorting, columnFilters: filters, columnPinning: pinning },
    onSortingChange: setSorting,
    onColumnFiltersChange: setFilters,
    onColumnPinningChange: setPinning,
    getCoreRowModel: getCoreRowModel(),
    getFilteredRowModel: getFilteredRowModel(),
    getSortedRowModel: getSortedRowModel(),
  })

  return (
    <div style={{overflowX:'auto', border:'1px solid #334155', borderRadius:16}}>
      <table style={{borderCollapse:'separate', borderSpacing:0, minWidth:1600, width:'100%'}}>
        <thead>
          {table.getHeaderGroups().map(hg => (
            <tr key={hg.id}>
              {hg.headers.map(header => {
                const pinned = header.column.getIsPinned()
                return (
                  <th
                    key={header.id}
                    style={{
                      position: pinned ? 'sticky' : 'static',
                      left: pinned === 'left' ? `${header.column.getStart('left')}px` : undefined,
                      right: pinned === 'right' ? `${header.column.getAfter('right')}px` : undefined,
                      zIndex: pinned ? 2 : 1,
                      background: 'var(--card)',
                      minWidth: 120,
                      borderBottom: '1px solid #334155',
                      padding: 10,
                      textAlign: 'left',
                      whiteSpace: 'nowrap'
                    }}
                  >
                    {header.isPlaceholder ? null : (
                      <div className="row" style={{gap:8}}>
                        <button onClick={header.column.getToggleSortingHandler() as any}>
                          {flexRender(header.column.columnDef.header, header.getContext())}
                        </button>
                        <button onClick={() => header.column.pin(pinned === 'left' ? false : 'left')}>📌</button>
                        <button onClick={() => header.column.setFilterValue('')}>✕</button>
                      </div>
                    )}
                    <input
                      style={{width:'100%', marginTop:6}}
                      value={(header.column.getFilterValue() ?? '') as string}
                      onChange={e => header.column.setFilterValue(e.target.value)}
                      placeholder="Filter"
                    />
                  </th>
                )
              })}
            </tr>
          ))}
        </thead>
        <tbody>
          {table.getRowModel().rows.map(row => (
            <tr key={row.id}>
              {row.getVisibleCells().map(cell => {
                const pinned = cell.column.getIsPinned()
                return (
                  <td
                    key={cell.id}
                    style={{
                      position: pinned ? 'sticky' : 'static',
                      left: pinned === 'left' ? `${cell.column.getStart('left')}px` : undefined,
                      right: pinned === 'right' ? `${cell.column.getAfter('right')}px` : undefined,
                      zIndex: pinned ? 1 : 0,
                      background: 'var(--bg)',
                      borderBottom: '1px solid #1f2937',
                      padding: 10,
                      whiteSpace: 'nowrap'
                    }}
                  >
                    {flexRender(cell.column.columnDef.cell, cell.getContext())}
                  </td>
                )
              })}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
