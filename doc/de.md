Differential Expression (`DE`) Subcommand 
===================================================

The `DE` subcommand is planned to group differential-expression style analyses
under one interface with nested DE methods.

It currently documents one planned method:

- `tstat`: tissue specificity t-statistics.

### Common Synopsis

```bash
python CountTableTool.py DE <method> [options]
```

where `<method>` is:

- `tstat`

---

## `tstat` method

Computes tissue-specific t-statistics from a count table. This method is
intended to expose the same behavior as the legacy
`compute_tissue_tstat` workflow from `RegGenome_script_lib`.

### Synopsis

```bash
python CountTableTool.py DE tstat \
    --inpath PATH \
    [--tissue_labels LABEL1,LABEL2,...] \
    [--missing {raise,drop}] \
    [--opath PATH]
```

### Options

- **`--inpath`, `-I`** (required)  
  Path to the input count table file (CSV).  
  - Parsed as a pandas DataFrame with the first column used as the index.
  - Columns are treated as samples.

- **`--tissue_labels`** (optional, default: `None`)  
  Comma-separated tissue label for each sample column.  
  - Example: `--tissue_labels liver,liver,brain,brain`.  
  - If omitted, column names are used as tissue labels.
  - Number of labels should match the number of columns in `--inpath`.

- **`--missing`** (optional, default: `raise`)  
  Missing-value handling mode passed to OLS fitting.  
  - Allowed values: `raise`, `drop`.

- **`--opath`** (optional, default: `stdout`)  
  Path where the t-stat table is written.  
  - If `stdout`, the result is written to standard output as A CountTable.

### Behavior

- Reads the count table from `--inpath`.
- Determines tissue labels from `--tissue_labels`, or falls back to column names.
- For each unique tissue:
  - Builds a tissue indicator vector over samples (`1` for target tissue, `-1` otherwise).
  - Fits an OLS model for each row/element and computes the t-value of the tissue indicator.
- Writes an output table with:
  - rows = original elements (same index as input),
  - columns = unique tissue labels,
  - values = tissue-specific t-statistics.

---

## Transition note

The planned interface:

```bash
python CountTableTool.py DE tstat ...
```

is intended to replace the legacy command:

```bash
python count_table_tool.py compute_tissue_tstat ...
```
