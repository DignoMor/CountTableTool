Normalization Subcommand
========================

The `normalization` subcommand normalizes a count table according to a specified normalization type.

It currently provides one normalization type:

- `per_million`: Normalize counts to counts-per-million (CPM).

### Common Synopsis

```bash
python CountTableTool.py normalization <normalization_type> [options]
```

where `<normalization_type>` is:

- `per_million`

---

## `per_million` normalization type

Performs counts-per-million normalization on each column.

### Synopsis

```bash
python CountTableTool.py normalization per_million \\
    --inpath PATH \\
    [--opath PATH]
```

### Options

- **`--inpath`, `-I`** (required)  
  Path to the input count table file (CSV).

- **`--opath`, `-O`** (optional, default: `stdout`)  
  Path where the normalized table is written.  
  - If `stdout`, the result is written to standard output as CSV.

### Behavior

- Reads the count table from `--inpath`.
- For each column, computes the column sum.
- Divides each value in the column by the column sum and multiplies by 1e6 to obtain counts-per-million.  
  Mathematically, for column \(j\):  
  \[
    \text{output}_{ij} = \frac{\text{input}_{ij}}{\sum_i \text{input}_{ij}} \times 10^6
  \]
- Writes the normalized table to `--opath`.

