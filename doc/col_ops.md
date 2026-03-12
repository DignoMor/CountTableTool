Column Operations (`col_ops`) Subcommand
========================================

The `col_ops` subcommand performs operations on the **columns** of one or more count tables.

It provides two operations:

- `concat`: Concatenate count tables column-wise.
- `filter`: Select a subset of columns from a count table.

### Common Synopsis

```bash
python CountTableTool.py col_ops <operation> [options]
```

where `<operation>` is one of:

- `concat`
- `filter`

---

## `concat` operation

Concatenates multiple count tables along the column axis.

### Synopsis

```bash
python CountTableTool.py col_ops concat --inpath PATH --inpath PATH [...] [--opath PATH]
```

### Options

- **`--inpath`, `-I`** (required, repeatable)  
  Input paths for the count tables to concatenate.  
  - You can specify this option multiple times; each occurrence adds one input file.  
  - All input tables must have the same row index; if not, a value error is raised after concatenation.

- **`--opath`** (optional, default: `stdout`)  
  Path where the concatenated table is written.  
  - If `stdout`, the result is written to standard output as CSV.

### Behavior

- Reads each input file as a count table with the first column used as the index.
- Concatenates all tables column-wise (`axis=1`).
- Checks that the number of rows in the result matches the first input table; otherwise raises `ValueError("Index mismatch.")`.

---

## `filter` operation

Selects a subset of columns from a single count table.

### Synopsis

```bash
python CountTableTool.py col_ops filter --inpath PATH --col NAME [--col NAME ...] [--opath PATH]
```

### Options

- **`--inpath`, `-I`** (required)  
  Input path for the count table to filter.

- **`--col`** (required, repeatable)  
  Name of a column to keep in the output.  
  - You can specify this option multiple times to keep multiple columns.  
  - If any requested column is not present, a `ValueError` is raised.

- **`--opath`** (optional, default: `stdout`)  
  Path where the filtered table is written.  
  - If `stdout`, the result is written to standard output as CSV.

### Behavior

- Reads the input table from `--inpath`.
- Validates that each `--col` specified exists in the table.
- Constructs a new table with only the requested columns, in the order specified.
- Writes the resulting table to `--opath`.

