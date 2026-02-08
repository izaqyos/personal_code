#!/usr/bin/env python3
"""
Day 5: SciPy Scientific Computing - ANSWERS

Complete solutions for all Day 5 exercises.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from scipy import optimize
from scipy import interpolate
from scipy import signal
from scipy import integrate
import os

os.makedirs('output', exist_ok=True)


def exercise_1_statistical_distributions():
    """Exercise 1: Statistical distributions."""
    print("\n" + "="*60)
    print("Exercise 1: Statistical Distributions - ANSWER")
    print("="*60)
    
    np.random.seed(42)
    
    # Create normal distribution
    normal_dist = stats.norm(loc=100, scale=15)
    
    # Generate samples
    samples = normal_dist.rvs(size=1000)
    
    # PDF at x=100
    pdf_at_100 = normal_dist.pdf(100)
    print(f"PDF at mean (100): {pdf_at_100:.6f}")
    
    # CDF at x=115
    cdf_at_115 = normal_dist.cdf(115)
    print(f"P(X <= 115): {cdf_at_115:.4f} ({cdf_at_115*100:.1f}%)")
    
    # 95th percentile
    percentile_95 = normal_dist.ppf(0.95)
    print(f"95th percentile: {percentile_95:.2f}")
    
    # Fit to samples
    fitted_mean, fitted_std = stats.norm.fit(samples)
    print(f"Fitted: mean={fitted_mean:.2f}, std={fitted_std:.2f}")
    
    # Visualization
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    
    x = np.linspace(50, 150, 100)
    axes[0].plot(x, normal_dist.pdf(x), 'b-', lw=2, label='PDF')
    axes[0].hist(samples, bins=30, density=True, alpha=0.5, label='Samples')
    axes[0].axvline(100, color='r', linestyle='--', label='Mean')
    axes[0].set_title('Normal Distribution')
    axes[0].legend()
    
    axes[1].plot(x, normal_dist.cdf(x), 'g-', lw=2)
    axes[1].axhline(0.95, color='r', linestyle='--')
    axes[1].axvline(percentile_95, color='r', linestyle='--')
    axes[1].set_title('CDF with 95th Percentile')
    
    plt.tight_layout()
    plt.savefig('output/day5_ex1_distributions.png', dpi=150)
    print("✓ Saved: output/day5_ex1_distributions.png")
    plt.show()


def exercise_2_statistical_tests():
    """Exercise 2: Statistical tests."""
    print("\n" + "="*60)
    print("Exercise 2: Statistical Tests - ANSWER")
    print("="*60)
    
    np.random.seed(42)
    
    group_a = np.random.normal(100, 15, 50)
    group_b = np.random.normal(110, 15, 50)
    group_c = np.random.normal(105, 15, 50)
    
    # T-test
    t_stat, t_pvalue = stats.ttest_ind(group_a, group_b)
    print(f"T-test (A vs B): t={t_stat:.3f}, p={t_pvalue:.4f}")
    print(f"  → {'Significant' if t_pvalue < 0.05 else 'Not significant'} difference")
    
    # Chi-square
    observed = np.array([[30, 10], [15, 45]])
    chi2, chi_pvalue, dof, expected = stats.chi2_contingency(observed)
    print(f"\nChi-square: χ²={chi2:.3f}, p={chi_pvalue:.4f}, dof={dof}")
    print(f"  → {'Significant' if chi_pvalue < 0.05 else 'Not significant'} association")
    
    # Pearson correlation
    x = np.arange(50)
    y = x * 2 + np.random.randn(50) * 5
    corr, corr_pvalue = stats.pearsonr(x, y)
    print(f"\nPearson correlation: r={corr:.3f}, p={corr_pvalue:.4f}")
    
    # Shapiro-Wilk
    shapiro_stat, shapiro_pvalue = stats.shapiro(group_a)
    print(f"\nShapiro-Wilk (normality): W={shapiro_stat:.4f}, p={shapiro_pvalue:.4f}")
    print(f"  → {'Normal' if shapiro_pvalue > 0.05 else 'Non-normal'} distribution")
    
    # ANOVA
    f_stat, anova_pvalue = stats.f_oneway(group_a, group_b, group_c)
    print(f"\nANOVA: F={f_stat:.3f}, p={anova_pvalue:.4f}")
    print(f"  → {'Significant' if anova_pvalue < 0.05 else 'No significant'} difference between groups")


def exercise_3_optimization():
    """Exercise 3: Optimization."""
    print("\n" + "="*60)
    print("Exercise 3: Optimization - ANSWER")
    print("="*60)
    
    np.random.seed(42)
    
    # Minimize quadratic
    def quadratic(x):
        return (x - 3)**2 + 2
    
    result = optimize.minimize(quadratic, x0=0)
    print(f"Minimum of (x-3)²+2: x={result.x[0]:.4f}, f(x)={result.fun:.4f}")
    
    # Find root
    def cubic(x):
        return x**3 - 2*x - 5
    
    root = optimize.brentq(cubic, 0, 3)
    print(f"Root of x³-2x-5: x={root:.4f} (verify: {cubic(root):.2e})")
    
    # Polynomial fit
    x_data = np.linspace(0, 10, 50)
    y_true = 2*x_data**2 - 3*x_data + 5
    y_noisy = y_true + np.random.randn(50) * 10
    
    coefficients = np.polyfit(x_data, y_noisy, 2)
    poly = np.poly1d(coefficients)
    print(f"Polynomial fit: {coefficients[0]:.2f}x² + {coefficients[1]:.2f}x + {coefficients[2]:.2f}")
    print(f"  (True: 2x² - 3x + 5)")
    
    # Curve fit
    def exp_func(x, a, b, c):
        return a * np.exp(-b * x) + c
    
    x_exp = np.linspace(0, 4, 50)
    y_exp = 2.5 * np.exp(-1.3 * x_exp) + 0.5 + np.random.randn(50) * 0.1
    
    popt, pcov = optimize.curve_fit(exp_func, x_exp, y_exp)
    print(f"Exponential fit: a={popt[0]:.3f}, b={popt[1]:.3f}, c={popt[2]:.3f}")
    print(f"  (True: a=2.5, b=1.3, c=0.5)")
    
    # Visualization
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    
    axes[0].scatter(x_data, y_noisy, alpha=0.5, label='Noisy data')
    axes[0].plot(x_data, poly(x_data), 'r-', lw=2, label='Polynomial fit')
    axes[0].plot(x_data, y_true, 'g--', lw=2, label='True')
    axes[0].set_title('Polynomial Fitting')
    axes[0].legend()
    
    axes[1].scatter(x_exp, y_exp, alpha=0.5, label='Noisy data')
    axes[1].plot(x_exp, exp_func(x_exp, *popt), 'r-', lw=2, label='Fit')
    axes[1].set_title('Exponential Curve Fitting')
    axes[1].legend()
    
    plt.tight_layout()
    plt.savefig('output/day5_ex3_optimization.png', dpi=150)
    print("✓ Saved: output/day5_ex3_optimization.png")
    plt.show()


def exercise_4_interpolation():
    """Exercise 4: Interpolation."""
    print("\n" + "="*60)
    print("Exercise 4: Interpolation - ANSWER")
    print("="*60)
    
    x_known = np.array([0, 1, 2, 3, 4, 5, 6])
    y_known = np.array([0, 0.8, 0.9, 0.1, -0.8, -1.0, -0.3])
    x_dense = np.linspace(0, 6, 100)
    
    # Linear interpolation
    linear_interp = interpolate.interp1d(x_known, y_known, kind='linear')
    y_linear = linear_interp(x_dense)
    
    # Cubic interpolation
    cubic_interp = interpolate.interp1d(x_known, y_known, kind='cubic')
    y_cubic = cubic_interp(x_dense)
    
    # Cubic spline
    spline = interpolate.CubicSpline(x_known, y_known)
    y_spline = spline(x_dense)
    
    # Plot
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter(x_known, y_known, s=100, c='red', zorder=5, label='Known points')
    ax.plot(x_dense, y_linear, '--', label='Linear', alpha=0.7)
    ax.plot(x_dense, y_cubic, '-', label='Cubic', alpha=0.7)
    ax.plot(x_dense, y_spline, ':', label='Spline', lw=2, alpha=0.7)
    ax.set_title('Interpolation Methods')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    plt.savefig('output/day5_ex4_interpolation.png', dpi=150)
    print("✓ Saved: output/day5_ex4_interpolation.png")
    plt.show()


def exercise_5_signal_processing():
    """Exercise 5: Signal processing."""
    print("\n" + "="*60)
    print("Exercise 5: Signal Processing - ANSWER")
    print("="*60)
    
    np.random.seed(42)
    
    # Create signal
    t = np.linspace(0, 1, 1000)
    signal_clean = np.sin(2 * np.pi * 5 * t) + 0.5 * np.sin(2 * np.pi * 20 * t)
    noise = np.random.randn(1000) * 0.5
    signal_noisy = signal_clean + noise
    
    # Low-pass filter
    b, a = signal.butter(4, 10/(1000/2), btype='low')
    signal_filtered = signal.filtfilt(b, a, signal_noisy)
    
    # FFT
    fft_result = np.fft.fft(signal_clean)
    frequencies = np.fft.fftfreq(len(t), t[1] - t[0])
    magnitude = np.abs(fft_result)
    
    # Peak detection
    from scipy.signal import find_peaks
    peaks, properties = find_peaks(signal_clean, height=0.5, distance=50)
    
    # Plot
    fig, axes = plt.subplots(3, 1, figsize=(12, 10))
    
    axes[0].plot(t, signal_noisy, alpha=0.5, label='Noisy')
    axes[0].plot(t, signal_filtered, label='Filtered', lw=2)
    axes[0].set_title('Low-pass Filter (cutoff=10Hz)')
    axes[0].legend()
    
    axes[1].plot(frequencies[:500], magnitude[:500])
    axes[1].set_title('FFT Magnitude Spectrum')
    axes[1].set_xlabel('Frequency (Hz)')
    axes[1].set_ylabel('Magnitude')
    
    axes[2].plot(t, signal_clean)
    axes[2].plot(t[peaks], signal_clean[peaks], 'rx', markersize=10, label=f'{len(peaks)} peaks')
    axes[2].set_title('Peak Detection')
    axes[2].legend()
    
    plt.tight_layout()
    plt.savefig('output/day5_ex5_signal.png', dpi=150)
    print("✓ Saved: output/day5_ex5_signal.png")
    plt.show()


def exercise_6_integration():
    """Exercise 6: Numerical integration."""
    print("\n" + "="*60)
    print("Exercise 6: Integration - ANSWER")
    print("="*60)
    
    # Definite integral of sin(x) from 0 to pi
    def sin_func(x):
        return np.sin(x)
    
    result, error = integrate.quad(sin_func, 0, np.pi)
    print(f"∫sin(x)dx from 0 to π = {result:.6f} (error: {error:.2e})")
    print(f"  (Exact: 2.0)")
    
    # Trapezoid rule
    x_samples = np.linspace(0, 1, 100)
    y_samples = x_samples**2
    area = integrate.trapezoid(y_samples, x_samples)
    print(f"∫x²dx from 0 to 1 ≈ {area:.6f} (exact: 0.333333)")
    
    # ODE
    def decay(y, t):
        return -0.5 * y
    
    t_span = np.linspace(0, 10, 100)
    y0 = [1.0]
    solution = integrate.odeint(decay, y0, t_span)
    exact = np.exp(-0.5 * t_span)
    
    # Plot ODE solution
    plt.figure(figsize=(10, 6))
    plt.plot(t_span, solution, 'b-', lw=2, label='Numerical (odeint)')
    plt.plot(t_span, exact, 'r--', lw=2, label='Exact')
    plt.xlabel('Time')
    plt.ylabel('y(t)')
    plt.title('ODE Solution: dy/dt = -0.5y')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plt.savefig('output/day5_ex6_ode.png', dpi=150)
    print("✓ Saved: output/day5_ex6_ode.png")
    plt.show()


def main():
    """Run all exercises."""
    print("\n" + "="*60)
    print("DAY 5: SCIPY SCIENTIFIC COMPUTING - ANSWERS")
    print("="*60)
    
    exercise_1_statistical_distributions()
    exercise_2_statistical_tests()
    exercise_3_optimization()
    exercise_4_interpolation()
    exercise_5_signal_processing()
    exercise_6_integration()
    
    print("\n✓ All exercises completed!")


if __name__ == "__main__":
    main()
