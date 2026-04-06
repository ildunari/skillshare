# Engineering & Scientific Research Applications

This file covers scientific and lab-oriented spreadsheet work: experimental data layout, controls, units, calibration curves, dose-response analysis, pharmacokinetic summaries, nanoparticle characterization, drug release kinetics, uncertainty, significant figures, regulatory awareness, and grant-budget structure.

See also: `data-science-statistics.md` for statistical procedure choices, `charts-and-visualization.md` for figure construction, and `review-readiness.md` for publication and review checks.

## Organize lab data for traceability

Lab and research sheets should be long-format and explicit where possible. Favor one observation per row with identifying fields.

**Example long-format layout:**

| Sample_ID | Subject_ID | Group | Treatment | Replicate | Time_h | Analyte | Result | Unit | Run_Date | Analyst | Instrument | Batch |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| NP-001-A | S01 | PLGA-50 | 10mg/kg | 1 | 0.5 | GLP-1RA | 24.7 | ng/mL | 2025-03-15 | KM | HPLC-UV | B2025-03 |
| NP-001-B | S01 | PLGA-50 | 10mg/kg | 2 | 0.5 | GLP-1RA | 26.1 | ng/mL | 2025-03-15 | KM | HPLC-UV | B2025-03 |

Wide-format blocks with unlabeled columns and hidden replicate structure make analysis fragile and review difficult. If the data arrives wide, reshape it to long-format in a staging sheet before analysis.

## Make controls, blanks, standards, and replicates explicit

Reserve separate fields or clear labels for negative controls, positive controls, blanks, standards or calibrators, technical replicates, biological replicates, and excluded wells or failed runs.

A reviewer should be able to reconstruct what happened without decoding color alone. Use a `Sample_Type` field (e.g., "Unknown," "Standard," "Blank," "QC-Low," "QC-High," "Positive Ctrl," "Negative Ctrl") to make this machine-readable.

## Unit handling and dimensional discipline

Put units in headers and keep them consistent down the column. A header reading `Concentration` is incomplete — `Concentration (ng/mL)` is specific.

When conversions occur, show the conversion factor or normalized result in a separate column rather than overwriting the original. Dimensional mistakes are among the most expensive spreadsheet errors — making the unit path visible is a form of error prevention.

**Example conversion layout:**

| Mass_mg | Volume_mL | Conc_mg_per_mL | Conc_µg_per_mL |
|---|---|---|---|
| 5.2 | 10.0 | =A2/B2 | =C2*1000 |

The conversion from mg/mL to µg/mL is visible and auditable. The factor (1000) lives in the formula because it's a true unit constant, not an assumption — but if the conversion is non-obvious, put the factor in a labeled cell.

## Calibration curves and standard curves

Use scatter plots, not line charts, for calibration data — the x-axis is quantitative, not categorical. Keep raw standard points visible as markers. Show the fitted relationship, the range, the equation, and R² when appropriate.

**Example calibration layout:**

| Std_Conc_ng_mL | Abs_450nm | Abs_450nm_Rep2 | Avg_Abs | Fit_Abs |
|---|---|---|---|---|
| 0 | 0.051 | 0.048 | =AVERAGE(B2,C2) | — |
| 10 | 0.182 | 0.175 | =AVERAGE(B3,C3) | =SLOPE*A3+INTERCEPT |

Keep the fit parameters (slope, intercept, R²) in clearly labeled cells below or beside the table. Flag any standard point that deviates significantly from the fit — it may indicate a preparation error.

Extrapolation beyond the validated range should always be flagged with a conditional format or note. If blanks, standards, or QC samples fail acceptance criteria, the run should not be used without explicit justification.

## Dose-response and IC50 / EC50

Dose-response work should use concentration on a log scale (base 10) for the x-axis and response on a clearly defined normalized scale for the y-axis. Keep raw concentrations, log-transformed concentrations, normalized response, fit assumptions, and final parameter estimates in separate columns.

**Example dose-response table:**

