import React from "react"
import { ExpandLess, ExpandMore, Visibility } from "@mui/icons-material"
import {
  IconButton,
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
  Typography,
} from "@mui/material"
import { Link } from "react-router-dom"
import theme from "theme"
import { enrichColumns } from "helpers/columns"
import useWorkspace from "helpers/useWorkspace"
import ColumnData from "./ColumnData"
import ColumnProperties from "./ColumnProperties"
import ColumnRequirements from "./ColumnRequirements"
import ColumnTests from "./ColumnTests"

interface GraiColumnMetadata {
  node_attributes: {
    data_type?: string | null
    is_nullable?: boolean | null
    is_primary_key?: boolean | null
    is_unique?: boolean | null
  }
}

export interface ColumnMetadata {
  grai: GraiColumnMetadata | null
}

interface RequirementEdge {
  metadata?: {
    grai?: {
      edge_attributes: {
        preserves_data_type?: boolean | null
        preserves_nullable?: boolean | null
        preserves_unique?: boolean | null
      }
    }
  } | null
  destination: {
    id: string
    name: string
    display_name: string
    metadata: ColumnMetadata
  }
}

export interface Column {
  id: string
  name: string
  display_name: string
  metadata: ColumnMetadata | null
  requirements_edges: { data: RequirementEdge[] }
}

type TableColumnsTableProps = {
  search: string | null
  columns: Column[]
  expanded: string[]
  onExpand: (id: string, expand: boolean) => void
}

const TableColumnsTable: React.FC<TableColumnsTableProps> = ({
  search,
  columns,
  expanded,
  onExpand,
}) => {
  const { routePrefix } = useWorkspace()

  const filteredColumns = search
    ? columns.filter(column =>
        column.name.toLowerCase().includes(search.toLowerCase()),
      )
    : columns

  const enrichedColumns = enrichColumns(filteredColumns)

  return (
    <Table sx={{ mt: 1 }} data-testid="columns-table">
      <TableHead>
        <TableRow>
          <TableCell sx={{ width: 0 }} />
          <TableCell>Name</TableCell>
          <TableCell>Data Type</TableCell>
          <TableCell>Properties</TableCell>
          <TableCell>Downstream Tests</TableCell>
          <TableCell>Data</TableCell>
          <TableCell sx={{ width: 0 }} />
          <TableCell sx={{ width: 0 }} />
        </TableRow>
      </TableHead>
      <TableBody>
        {enrichedColumns.map((column, index) => {
          const expand = expanded.includes(column.id)
          return (
            <React.Fragment key={column.id}>
              <TableRow
                hover
                sx={{ cursor: "pointer" }}
                onClick={() => onExpand(column.id, !expand)}
              >
                <TableCell sx={{ color: theme.palette.grey[500], pr: 0 }}>
                  {index}
                </TableCell>
                <TableCell sx={{ pl: 1 }}>{column.display_name}</TableCell>
                <TableCell>
                  {column.metadata?.grai?.node_attributes.data_type}
                </TableCell>
                <TableCell sx={{ py: 0 }}>
                  <ColumnProperties column={column} />
                </TableCell>
                <TableCell sx={{ py: 0 }}>
                  <ColumnTests column={column} />
                </TableCell>
                <TableCell>
                  <ColumnData />
                </TableCell>
                <TableCell sx={{ py: 0, px: 1 }}>
                  {column.requirements.length > 0 &&
                    (expand ? <ExpandLess /> : <ExpandMore />)}
                </TableCell>
                <TableCell sx={{ p: 0 }}>
                  <IconButton
                    component={Link}
                    to={`${routePrefix}/nodes/${column.id}`}
                  >
                    <Visibility />
                  </IconButton>
                </TableCell>
              </TableRow>
              {expand &&
                column.requirements.map(requirement => (
                  <TableRow
                    key={requirement.destination.name}
                    sx={{ backgroundColor: theme => theme.palette.grey[100] }}
                  >
                    <TableCell />
                    <TableCell>{requirement.destination.name}</TableCell>
                    <TableCell colSpan={2} />
                    <TableCell sx={{ py: 0 }}>
                      <ColumnRequirements edges={requirement.tests} />
                    </TableCell>
                    <TableCell />
                    <TableCell />
                    <TableCell />
                  </TableRow>
                ))}
            </React.Fragment>
          )
        })}
        {filteredColumns.length === 0 && (
          <TableRow>
            <TableCell colSpan={99} sx={{ textAlign: "center", py: 10 }}>
              <Typography>No columns found</Typography>
              {search && (
                <Typography sx={{ mt: 2 }}>Try clearing search</Typography>
              )}
            </TableCell>
          </TableRow>
        )}
      </TableBody>
    </Table>
  )
}

export default TableColumnsTable
