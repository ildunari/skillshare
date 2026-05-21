# Biomedical Visualization Reference

Templates and patterns for drug delivery, pharmacology, and biomedical research figures.


## Contents

- [Dose-Response Curves](#dose-response-curves)
- [Pharmacokinetic Profiles](#pharmacokinetic-profiles)
- [Drug Release Kinetics](#drug-release-kinetics)
- [Kaplan-Meier Survival Curves](#kaplan-meier-survival-curves)
- [Particle Size Distribution](#particle-size-distribution)
- [Zeta Potential](#zeta-potential)
- [Biodistribution](#biodistribution)
- [Multi-Panel Figure Template](#multi-panel-figure-template)
- [Style Notes](#style-notes)

## Dose-Response Curves

### 4-Parameter Logistic (Hill Equation)

$$y = \text{Bottom} + \frac{\text{Top} - \text{Bottom}}{1 + (IC_{50}/x)^{n_H}}$$

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

def hill_equation(x, bottom, top, ic50, n_hill):
    """4-parameter logistic (Hill equation) for dose-response."""
    return bottom + (top - bottom) / (1 + (ic50 / x)**n_hill)

# Example data
concentrations = np.array([0.001, 0.01, 0.1, 1, 10, 100, 1000])  # uM
response = np.array([98, 95, 85, 52, 18, 5, 2])                    # % viability
response_sem = np.array([3, 4, 5, 6, 4, 3, 2])

# Fit
popt, pcov = curve_fit(hill_equation, concentrations, response,
                        p0=[0, 100, 1, 1],  # initial guess
                        bounds=([0, 50, 1e-6, 0.1], [50, 150, 1e6, 10]))
bottom, top, ic50, n_hill = popt
perr = np.sqrt(np.diag(pcov))  # standard errors

# Plot
fig, ax = plt.subplots(figsize=(5, 4))
x_fit = np.logspace(-3, 3, 200)
ax.errorbar(concentrations, response, yerr=response_sem, fmt='ko',
            capsize=3, markersize=5, label='Data')
ax.plot(x_fit, hill_equation(x_fit, *popt), 'b-', linewidth=1.5, label='Fit')

# IC50 annotation
ax.axhline(y=(top + bottom)/2, color='gray', linestyle=':', alpha=0.5)
ax.axvline(x=ic50, color='gray', linestyle=':', alpha=0.5)
# Offset relative to y-axis range so annotation stays on-canvas for any unit scale.
ylo, yhi = ax.get_ylim()
y_offset = 0.15 * (yhi - ylo)
ax.annotate(f'IC$_{{50}}$ = {ic50:.2f} µM', xy=(ic50, (top+bottom)/2),
            xytext=(ic50*10, (top+bottom)/2 + y_offset),
            arrowprops=dict(arrowstyle='->', color='gray'),
            fontsize=9, color='gray')

ax.set_xscale('log')
ax.set_xlabel('Concentration (µM)')
ax.set_ylabel('Cell Viability (%)')
ax.set_title('Dose-Response Curve')
ax.legend(frameon=False)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
fig.savefig('dose_response.png', dpi=300, bbox_inches='tight')
```

### Multi-compound overlay

```python
fig, ax = plt.subplots(figsize=(6, 4))
colors = ['#0072B2', '#D55E00', '#009E73', '#CC79A7']

for i, (name, conc, resp) in enumerate(compounds):
    popt, _ = curve_fit(hill_equation, conc, resp, p0=[0, 100, 1, 1],
                         bounds=([0, 50, 1e-6, 0.1], [50, 150, 1e6, 10]))
    x_fit = np.logspace(np.log10(conc.min()), np.log10(conc.max()), 200)
    ax.plot(x_fit, hill_equation(x_fit, *popt), '-', color=colors[i],
            linewidth=1.5, label=f'{name} (IC₅₀={popt[2]:.2f})')
    ax.plot(conc, resp, 'o', color=colors[i], markersize=4)

ax.set_xscale('log')
ax.set_xlabel('Concentration (µM)')
ax.set_ylabel('Cell Viability (%)')
ax.legend(frameon=False, fontsize=8)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
```

## Pharmacokinetic Profiles

### Single-compartment model

```python
def one_compartment_iv(t, C0, ke):
    """One-compartment IV bolus: C(t) = C0 * exp(-ke*t)"""
    return C0 * np.exp(-ke * t)

def one_compartment_oral(t, F, D, Vd, ka, ke):
    """One-compartment oral: C(t) = (F*D*ka)/(Vd*(ka-ke)) * (exp(-ke*t) - exp(-ka*t))"""
    return (F * D * ka) / (Vd * (ka - ke)) * (np.exp(-ke * t) - np.exp(-ka * t))
```

### PK profile plot

```python
fig, ax = plt.subplots(figsize=(6, 4))

time = np.array([0, 0.5, 1, 2, 4, 8, 12, 24, 48])  # hours
conc = np.array([0, 45, 82, 65, 38, 15, 7, 1.5, 0.3])  # ng/mL
conc_sem = np.array([0, 5, 8, 7, 4, 2, 1, 0.5, 0.1])

# Fit
popt, _ = curve_fit(one_compartment_oral, time[1:], conc[1:],
                     p0=[0.8, 100, 50, 2, 0.1])
t_fit = np.linspace(0.01, 48, 500)
c_fit = one_compartment_oral(t_fit, *popt)

# Linear scale
ax.errorbar(time, conc, yerr=conc_sem, fmt='ko', capsize=3, markersize=5)
ax.plot(t_fit, c_fit, 'b-', linewidth=1.5)

# Cmax and Tmax
cmax_idx = np.argmax(c_fit)
cmax, tmax = c_fit[cmax_idx], t_fit[cmax_idx]
ax.annotate(f'C$_{{max}}$ = {cmax:.1f} ng/mL\nt$_{{max}}$ = {tmax:.1f} h',
            xy=(tmax, cmax),
            xytext=(0.6, 0.82),         # axes fraction — stays on-canvas for any scale
            xycoords='data', textcoords='axes fraction',
            arrowprops=dict(arrowstyle='->', color='gray'), fontsize=8)

# AUC shading
ax.fill_between(t_fit, c_fit, alpha=0.15, color='blue', label='AUC')

ax.set_xlabel('Time (hours)')
ax.set_ylabel('Plasma Concentration (ng/mL)')
ax.legend(frameon=False)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
```

### Semi-log PK plot

```python
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))

# Linear
ax1.errorbar(time, conc, yerr=conc_sem, fmt='ko', capsize=3, markersize=4)
ax1.plot(t_fit, c_fit, 'b-', linewidth=1.5)
ax1.set_xlabel('Time (hours)')
ax1.set_ylabel('Concentration (ng/mL)')
ax1.set_title('Linear Scale')

# Semi-log
ax2.errorbar(time[1:], conc[1:], yerr=conc_sem[1:], fmt='ko', capsize=3, markersize=4)
ax2.plot(t_fit, c_fit, 'b-', linewidth=1.5)
ax2.set_yscale('log')
ax2.set_xlabel('Time (hours)')
ax2.set_ylabel('Concentration (ng/mL)')
ax2.set_title('Semi-Log Scale')

for ax in [ax1, ax2]:
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
fig.tight_layout()
```

## Drug Release Kinetics

### Release models

```python
def zero_order(t, k0):
    """Zero order: Q = k0 * t"""
    return k0 * t

def first_order(t, Q_inf, k1):
    """First order: Q = Q_inf * (1 - exp(-k1*t))"""
    return Q_inf * (1 - np.exp(-k1 * t))

def higuchi(t, k_h):
    """Higuchi: Q = k_H * sqrt(t)"""
    return k_h * np.sqrt(t)

def korsmeyer_peppas(t, k_kp, n):
    """Korsmeyer-Peppas: Q = k * t^n"""
    return k_kp * t**n

def hixson_crowell(t, Q_inf, k_hc):
    """Hixson-Crowell: Q_inf^(1/3) - Q^(1/3) = k_HC * t"""
    return Q_inf * (1 - (1 - k_hc * t / Q_inf**(1/3))**3)
```

### Drug release plot with model comparison

```python
time_h = np.array([0, 0.5, 1, 2, 4, 8, 12, 24, 48, 72])
release_pct = np.array([0, 12, 18, 28, 42, 58, 68, 82, 91, 95])
release_std = np.array([0, 2, 3, 3, 4, 5, 4, 3, 2, 1])

fig, ax = plt.subplots(figsize=(6, 4))

# Data
ax.errorbar(time_h, release_pct, yerr=release_std, fmt='ko',
            capsize=3, markersize=5, label='Data', zorder=5)

# Fit models
t_fit = np.linspace(0.01, 72, 500)
models = {
    'First-order': (first_order, [100, 0.05]),
    'Higuchi': (higuchi, [12]),
    'Korsmeyer-Peppas': (korsmeyer_peppas, [12, 0.5]),
}
colors = ['#0072B2', '#D55E00', '#009E73']

for (name, (func, p0)), color in zip(models.items(), colors):
    try:
        popt, _ = curve_fit(func, time_h[1:], release_pct[1:], p0=p0,
                             maxfev=5000)
        y_fit = func(t_fit, *popt)
        y_pred = func(time_h[1:], *popt)
        ss_res = np.sum((release_pct[1:] - y_pred)**2)
        ss_tot = np.sum((release_pct[1:] - np.mean(release_pct[1:]))**2)
        r2 = 1 - ss_res / ss_tot
        ax.plot(t_fit, y_fit, '-', color=color, linewidth=1.5,
                label=f'{name} (R²={r2:.3f})')
    except RuntimeError:
        pass

ax.set_xlabel('Time (hours)')
ax.set_ylabel('Cumulative Release (%)')
ax.set_ylim(0, 105)
ax.legend(frameon=False, fontsize=8)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
fig.savefig('drug_release.png', dpi=300, bbox_inches='tight')
```

### Release mechanism interpretation

| Korsmeyer-Peppas n value | Release mechanism | Geometry |
|---|---|---|
| 0.5 | Fickian diffusion | Sphere |
| 0.45 | Fickian diffusion | Cylinder |
| 0.43 | Fickian diffusion | Thin film |
| 0.5 < n < 1.0 | Anomalous transport | — |
| 1.0 | Case II transport (zero-order) | — |
| > 1.0 | Super Case II | — |

## Kaplan-Meier Survival Curves

Requires `lifelines` library: `pip install lifelines`

```python
from lifelines import KaplanMeierFitter
from lifelines.statistics import logrank_test
import matplotlib.pyplot as plt

# Example data
time_control = np.array([5, 8, 12, 15, 18, 20, 22, 25, 28, 30])
event_control = np.array([1, 1, 1, 0, 1, 1, 0, 1, 0, 1])  # 1=event, 0=censored
time_treatment = np.array([10, 15, 20, 25, 28, 30, 32, 35, 38, 40])
event_treatment = np.array([1, 0, 1, 0, 1, 0, 0, 1, 0, 0])

fig, ax = plt.subplots(figsize=(6, 4))

kmf_control = KaplanMeierFitter()
kmf_control.fit(time_control, event_control, label='Control')
kmf_control.plot_survival_function(ax=ax, ci_show=True, color='#D55E00')

kmf_treatment = KaplanMeierFitter()
kmf_treatment.fit(time_treatment, event_treatment, label='Treatment')
kmf_treatment.plot_survival_function(ax=ax, ci_show=True, color='#0072B2')

# Log-rank test
results = logrank_test(time_control, time_treatment,
                        event_control, event_treatment)
ax.text(0.6, 0.9, f'Log-rank p = {results.p_value:.4f}',
        transform=ax.transAxes, fontsize=9,
        bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

ax.set_xlabel('Time (days)')
ax.set_ylabel('Survival Probability')
ax.set_ylim(0, 1.05)
ax.legend(frameon=False)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
fig.savefig('kaplan_meier.png', dpi=300, bbox_inches='tight')
```

## Particle Size Distribution

```python
fig, ax = plt.subplots(figsize=(6, 4))

sizes = np.random.lognormal(mean=np.log(200), sigma=0.3, size=500)  # nm

# Histogram + KDE
ax.hist(sizes, bins=30, density=True, alpha=0.5, color='steelblue', edgecolor='white')
from scipy.stats import gaussian_kde
kde = gaussian_kde(sizes)
x_kde = np.linspace(sizes.min(), sizes.max(), 200)
ax.plot(x_kde, kde(x_kde), 'k-', linewidth=1.5)

# D10, D50, D90 lines
# Stagger y-positions so labels don't overlap when PDI is low (narrow distribution).
d10, d50, d90 = np.percentile(sizes, [10, 50, 90])
ylo, yhi = ax.get_ylim()
y_levels = [0.92, 0.76, 0.60]   # alternating lanes — top, mid, lower
for (val, label), y_frac in zip([(d10, 'D10'), (d50, 'D50'), (d90, 'D90')], y_levels):
    ax.axvline(x=val, color='gray', linestyle='--', alpha=0.7)
    ax.text(val, ylo + y_frac * (yhi - ylo), f'{label}\n{val:.0f} nm',
            ha='center', fontsize=8, color='gray',
            bbox=dict(boxstyle='round,pad=0.1', fc='white', alpha=0.6, lw=0))

pdi = (np.std(sizes) / np.mean(sizes))**2
ax.text(0.95, 0.85, f'D50 = {d50:.0f} nm\nPDI = {pdi:.3f}',
        transform=ax.transAxes, ha='right', fontsize=9,
        bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

ax.set_xlabel('Particle Size (nm)')
ax.set_ylabel('Density')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
```

## Zeta Potential

```python
fig, ax = plt.subplots(figsize=(6, 4))

zeta_values = np.random.normal(loc=-28, scale=5, size=300)  # mV

ax.hist(zeta_values, bins=25, density=True, alpha=0.6, color='steelblue', edgecolor='white')
kde = gaussian_kde(zeta_values)
x_kde = np.linspace(zeta_values.min(), zeta_values.max(), 200)
ax.plot(x_kde, kde(x_kde), 'k-', linewidth=1.5)

# Stability zones
zones = [(-100, -30, '#c6efce', 'Highly stable'),
         (-30, -20, '#ffeb9c', 'Moderately stable'),
         (-20, 20, '#ffc7ce', 'Unstable'),
         (20, 30, '#ffeb9c', 'Moderately stable'),
         (30, 100, '#c6efce', 'Highly stable')]

for x0, x1, color, label in zones:
    ax.axvspan(x0, x1, alpha=0.15, color=color)

mean_zeta = np.mean(zeta_values)
ax.text(0.95, 0.85, f'ζ = {mean_zeta:.1f} ± {np.std(zeta_values):.1f} mV',
        transform=ax.transAxes, ha='right', fontsize=9,
        bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

ax.set_xlabel('Zeta Potential (mV)')
ax.set_ylabel('Density')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
```

## Biodistribution

```python
fig, ax = plt.subplots(figsize=(7, 4))

organs = ['Liver', 'Spleen', 'Kidney', 'Lung', 'Heart', 'Brain', 'Tumor']
control = [12, 8, 5, 3, 1.5, 0.5, 2]
treatment = [6, 4, 4, 2, 1, 0.3, 8]
control_err = [1.5, 1, 0.8, 0.5, 0.3, 0.1, 0.5]
treatment_err = [0.8, 0.6, 0.6, 0.3, 0.2, 0.08, 1.2]

x = np.arange(len(organs))
width = 0.35

bars1 = ax.bar(x - width/2, control, width, yerr=control_err, capsize=3,
               label='Free drug', color='#D55E00', alpha=0.8)
bars2 = ax.bar(x + width/2, treatment, width, yerr=treatment_err, capsize=3,
               label='Nanoparticle', color='#0072B2', alpha=0.8)

ax.set_xticks(x)
ax.set_xticklabels(organs)
ax.set_ylabel('% Injected Dose / g tissue')
ax.legend(frameon=False)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
```

## Multi-Panel Figure Template

Common layout for biomedical papers: synthesis + characterization + in vitro.

```python
fig = plt.figure(figsize=(7, 8))  # single column, tall
gs = fig.add_gridspec(3, 2, hspace=0.35, wspace=0.3)

ax_scheme = fig.add_subplot(gs[0, :])    # A: Synthesis scheme (full width)
ax_size = fig.add_subplot(gs[1, 0])      # B: Particle size
ax_zeta = fig.add_subplot(gs[1, 1])      # C: Zeta potential
ax_release = fig.add_subplot(gs[2, 0])   # D: Drug release
ax_viab = fig.add_subplot(gs[2, 1])      # E: Cell viability

# Label panels
for ax, label in zip([ax_scheme, ax_size, ax_zeta, ax_release, ax_viab],
                      ['A', 'B', 'C', 'D', 'E']):
    ax.text(-0.12, 1.08, label, transform=ax.transAxes,
            fontsize=14, fontweight='bold', va='top')

# ... add plots to each axes ...
fig.savefig('figure1.pdf', dpi=300, bbox_inches='tight')
```

## Style Notes

- **Prefer clean minimal style** for biomedical journals — no 3D bar charts, no gradient backgrounds.
- **Okabe-Ito palette** for colorblind safety: `['#E69F00', '#56B4E9', '#009E73', '#F0E442', '#0072B2', '#D55E00', '#CC79A7']`
- **Error bars:** Always include. Use SEM for experimental comparison, SD for describing variability.
- **Significance markers:** `*` p<0.05, `**` p<0.01, `***` p<0.001, `ns` not significant. Use bracket annotations.
- **Axis labels:** Include units in parentheses: `Concentration (µM)`, `Time (hours)`.
- **Figure sizing:** Match journal requirements exactly. See `latex-integration.md` for column width tables.