| Conc_nM | Log_Conc | Raw_Signal | Normalized_% | Fit_% |
|---|---|---|---|---|
| 0.1 | -1 | 98.2 | 100.0 | — |
| 1 | 0 | 95.1 | 96.8 | =fitted value |
| 10 | 1 | 72.4 | 73.8 | =fitted value |
| 100 | 2 | 31.6 | 32.2 | =fitted value |
| 1000 | 3 | 8.9 | 9.1 | =fitted value |

Normalization should reference the method explicitly: "% of vehicle control" or "% of max response." Report IC50/EC50 with units and confidence intervals when available. A crude two-point interpolation is insufficient when proper curve fitting is expected — flag the limitation if Excel's built-in tools are insufficient and recommend GraphPad Prism or Python (scipy.optimize.curve_fit) for four-parameter logistic fits.

## Pharmacokinetic parameter tables

PK summary tables should clearly report units and calculation methods for core parameters.

**Example PK summary layout:**

| Parameter | Units | Subject 1 | Subject 2 | Subject 3 | Mean | SD | Method |
|---|---|---|---|---|---|---|---|
| Cmax | ng/mL | 342 | 289 | 315 | 315.3 | 26.5 | Observed |
| Tmax | h | 2.0 | 1.5 | 2.0 | 1.83 | 0.29 | Observed |
| AUC₀₋₂₄ | ng·h/mL | 2840 | 2510 | 2690 | 2680 | 165 | Linear trapezoidal |
| t½ | h | 8.2 | 7.9 | 8.5 | 8.20 | 0.30 | Terminal log-linear |
| CL/F | L/h | 3.52 | 3.98 | 3.72 | 3.74 | 0.23 | Dose/AUC₀₋∞ |
| Vd/F | L | 41.7 | 45.4 | 45.6 | 44.2 | 2.2 | CL/F × t½/0.693 |

Keep subject-level values separate from cohort summaries. Use the Method column to make calculation assumptions transparent — a reviewer should be able to verify each parameter.

## Nanoparticle characterization data

Nanoparticle (NP) formulation data has specific layout requirements that standard lab templates often miss.

### Particle sizing (DLS)

**Example DLS summary:**

| Batch_ID | Formulation | Z_Avg_nm | PDI | Peak1_nm | Peak1_% | Peak2_nm | Peak2_% | Instrument | Date |
|---|---|---|---|---|---|---|---|---|---|
| NP-2025-001 | PLGA 50:50 5% PVA | 185.3 | 0.124 | 178.9 | 98.2 | 1420 | 1.8 | Zetasizer Ultra | 2025-03-15 |

Report the Z-average (intensity-weighted), PDI, and individual peak data. A PDI above 0.3 warrants a note. If the correlation function was poor or the count rate was outside the optimal range, flag the measurement as potentially unreliable.

### Zeta potential

| Batch_ID | Zeta_mV | Zeta_SD_mV | Conductivity_mS_cm | Dispersant | pH | Temp_C |
|---|---|---|---|---|---|---|
| NP-2025-001 | -28.4 | 3.2 | 0.045 | Water | 7.0 | 25 |

Report the dispersant, pH, and temperature — zeta potential is meaningless without these contextual parameters. If the measurement was taken in buffer, note the ionic strength.

### Encapsulation efficiency

| Batch_ID | Drug_Loaded_mg | Total_Drug_mg | EE_% | DL_% | Method |
|---|---|---|---|---|---|
| NP-2025-001 | 4.82 | 5.00 | 96.4 | 8.7 | Direct (dissolve NP, quantify by HPLC) |

Show the calculation path: EE% = (Drug in NP / Total Drug Added) × 100. Drug Loading % = (Drug in NP / Total NP Mass) × 100. Document whether the method is direct (dissolve and quantify) or indirect (measure unencapsulated drug in supernatant).

## Drug release kinetics

Release study data should track cumulative and non-cumulative release over time with clear sink condition documentation.

**Example release table:**

| Time_h | Conc_µg_mL | Vol_Sampled_mL | Vol_Replaced_mL | Drug_Released_µg | Cumulative_Released_µg | Cumulative_% |
|---|---|---|---|---|---|---|
| 0.5 | 2.14 | 1.0 | 1.0 | 42.8 | 42.8 | 4.28 |
| 1 | 1.87 | 1.0 | 1.0 | 37.4 | 80.2 | 8.02 |
| 2 | 3.21 | 1.0 | 1.0 | 64.2 | 144.4 | 14.44 |

