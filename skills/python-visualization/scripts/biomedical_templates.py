"""Biomedical visualization templates with curve fitting.

Provides ready-to-use functions for common biomedical plots:
- Dose-response curves with IC50 extraction
- Pharmacokinetic profiles (linear and semi-log)
- Drug release kinetics with model comparison
- Kaplan-Meier survival curves with log-rank test
- Particle size distribution with D10/D50/D90
- Biodistribution bar charts
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.stats import gaussian_kde


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------

def hill_equation(x, bottom, top, ic50, n_hill):
    """4-parameter logistic (Hill equation) for dose-response."""
    return bottom + (top - bottom) / (1 + (ic50 / x) ** n_hill)


def one_compartment_oral(t, F_D_over_Vd, ka, ke):
    """One-compartment oral PK model (simplified).
    C(t) = (F*D/Vd) * ka/(ka-ke) * (exp(-ke*t) - exp(-ka*t))
    """
    return F_D_over_Vd * ka / (ka - ke) * (np.exp(-ke * t) - np.exp(-ka * t))


def first_order_release(t, Q_inf, k1):
    """First-order release: Q = Q_inf * (1 - exp(-k1*t))"""
    return Q_inf * (1 - np.exp(-k1 * t))


def higuchi_release(t, k_h):
    """Higuchi model: Q = k_H * sqrt(t)"""
    return k_h * np.sqrt(t)


def korsmeyer_peppas(t, k_kp, n):
    """Korsmeyer-Peppas: Q = k * t^n"""
    return k_kp * t ** n


# ---------------------------------------------------------------------------
# Plotting functions
# ---------------------------------------------------------------------------

def plot_dose_response(concentrations, responses, response_err=None,
                       ax=None, label='Data', color='#0072B2',
                       fit=True, annotate_ic50=True, **kwargs):
    """Plot dose-response curve with optional Hill equation fit.

    Parameters
    ----------
    concentrations : array-like
        Drug concentrations (will be plotted on log scale).
    responses : array-like
        Response values (e.g. % viability).
    response_err : array-like, optional
        Error bars (SEM or SD).
    ax : matplotlib.axes.Axes, optional
    label : str
    color : str
    fit : bool
        Whether to fit Hill equation.
    annotate_ic50 : bool
        Whether to annotate IC50 on the plot.

    Returns
    -------
    dict with keys: 'ax', 'popt' (if fit), 'ic50' (if fit)
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(5, 4))

    conc = np.asarray(concentrations, dtype=float)
    resp = np.asarray(responses, dtype=float)

    # Data points
    err_kw = dict(fmt='o', capsize=3, markersize=5, color=color, label=label)
    if response_err is not None:
        ax.errorbar(conc, resp, yerr=response_err, **err_kw)
    else:
        ax.errorbar(conc, resp, **err_kw)

    result = {'ax': ax}

    if fit:
        try:
            popt, pcov = curve_fit(
                hill_equation, conc, resp,
                p0=[0, 100, np.median(conc), 1],
                bounds=([0, 50, 1e-10, 0.1], [50, 150, conc.max() * 100, 10]),
                maxfev=10000,
            )
            x_fit = np.logspace(np.log10(conc.min()), np.log10(conc.max()), 300)
            ax.plot(x_fit, hill_equation(x_fit, *popt), '-', color=color,
                    linewidth=1.5, label=f'Fit (IC₅₀={popt[2]:.2f})')
            result['popt'] = popt
            result['ic50'] = popt[2]

            if annotate_ic50:
                mid_y = (popt[0] + popt[1]) / 2
                ax.axhline(y=mid_y, color='gray', linestyle=':', alpha=0.4)
                ax.axvline(x=popt[2], color='gray', linestyle=':', alpha=0.4)
                # Offset in axis-relative units to stay on-canvas regardless of
                # whether y is 0-1, 0-100, or 0-10000.
                ylo, yhi = ax.get_ylim()
                y_offset = 0.15 * (yhi - ylo)
                ax.annotate(
                    f'IC$_{{50}}$ = {popt[2]:.2f}',
                    xy=(popt[2], mid_y),
                    xytext=(popt[2] * 5, mid_y + y_offset),
                    arrowprops=dict(arrowstyle='->', color='gray'),
                    fontsize=8, color='gray',
                )
        except RuntimeError:
            pass

    ax.set_xscale('log')
    ax.set_xlabel('Concentration')
    ax.set_ylabel('Response (%)')
    ax.legend(frameon=False, fontsize=8)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    return result


