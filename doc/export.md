Export Subcommand
=================

The `export` subcommand transforms a count table into other formats.  
Currently, it supports exporting the top percentile of entries in `GenomicElements` format using `RGTools`.

It provides one export type:

- `top_percentile_ge`: Export top percentile entries as `GenomicElements`.

### Common Synopsis

```bash
python CountTableTool.py export <export_type> [options]
```

where `<export_type>` is:

- `top_percentile_ge`

---

## `top_percentile_ge` export type

Exports genomic regions corresponding to the top percentile of values in a specified column, in `GenomicElements` format.

### Synopsis

```bash
python CountTableTool.py export top_percentile_ge \\
    --inpath PATH \\
    --percentile PERCENT \\
    --filter_by COLUMN \\
    --region_file_path PATH \\
    --region_file_type TYPE \\
    [--opath PATH]
```

### Options

- **`--inpath`, `-I`** (required)  
  Path to the input count table file (CSV).

- **`--percentile`** (required, integer)  
  Top percentile (as an integer) of entries to export.  
  - For example, `--percentile 5` exports entries with values in the top 5% of the specified column.

- **`--filter_by`** (required)  
  Name of the column in the count table to use for percentile-based filtering.

- **`--region_file_path`** (required, via `GenomicElements.set_parser_genomic_element_region`)  
  Path to the region annotation file providing genomic regions corresponding to the rows of the count table.

- **`--region_file_type`** (required, via `GenomicElements.set_parser_genomic_element_region`)  
  Type/format of the region file (e.g. BED or another supported format defined by `RGTools.GenomicElements`).

- **`--opath`, `-O`** (optional, default: `stdout`)  
  Path where the filtered genomic elements will be written.  
  - If `stdout`, the result is written to standard output (format defined by `GenomicElements`).

### Behavior

- Reads the count table from `--inpath`.
- Extracts the values from the `--filter_by` column.
- Computes a percentile cutoff using NumPy on non-NaN values:  
  cutoff = `np.percentile(values, 100 - percentile)`.
- Builds a logical mask selecting all rows with values `>= cutoff`.
- Constructs a `GenomicElements` object from `--region_file_path` and `--region_file_type`.
- Applies the logical filter to the `GenomicElements` and writes the result to `--opath`.