The cumulative release calculation must account for drug removed in previous samples — this is a common error. If the total release volume changes (media replacement), the correction factor should be visible in the formula, not buried.

For kinetic model fitting (zero-order, first-order, Higuchi, Korsmeyer-Peppas), keep the fit parameters in a separate summary table with R² values. If Excel's Solver or trendline tools are insufficient for the model, recommend Python (scipy) or dedicated release kinetics software.

## Stability study tracking

ICH-style stability data should be organized for both trending and regulatory reporting.

**Example stability layout:**

| Batch_ID | Storage_Condition | Timepoint_Months | Particle_Size_nm | PDI | Zeta_mV | EE_% | Potency_% | Appearance |
|---|---|---|---|---|---|---|---|---|
| NP-2025-001 | 25°C/60%RH | 0 | 185.3 | 0.124 | -28.4 | 96.4 | 100.0 | Clear suspension |
| NP-2025-001 | 25°C/60%RH | 1 | 188.7 | 0.131 | -27.1 | 95.8 | 99.2 | Clear suspension |
| NP-2025-001 | 40°C/75%RH | 0 | 185.3 | 0.124 | -28.4 | 96.4 | 100.0 | Clear suspension |
| NP-2025-001 | 40°C/75%RH | 1 | 201.4 | 0.186 | -24.2 | 91.1 | 96.8 | Slight turbidity |

Storage conditions should follow ICH nomenclature. Trending charts should show each condition as a separate series with specification limits as reference lines.

## Error propagation and uncertainty

Where calculations combine measured values, note uncertainty sources. For independent errors being combined through addition/subtraction, propagate as root-sum-of-squares of absolute uncertainties. For multiplication/division, propagate as root-sum-of-squares of relative uncertainties. Report the resulting uncertainty with the final estimate.

**Example:**

If Concentration = Mass / Volume, and Mass = 5.0 ± 0.1 mg, Volume = 10.0 ± 0.2 mL:
- Relative uncertainty in mass: 0.1/5.0 = 2.0%
- Relative uncertainty in volume: 0.2/10.0 = 2.0%
- Combined relative uncertainty: √(2.0² + 2.0²) = 2.83%
- Concentration = 0.50 ± 0.014 mg/mL

Show this calculation path in helper columns, not just the final result.

## Significant figures and rounding

Round late, display late. Calculate with full precision, but present values with scientifically defensible significant figures. Means, SDs, concentrations, and fitted parameters should reflect measurement reality, not Excel's default 15-digit display.

**Practical rules:** Report the mean to one more significant figure than the raw data. Report the SD to 1-2 significant figures. Report IC50/EC50 to 2-3 significant figures. Format cells to display the correct precision — never round the underlying value in the cell.

## GxP and regulatory awareness

In regulated contexts, Excel is a calculation surface, not a compliance guarantee. If the workbook supports GxP work:

- Use locked formulas and controlled inputs
- Add visible checks with pass/fail indicators
- Include version and date stamps
- Document validation: test normal, boundary, and failure cases
- Be aware that Excel alone does not satisfy 21 CFR Part 11 expectations for electronic records and signatures — additional controls (audit trail, access control, electronic signatures) require purpose-built systems

## Grant budget templates

For NIH-style budgets, maintain a clean assumptions section for salary, effort (% FTE or calendar months), fringe rates, equipment (>$5K threshold), travel, supplies, consortium costs (F&A on first $25K), and indirect cost rates.

**Example assumptions block:**

| Item | Value | Source |
|---|---|---|
| PI Salary | $95,000 | Institutional base |
| PI Effort | 20% (2.4 cal months) | Grant commitment |
| Fringe Rate | 32.5% | FY2025 institutional rate |
| F&A Rate | 56.5% MTDC | Negotiated rate agreement |
| Graduate RA | $35,000/yr | Dept standard |
| Tuition Remission | $54,000/yr | Brown FY2025 |

Even when a modular budget ($250K modules) is the submission surface, keep the underlying detailed budget transparent for internal review and Just-in-Time documentation. The detailed budget should tie exactly to the modular request — reviewers will notice if the numbers don't add up.