def plot_pk_profile(time, concentration, conc_err=None, ax=None,
                    label='Data', color='#0072B2', semi_log=False,
                    annotate_cmax=True, shade_auc=True, **kwargs):
    """Plot pharmacokinetic concentration-time profile.

    Parameters
    ----------
    time : array-like
        Time points.
    concentration : array-like
        Plasma concentration values.
    conc_err : array-like, optional
        Error bars.
    semi_log : bool
        If True, use log scale for y-axis.
    annotate_cmax : bool
        Annotate Cmax and Tmax.
    shade_auc : bool
        Shade area under curve.

    Returns
    -------
    dict with keys: 'ax', 'cmax', 'tmax'
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(6, 4))

    t = np.asarray(time, dtype=float)
    c = np.asarray(concentration, dtype=float)

    err_kw = dict(fmt='o-', capsize=3, markersize=4, color=color,
                  linewidth=1.5, label=label)
    if conc_err is not None:
        ax.errorbar(t, c, yerr=conc_err, **err_kw)
    else:
        ax.errorbar(t, c, **err_kw)

    cmax_idx = np.argmax(c)
    cmax, tmax = c[cmax_idx], t[cmax_idx]

    if shade_auc:
        ax.fill_between(t, c, alpha=0.12, color=color)

    if annotate_cmax:
        # Use axes-fraction text position so the annotation stays on-canvas
        # regardless of concentration/time units or scale.
        ax.annotate(
            f'C$_{{max}}$ = {cmax:.1f}\nt$_{{max}}$ = {tmax:.1f}',
            xy=(tmax, cmax),
            xytext=(0.6, 0.82),
            xycoords='data',
            textcoords='axes fraction',
            arrowprops=dict(arrowstyle='->', color='gray'),
            fontsize=8, bbox=dict(boxstyle='round', fc='white', alpha=0.8),
        )

    if semi_log:
        ax.set_yscale('log')

    ax.set_xlabel('Time')
    ax.set_ylabel('Concentration')
    ax.legend(frameon=False, fontsize=8)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    return {'ax': ax, 'cmax': cmax, 'tmax': tmax}


def plot_drug_release(time, release_pct, release_err=None, ax=None,
                      label='Data', color='#0072B2', fit_models=True, **kwargs):
    """Plot cumulative drug release with model comparison.

    Parameters
    ----------
    time : array-like
        Time points (exclude t=0 or include with release=0).
    release_pct : array-like
        Cumulative release percentage.
    release_err : array-like, optional
    fit_models : bool
        Fit first-order, Higuchi, and Korsmeyer-Peppas models.

    Returns
    -------
    dict with keys: 'ax', 'fits' (model name -> {popt, r2})
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(6, 4))

    t = np.asarray(time, dtype=float)
    r = np.asarray(release_pct, dtype=float)

    err_kw = dict(fmt='ko', capsize=3, markersize=5, label=label, zorder=5)
    if release_err is not None:
        ax.errorbar(t, r, yerr=release_err, **err_kw)
    else:
        ax.errorbar(t, r, **err_kw)

    result = {'ax': ax, 'fits': {}}

    if fit_models:
        mask = t > 0
        t_pos, r_pos = t[mask], r[mask]
        t_fit = np.linspace(t_pos.min(), t_pos.max(), 300)
        ss_tot = np.sum((r_pos - np.mean(r_pos)) ** 2)

        models = [
            ('First-order', first_order_release, [100, 0.05], '#D55E00'),
            ('Higuchi', higuchi_release, [12], '#009E73'),
            ('Korsmeyer-Peppas', korsmeyer_peppas, [12, 0.5], '#CC79A7'),
        ]

        for name, func, p0, clr in models:
            try:
                popt, _ = curve_fit(func, t_pos, r_pos, p0=p0, maxfev=10000)
                y_pred = func(t_pos, *popt)
                ss_res = np.sum((r_pos - y_pred) ** 2)
                r2 = 1 - ss_res / ss_tot
                ax.plot(t_fit, func(t_fit, *popt), '-', color=clr, linewidth=1.5,
                        label=f'{name} (R²={r2:.3f})')
                result['fits'][name] = {'popt': popt, 'r2': r2}
            except RuntimeError:
                pass

    ax.set_xlabel('Time')
    ax.set_ylabel('Cumulative Release (%)')
    ax.set_ylim(0, 105)
    ax.legend(frameon=False, fontsize=8)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    return result


