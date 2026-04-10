Import Subcommand
=================

The `import` subcommand converts external quantification outputs into a standardized count table.

It currently defines one import type:

- `rsem`: Build a count table from one or more RSEM result files.

### Common Synopsis

```bash
python CountTableTool.py import <import_type> [options]
```

where `<import_type>` is:

- `rsem`

---

## `rsem` import type

Creates a count table by collecting a selected count metric (for example `expected_count` or `TPM`) from multiple RSEM outputs and aligning rows to a provided gene ID list.

### Synopsis

```bash
python CountTableTool.py import rsem \
    --sample SAMPLE_NAME \
    --rsem_output PATH \
    --sample SAMPLE_NAME \
    --rsem_output PATH \
    --gene_id_list PATH \
    [--count_type COLUMN_NAME] \
    --opath PATH
```

### Options

- **`--sample`** (required, repeatable)  
  Sample name for one input RSEM file.  
  - Specify once per sample.

- **`--rsem_output`** (required, repeatable)  
  Path to an RSEM tab-delimited output file.  
  - Specify once per sample, in the same order as `--sample`.

- **`--gene_id_list`** (required)  
  Path to a plain-text file containing one gene ID per line.  
  - The output row order follows this file exactly.

- **`--count_type`** (optional, default: `expected_count`)  
  Name of the numeric column to extract from each RSEM file (for example `expected_count` or `TPM`).

- **`--opath`, `-O`** (required)  
  Output path for the generated count table (CSV).

### Input Expectations

- Each RSEM file is read as a tab-delimited table.
- The first column is treated as the row index (gene/transcript IDs).
- The selected `--count_type` column is expected to exist in every input RSEM file.
- The number of `--sample` and `--rsem_output` arguments should match one-to-one.

### Behavior

- Reads all RSEM input files.
- Reads the ordered gene ID list from `--gene_id_list`.
- For each sample, extracts values from the selected `--count_type` column by gene ID.
- Builds a count table with:
  - rows = gene IDs from `--gene_id_list`
  - columns = sample names from `--sample`
- Writes the resulting table to `--opath`.

### Example

```bash
python CountTableTool.py import rsem \
    --sample sample_A \
    --rsem_output data/sample_A.genes.results \
    --sample sample_B \
    --rsem_output data/sample_B.genes.results \
    --gene_id_list data/gene_ids.txt \
    --count_type expected_count \
    --opath output/count_table.csv
```
