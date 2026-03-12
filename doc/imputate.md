Imputate Subcommand
===================

The `imputate` subcommand fills missing values in a count table using a simple imputation method.

### Synopsis

```bash
python CountTableTool.py imputate --inpath PATH [--opath PATH] [--method METHOD]
```

### Options

- **`--inpath`, `-I`** (required)  
  Path to the input count table file (CSV).  
  - Parsed as a pandas DataFrame with the first column used as the index.

- **`--opath`, `-O`** (optional, default: `stdout`)  
  Path where the imputed count table will be written.  
  - If `stdout`, the result is written to standard output as CSV.

- **`--method`** (optional, default: `min`)  
  Imputation method to use. Currently supported:
  - `min`: For each column, replaces missing values with the minimum value of that column.

### Behavior

For `method = min`, the tool:

- Reads the input count table from `--inpath`.
- For each column, computes the column-wise minimum value.
- Fills `NaN` entries in each column with that column’s minimum.
- Writes the resulting table to `--opath`.

