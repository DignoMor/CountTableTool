Export Subcommand
=================

The `export` subcommand transforms a count table into other formats.  
Currently, it supports exporting the top percentile of entries in `GenomicElements` format using `RGTools`.

It provides the following export types:

- `top_percentile_ge`: Export top percentile entries as `GenomicElements`.
- `name_replaced_ct`: Export a `CountTable` with replaced index name.

### Common Synopsis

```bash
python CountTableTool.py export <export_type> [options]
```

where `<export_type>` is:

- `top_percentile_ge`
- `name_replaced_ct`

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

---

## `name_replaced_ct` export type

Exports a `CountTable` after replacing the index column name in the output CSV.

### Synopsis

```bash
python CountTableTool.py export name_replaced_ct \
    --inpath PATH \
    --old_index_list <old_index_list_file> \
    --new_index_list <new_index_list_file> \
    [--opath PATH]
```

### Options

- **`--inpath`, `-I`** (required)  
  Path to the input count table file (CSV).

- **`--old_index_list`** (required)  
  Path to a list file containing old index names, one per line.

- **`--new_index_list`** (required)  
  Path to a list file containing new index names, one per line.  
  - Entries are matched by line order with `--old_index_list`.

- **`--opath`, `-O`** (optional, default: `stdout`)  
  Path where the renamed count table will be written.  
  - If `stdout`, the result is written to standard output as CSV.

### Behavior

- Reads the count table from `--inpath` with the first column as the row index.
- Reads old and new index name lists from `--old_index_list` and `--new_index_list`.
- Replaces index labels based on the old-to-new mapping.
- Preserves all row labels, column names, and numeric values.
- Writes the updated count table to `--opath`.

### Example

```bash
python CountTableTool.py export name_replaced_ct \
    --inpath output/count_table.csv \
    --old_index_list old_index_list.txt \
    --new_index_list new_index_list.txt \
    --opath output/count_table_with_gene_id_index.csv
```

