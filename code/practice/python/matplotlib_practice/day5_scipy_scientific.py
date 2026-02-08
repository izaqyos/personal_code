#!/usr/bin/env python3
"""
Day 5: SciPy Scientific Computing

SciPy (Scientific Python) extends NumPy with advanced scientific functions.
It provides:
- Statistical functions (distributions, tests, correlations)
- Optimization (minimize, curve fitting)
- Signal processing (FFT, filters)
- Linear algebra (eigenvalues, decompositions)
- Interpolation and integration
- Sparse matrices and spatial algorithms

WHY SCIPY?
- Production-ready implementations of complex algorithms
- Highly optimized (C/Fortran under the hood)
- Standard for scientific computing and data science
- Integrates seamlessly with NumPy and matplotlib

INSTRUCTIONS:
1. Complete each exercise by filling in the TODO sections
2. Run the script to verify your solutions
3. Check day5_scipy_scientific_answers.py if stuck
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
    """
    Exercise 1: Work with statistical distributions.
    
    TODO:
    1. Create a normal distribution with mean=100, std=15
    2. Generate 1000 random samples from it
    3. Calculate PDF (probability density function) at x=100
    4. Calculate CDF (cumulative distribution) at x=115
    5. Find the value at the 95th percentile (ppf - percent point function)
    6. Fit a normal distribution to sample data and get parameters
    
    HINTS:
    - stats.norm(loc=mean, scale=std)
    - dist.rvs(size=n) for random samples
    - dist.pdf(x) for probability density
    - dist.cdf(x) for cumulative probability
    - dist.ppf(0.95) for percentile
    - stats.norm.fit(data) returns (mean, std)
    """
    print("\n" + "="*60)
    print("Exercise 1: Statistical Distributions")
    print("="*60)
    
    np.random.seed(42)
    
    # TODO: Create normal distribution (mean=100, std=15)
    normal_dist = None  # stats.norm(loc=..., scale=...)
    
    # TODO: Generate 1000 random samples
    samples = None  # normal_dist.rvs(size=...)
    
    # TODO: PDF at x=100
    pdf_at_100 = None
    
    # TODO: CDF at x=115 (probability that X <= 115)
    cdf_at_115 = None
    
    # TODO: 95th percentile value
    percentile_95 = None
    
    # TODO: Fit distribution to samples and get parameters
    fitted_mean, fitted_std = None, None  # stats.norm.fit(samples)
    
    # Verification
    # print(f"PDF at mean: {pdf_at_100:.6f}")
    # print(f"P(X <= 115): {cdf_at_115:.4f}")
    # print(f"95th percentile: {percentile_95:.2f}")
    # print(f"Fitted: mean={fitted_mean:.2f}, std={fitted_std:.2f}")
    
    print("Exercise 1: Not implemented yet - fill in the TODOs!")


def exercise_2_statistical_tests():
    """
    Exercise 2: Perform statistical hypothesis tests.
    
    TODO:
    1. Perform a t-test comparing two groups
    2. Perform a chi-square test for independence
    3. Calculate Pearson correlation coefficient
    4. Perform a normality test (Shapiro-Wilk)
    5. Perform ANOVA for multiple groups
    
    HINTS:
    - stats.ttest_ind(group1, group2) for independent t-test
    - stats.chi2_contingency(contingency_table)
    - stats.pearsonr(x, y) returns (correlation, p-value)
    - stats.shapiro(data) for normality test
    - stats.f_oneway(group1, group2, group3) for ANOVA
    """
    print("\n" + "="*60)
    print("Exercise 2: Statistical Tests")
    print("="*60)
    
    np.random.seed(42)
    
    # Sample data
    group_a = np.random.normal(100, 15, 50)  # Mean 100
    group_b = np.random.normal(110, 15, 50)  # Mean 110 (different!)
    group_c = np.random.normal(105, 15, 50)  # Mean 105
    
    # TODO: Independent t-test between group_a and group_b
    t_stat, t_pvalue = None, None  # stats.ttest_ind(...)
    
    # TODO: Chi-square test
    # Contingency table: observed frequencies
    observed = np.array([[30, 10], [15, 45]])
    chi2, chi_pvalue, dof, expected = None, None, None, None  # stats.chi2_contingency(...)
    
    # TODO: Pearson correlation
    x = np.arange(50)
    y = x * 2 + np.random.randn(50) * 5  # Strong positive correlation
    corr, corr_pvalue = None, None  # stats.pearsonr(...)
    
    # TODO: Shapiro-Wilk normality test on group_a
    shapiro_stat, shapiro_pvalue = None, None  # stats.shapiro(...)
    
    # TODO: ANOVA across all three groups
    f_stat, anova_pvalue = None, None  # stats.f_oneway(...)
    
    # Verification
    # print(f"T-test: t={t_stat:.3f}, p={t_pvalue:.4f}")
    # print(f"Chi-square: χ²={chi2:.3f}, p={chi_pvalue:.4f}")
    # print(f"Correlation: r={corr:.3f}, p={corr_pvalue:.4f}")
    # print(f"Shapiro-Wilk: W={shapiro_stat:.4f}, p={shapiro_pvalue:.4f}")
    # print(f"ANOVA: F={f_stat:.3f}, p={anova_pvalue:.4f}")
    
    print("Exercise 2: Not implemented yet - fill in the TODOs!")


def exercise_3_optimization():
    """
    Exercise 3: Optimization and curve fitting.
    
    TODO:
    1. Find the minimum of f(x) = (x - 3)^2 + 2
    2. Find the root of f(x) = x^3 - 2x - 5
    3. Fit a polynomial to noisy data
    4. Fit a custom function using curve_fit
    
    HINTS:
    - optimize.minimize(func, x0) for minimization
    - optimize.brentq(func, a, b) for root finding
    - np.polyfit(x, y, degree) for polynomial fit
    - optimize.curve_fit(func, xdata, ydata) for custom fit
    """
    print("\n" + "="*60)
    print("Exercise 3: Optimization")
    print("="*60)
    
    np.random.seed(42)
    
    # TODO: Minimize f(x) = (x - 3)^2 + 2
    def quadratic(x):
        return (x - 3)**2 + 2
    
    result = None  # optimize.minimize(quadratic, x0=0)
    # min_x = result.x[0]
    # min_val = result.fun
    
    # TODO: Find root of x^3 - 2x - 5 = 0
    def cubic(x):
        return x**3 - 2*x - 5
    
    root = None  # optimize.brentq(cubic, 0, 3)
    
    # TODO: Polynomial fit to noisy data
    x_data = np.linspace(0, 10, 50)
    y_true = 2*x_data**2 - 3*x_data + 5
    y_noisy = y_true + np.random.randn(50) * 10
    
    # coefficients = np.polyfit(x_data, y_noisy, 2)  # Quadratic fit
    # poly = np.poly1d(coefficients)
    
    # TODO: Curve fit with custom exponential function
    def exp_func(x, a, b, c):
        return a * np.exp(-b * x) + c
    
    x_exp = np.linspace(0, 4, 50)
    y_exp = 2.5 * np.exp(-1.3 * x_exp) + 0.5 + np.random.randn(50) * 0.1
    
    # popt, pcov = optimize.curve_fit(exp_func, x_exp, y_exp)
    # a_fit, b_fit, c_fit = popt
    
    # print(f"Minimum at x={min_x:.4f}, f(x)={min_val:.4f}")
    # print(f"Root of cubic: x={root:.4f}")
    # print(f"Polynomial coefficients: {coefficients}")
    # print(f"Exponential fit: a={a_fit:.3f}, b={b_fit:.3f}, c={c_fit:.3f}")
    
    print("Exercise 3: Not implemented yet - fill in the TODOs!")


def exercise_4_interpolation():
    """
    Exercise 4: Interpolate between data points.
    
    TODO:
    1. Linear interpolation between known points
    2. Cubic spline interpolation
    3. Compare interpolation methods visually
    
    HINTS:
    - interpolate.interp1d(x, y, kind='linear')
    - interpolate.interp1d(x, y, kind='cubic')
    - interpolate.CubicSpline(x, y)
    """
    print("\n" + "="*60)
    print("Exercise 4: Interpolation")
    print("="*60)
    
    np.random.seed(42)
    
    # Known data points (sparse)
    x_known = np.array([0, 1, 2, 3, 4, 5, 6])
    y_known = np.array([0, 0.8, 0.9, 0.1, -0.8, -1.0, -0.3])
    
    # Dense x for interpolation
    x_dense = np.linspace(0, 6, 100)
    
    # TODO: Linear interpolation
    linear_interp = None  # interpolate.interp1d(x_known, y_known, kind='linear')
    # y_linear = linear_interp(x_dense)
    
    # TODO: Cubic interpolation
    cubic_interp = None  # interpolate.interp1d(x_known, y_known, kind='cubic')
    # y_cubic = cubic_interp(x_dense)
    
    # TODO: Cubic spline
    spline = None  # interpolate.CubicSpline(x_known, y_known)
    # y_spline = spline(x_dense)
    
    # TODO: Plot comparison
    # fig, ax = plt.subplots(figsize=(10, 6))
    # ax.scatter(x_known, y_known, s=100, c='red', zorder=5, label='Known points')
    # ax.plot(x_dense, y_linear, '--', label='Linear')
    # ax.plot(x_dense, y_cubic, '-', label='Cubic')
    # ax.legend()
    # plt.savefig('output/day5_ex4_interpolation.png', dpi=150)
    # plt.show()
    
    print("Exercise 4: Not implemented yet - fill in the TODOs!")


def exercise_5_signal_processing():
    """
    Exercise 5: Signal processing basics.
    
    TODO:
    1. Apply a low-pass filter to noisy signal
    2. Compute FFT (Fast Fourier Transform)
    3. Find peaks in a signal
    
    HINTS:
    - signal.butter(order, cutoff, btype='low') for filter design
    - signal.filtfilt(b, a, data) for zero-phase filtering
    - np.fft.fft(signal) and np.fft.fftfreq(n, d)
    - signal.find_peaks(data, height=..., distance=...)
    """
    print("\n" + "="*60)
    print("Exercise 5: Signal Processing")
    print("="*60)
    
    np.random.seed(42)
    
    # Create noisy signal (sum of two sine waves + noise)
    t = np.linspace(0, 1, 1000)
    signal_clean = np.sin(2 * np.pi * 5 * t) + 0.5 * np.sin(2 * np.pi * 20 * t)
    noise = np.random.randn(1000) * 0.5
    signal_noisy = signal_clean + noise
    
    # TODO: Design and apply low-pass Butterworth filter
    # Order 4, cutoff at 10 Hz (assuming sample rate = 1000 Hz)
    # b, a = signal.butter(4, 10/(1000/2), btype='low')
    # signal_filtered = signal.filtfilt(b, a, signal_noisy)
    
    # TODO: Compute FFT
    # fft_result = np.fft.fft(signal_clean)
    # frequencies = np.fft.fftfreq(len(t), t[1] - t[0])
    # magnitude = np.abs(fft_result)
    
    # TODO: Find peaks in the original signal
    # peaks, properties = signal.find_peaks(signal_clean, height=0.5, distance=50)
    
    # Plot results
    # fig, axes = plt.subplots(3, 1, figsize=(12, 10))
    # axes[0].plot(t, signal_noisy, alpha=0.5, label='Noisy')
    # axes[0].plot(t, signal_filtered, label='Filtered')
    # axes[0].set_title('Low-pass Filter')
    # axes[0].legend()
    
    # axes[1].plot(frequencies[:500], magnitude[:500])
    # axes[1].set_title('FFT Magnitude Spectrum')
    # axes[1].set_xlabel('Frequency (Hz)')
    
    # axes[2].plot(t, signal_clean)
    # axes[2].plot(t[peaks], signal_clean[peaks], 'rx', markersize=10)
    # axes[2].set_title('Peak Detection')
    
    # plt.tight_layout()
    # plt.savefig('output/day5_ex5_signal.png', dpi=150)
    # plt.show()
    
    print("Exercise 5: Not implemented yet - fill in the TODOs!")


def exercise_6_integration():
    """
    Exercise 6: Numerical integration.
    
    TODO:
    1. Integrate a simple function analytically known
    2. Integrate with sample data (trapezoid rule)
    3. Solve an ODE (ordinary differential equation)
    
    HINTS:
    - integrate.quad(func, a, b) for definite integral
    - integrate.trapezoid(y, x) for sampled data
    - integrate.odeint(deriv, y0, t) for ODEs
    """
    print("\n" + "="*60)
    print("Exercise 6: Integration")
    print("="*60)
    
    # TODO: Integrate sin(x) from 0 to pi (should be 2.0)
    def sin_func(x):
        return np.sin(x)
    
    # result, error = integrate.quad(sin_func, 0, np.pi)
    # print(f"∫sin(x)dx from 0 to π = {result:.6f} (error: {error:.2e})")
    
    # TODO: Integrate sampled data using trapezoid rule
    x_samples = np.linspace(0, 1, 100)
    y_samples = x_samples**2  # ∫x²dx from 0 to 1 = 1/3 ≈ 0.333
    
    # area = integrate.trapezoid(y_samples, x_samples)
    # print(f"∫x²dx from 0 to 1 ≈ {area:.6f} (exact: 0.333333)")
    
    # TODO: Solve ODE: dy/dt = -0.5 * y (exponential decay)
    # Initial condition: y(0) = 1
    # Exact solution: y(t) = e^(-0.5t)
    
    def decay(y, t):
        return -0.5 * y
    
    t_span = np.linspace(0, 10, 100)
    y0 = [1.0]
    
    # solution = integrate.odeint(decay, y0, t_span)
    # exact = np.exp(-0.5 * t_span)
    
    # Compare numerical and exact
    # plt.figure(figsize=(10, 6))
    # plt.plot(t_span, solution, 'b-', label='Numerical (odeint)')
    # plt.plot(t_span, exact, 'r--', label='Exact')
    # plt.xlabel('Time')
    # plt.ylabel('y(t)')
    # plt.title('ODE Solution: dy/dt = -0.5y')
    # plt.legend()
    # plt.savefig('output/day5_ex6_ode.png', dpi=150)
    # plt.show()
    
    print("Exercise 6: Not implemented yet - fill in the TODOs!")


def main():
    """Run all exercises."""
    print("\n" + "="*60)
    print("DAY 5: SCIPY SCIENTIFIC COMPUTING")
    print("="*60)
    print("\nSciPy provides advanced scientific computing capabilities.")
    print("Complete each exercise by filling in the TODO sections.")
    
    exercise_1_statistical_distributions()
    exercise_2_statistical_tests()
    exercise_3_optimization()
    exercise_4_interpolation()
    exercise_5_signal_processing()
    exercise_6_integration()
    
    print("\n" + "="*60)
    print("Complete the TODOs and run again to verify!")
    print("="*60)


if __name__ == "__main__":
    main()
