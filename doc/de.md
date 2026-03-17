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
    --exp_label LABEL1,LABEL2 \
    [--ctrl_label LABEL1,LABEL2,...] \
    [--tissue_labels LABEL1,LABEL2,...] \
    [--opath PATH]
```

### Options

- **`--inpath`, `-I`** (required)  
  Path to the input count table file (CSV).  
  - Parsed as a pandas DataFrame with the first column used as the index.
  - Columns are treated as samples.

- **`--exp_label`** 
  Label for the experiment group

- **`--ctrl_label`** (optional, default: `None`)
  Label for the control group
  - Can be multiple, comma seperated.
  - If omitted, use all other labels.

- **`--tissue_labels`** (optional, default: `None`)  
  Comma-separated tissue label for each sample column.  
  - Example: `--tissue_labels liver,liver,brain,brain`.  
  - If omitted, column names are used as tissue labels.
  - Number of labels should match the number of columns in `--inpath`.

- **`--opath`** (optional, default: `stdout`)  
  Path where the output table is written.  
  - If `stdout`, the result is written to standard output as A csv.

### Behavior

- Reads the count table from `--inpath`.
- Determines tissue labels from `--tissue_labels`, or falls back to column names.
- Perform DE
  - identify the experiment samples based on `--exp_label`
  - identify the ctrl samples based on `--ctrl_label`
  - Builds a tissue indicator vector over samples (`1` for exp samples , `-1` for ctrl samples).
  - Fits an OLS model for each row/element and computes the t-value of the tissue indicator.
- Writes an output table with:
  - rows = original elements (same index as input),
  - columns = [`log2FC`, `tstat`, `pval`, `padj`]

### tstat calculation

For each element (row) $g$, let $y_{gj}$ be the observed value in sample $j$,
for $j=1,\ldots,n$.

Define a group indicator $x_j$ from labels:

$$
x_j =
\begin{cases}
1, & \text{if sample } j \text{ is in } \texttt{--exp\_label} \\
-1, & \text{if sample } j \text{ is in control}
\end{cases}
$$

When `--ctrl_label` is omitted, control is all non-experiment samples.

The per-element model is ordinary least squares:

$$
y_{gj} = \beta_{0g} + \beta_{1g}x_j + \varepsilon_{gj}
$$

The reported `log2FC` is computed as:

$$
\log_2 \mathrm{FC}_g =
\log_2\left(\frac{\overline{y}_{g,\mathrm{exp}} + 1}{\overline{y}_{g,\mathrm{ctrl}} + 1}\right)
$$

where $\overline{y}_{g,\mathrm{exp}}$ and $\overline{y}_{g,\mathrm{ctrl}}$ are
the mean values in experiment and control samples, and `+1` is a pseudocount.

The reported `tstat` is the t-statistic for $\beta_{1g}$:

$$
t_g = \frac{\widehat{\beta}_{1g}}{\operatorname{SE}(\widehat{\beta}_{1g})}
$$

Interpretation:

- $t_g > 0$: element is higher in experiment vs control.
- $t_g < 0$: element is lower in experiment vs control.
- Larger $|t_g|$: stronger standardized separation between groups.

### Statistical Test

For each element $g$, the group-effect coefficient is tested with:

- Null hypothesis: $H_0: \beta_{1g}=0$ (no experiment-control difference).
- Alternative hypothesis: $H_A: \beta_{1g}\neq 0$ (two-sided difference).

Given the per-element t-statistic $t_g$, a two-sided p-value is:

$$
p_g = 2\left(1 - F_t\left(|t_g|;\ \nu_g\right)\right)
$$

where $F_t(\cdot;\nu_g)$ is the t-distribution CDF with residual degrees of
freedom $\nu_g$ from the fitted OLS model.

When many elements are tested, raw p-values should be adjusted for
multiple testing. The most common choice is Benjamini-Hochberg (BH) FDR:

$$
\mathrm{padj}_g = \mathrm{BH}(p_1,\ldots,p_m)_g
$$

with $m$ tested elements.

Interpretation guidelines:

- Small `pval` suggests evidence against $H_0$ for that element.
- Small `padj` controls expected false-discovery rate across all tested elements.
- In practice, combine significance with effect direction/magnitude (e.g. sign of `tstat` and optional fold-change threshold).