def plot_particle_size(sizes, ax=None, color='steelblue', show_kde=True,
                       show_percentiles=True, bins=30, **kwargs):
    """Plot particle size distribution with D10/D50/D90 and PDI.

    Parameters
    ----------
    sizes : array-like
        Particle sizes in nm.

    Returns
    -------
    dict with keys: 'ax', 'd10', 'd50', 'd90', 'pdi'
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(6, 4))

    sizes = np.asarray(sizes, dtype=float)
    ax.hist(sizes, bins=bins, density=True, alpha=0.5, color=color, edgecolor='white')

    if show_kde:
        kde = gaussian_kde(sizes)
        x_kde = np.linspace(sizes.min(), sizes.max(), 300)
        ax.plot(x_kde, kde(x_kde), 'k-', linewidth=1.5)

    d10, d50, d90 = np.percentile(sizes, [10, 50, 90])
    pdi = (np.std(sizes) / np.mean(sizes)) ** 2

    if show_percentiles:
        # Stagger y-positions so labels don't collide when D10/D50/D90 are close
        # (common with low-PDI, narrow distributions).
        ylo, yhi = ax.get_ylim()
        y_levels = [0.92, 0.76, 0.60]  # alternating lanes in axes fraction
        for (val, lbl), y_frac in zip([(d10, 'D10'), (d50, 'D50'), (d90, 'D90')], y_levels):
            ax.axvline(x=val, color='gray', linestyle='--', alpha=0.6)
            ax.text(val, ylo + y_frac * (yhi - ylo), f'{lbl}\n{val:.0f} nm',
                    ha='center', fontsize=7, color='gray',
                    bbox=dict(boxstyle='round,pad=0.1', fc='white', alpha=0.6, lw=0))

    ax.text(0.95, 0.85, f'D50 = {d50:.0f} nm\nPDI = {pdi:.3f}',
            transform=ax.transAxes, ha='right', fontsize=8,
            bbox=dict(boxstyle='round', fc='white', alpha=0.8))

    ax.set_xlabel('Particle Size (nm)')
    ax.set_ylabel('Density')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    return {'ax': ax, 'd10': d10, 'd50': d50, 'd90': d90, 'pdi': pdi}


def plot_biodistribution(organs, groups, values, errors=None, ax=None,
                         colors=None, **kwargs):
    """Plot biodistribution bar chart for multiple treatment groups.

    Parameters
    ----------
    organs : list of str
        Organ names.
    groups : list of str
        Treatment group names.
    values : list of array-like
        One array per group, matching organs length.
    errors : list of array-like, optional
        One error array per group.
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(7, 4))

    if colors is None:
        colors = ['#0072B2', '#D55E00', '#009E73', '#CC79A7', '#E69F00']

    n_groups = len(groups)
    x = np.arange(len(organs))
    width = 0.8 / n_groups

    for i, (name, vals) in enumerate(zip(groups, values)):
        err = errors[i] if errors else None
        ax.bar(x + i * width - (n_groups - 1) * width / 2, vals, width,
               yerr=err, capsize=3, label=name, color=colors[i % len(colors)],
               alpha=0.85)

    ax.set_xticks(x)
    ax.set_xticklabels(organs)
    ax.set_ylabel('% Injected Dose / g tissue')
    ax.legend(frameon=False, fontsize=8)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    return {'ax': ax}
