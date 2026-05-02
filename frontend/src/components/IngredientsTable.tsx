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

  const columns = useMemo<ColumnDef<Ingredient>[]>(() => [
    { accessorKey: 'name', header: 'Ingredient Name', size: 200, enablePinning: true },
    { accessorKey: 'category', header: 'Category', size: 100 },
    { accessorKey: 'unit', header: 'Unit', size: 80 },
    { accessorKey: 'quantity', header: 'Qty', size: 80 },
    { accessorKey: 'calories', header: 'Calories', size: 100 },
    { accessorKey: 'protein_g', header: 'Protein (g)', size: 100 },
    { accessorKey: 'carbs_g', header: 'Carbs (g)', size: 100 },
    { accessorKey: 'fat_g', header: 'Fat (g)', size: 100 },
    { accessorKey: 'fiber_g', header: 'Fiber (g)', size: 100 },
    { accessorKey: 'sugar_g', header: 'Sugar (g)', size: 100 },
    { accessorKey: 'sodium_mg', header: 'Sodium (mg)', size: 100 },
    { accessorKey: 'price', header: 'Price ($)', size: 80 },
    { accessorKey: 'source', header: 'Source', size: 80 },
    { accessorKey: 'manual_overrides', header: 'Manual?', size: 80, cell: info => info.getValue() ? 'Yes' : 'No' },
  ], [])

  const table = useReactTable({
    data,
    columns,
    state: { sorting, columnFilters: filters },
    onSortingChange: setSorting,
    onColumnFiltersChange: setFilters,
    getCoreRowModel: getCoreRowModel(),
    getFilteredRowModel: getFilteredRowModel(),
    getSortedRowModel: getSortedRowModel(),
    columnResizeMode: 'onChange',
  })

  return (
    <div style={{overflowX:'auto', border:'1px solid #334155', borderRadius:16}}>
      <table style={{borderCollapse:'collapse', minWidth:1600, width:'100%'}}>
        <thead>
          {table.getHeaderGroups().map(headerGroup => (
            <tr key={headerGroup.id}>
              {headerGroup.headers.map(header => (
                <th
                  key={header.id}
                  style={{
                    borderBottom: '1px solid #334155',
                    background: 'var(--card)',
                    padding: '12px 8px',
                    textAlign: 'left',
                    fontWeight: 'bold',
                    fontSize: '14px',
                    whiteSpace: 'nowrap',
                    width: header.getSize(),
                    position: 'sticky',
                    top: 0,
                    zIndex: 10,
                  }}
                >
                  <div style={{display:'flex', gap:4, alignItems:'center'}}>
                    <button
                      onClick={header.column.getToggleSortingHandler()}
                      style={{padding: '2px 4px', fontSize:12, background:'none', border:'none', cursor:'pointer'}}
                    >
                      {header.isPlaceholder ? null : (
                        <>
                          {flexRender(header.column.columnDef.header, header.getContext())}
                          {header.column.getIsSorted() === 'asc' ? ' 🔼' : header.column.getIsSorted() === 'desc' ? ' 🔽' : ' ↕️'}
                        </>
                      )}
                    </button>
                  </div>
                  <input
                    style={{width:'100%', padding:'4px', marginTop:4, fontSize:12}}
                    value={(header.column.getFilterValue() ?? '') as string}
                    onChange={e => header.column.setFilterValue(e.target.value)}
                    placeholder={`Filter ${header.column.id}...`}
                  />
                </th>
              ))}
            </tr>
          ))}
        </thead>
        <tbody>
          {table.getRowModel().rows.map(row => (
            <tr key={row.id}>
              {row.getVisibleCells().map(cell => (
                <td
                  key={cell.id}
                  style={{
                    borderBottom: '1px solid #1f2937',
                    padding: '12px 8px',
                    whiteSpace: 'nowrap',
                    width: cell.column.getSize(),
                  }}
                >
                  {flexRender(cell.column.columnDef.cell, cell.getContext())}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
