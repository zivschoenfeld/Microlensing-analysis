import numpy as np
import scipy as sp

# ---FLUX AND MAGNITUDE CONVERSIONS---


def magnitude_to_flux(mag, mag_base):
    """Converts apparent magnitude to flux."""
    return 10 ** (-0.4 * (mag - mag_base))


def flux_to_magnitude(flux, mag_base):
    """Converts flux to apparent magnitude."""
    return -2.5 * np.log10(flux) + mag_base


def calculate_flux_err(mag, mag_err, mag_base):
    """Calculates error in flux based on magnitude error."""
    return np.abs((-0.4) * np.log(10) * 10 ** (-0.4 * (mag - mag_base)) * mag_err)


# ---THEORETICAL MICROLENSING MODELS---


def calculate_amplification(u):
    """Calculates amplification A from impact parameter u."""
    return (u**2 + 2) / (u * (u**2 + 4) ** 0.5)


def get_u_from_amplification(amp):
    """Calculates impact parameter u from amplification A (assuming A > 1)."""
    return (2 * (amp / (amp**2 - 1) ** 0.5 - 1)) ** 0.5


def calculate_u(t, t_0, u_min, tau):
    """Calculates u(t) for a single lens event."""
    return (u_min**2 + ((t - t_0) / tau) ** 2) ** 0.5


def calculate_intensity(amp, f_bl):
    """Calculates Intensity I from Amplification A and blending fraction f_bl."""
    return f_bl * amp + (1 - f_bl)


def get_amplification_from_intensity(intensity, f_bl):
    """Calculates Amplification A from Intensity I and blending fraction f_bl."""
    return (intensity - (1 - f_bl)) / f_bl


def model_flux(t, u_min, tau, t_0, f_bl=1.0):
    """Calculates model flux for given parameters."""
    u_t = calculate_u(t, t_0, u_min, tau)
    A_t = calculate_amplification(u_t)
    I_t = calculate_intensity(A_t, f_bl)
    return I_t


# ---FITTING AND STATISTICS ALGORITHMS---


def isolate_peak_data(x, y, y_err, width_right, width_left):
    """Isolating data around peak."""

    peak_idx = np.argmin(y)  # index of peak (minimum y value)

    # edges indices of peak
    start_idx = peak_idx - width_right
    end_idx = peak_idx + width_left

    # getting the data around the peak
    x_peak_data = x[start_idx:end_idx]
    y_peak_data = y[start_idx:end_idx]
    y_err_peak_data = y_err[start_idx:end_idx]

    return x_peak_data, y_peak_data, y_err_peak_data


def fit_parabolic_LLS(y, y_error, x, f_bl):
    """Fitting parabolic model to data using Linear Least Squares method."""

    x_centered = x - np.mean(x)  # centering x data to improve numerical stability

    weight = np.diag(1.0 / (y_error**2))

    f_centered = np.column_stack(
        (x_centered**2, x_centered, np.ones_like(x_centered))
    )  # x^2 + x + 1 matrix

    # covariance matrix: C = (F_T * W * F)^-1
    cov_centered = np.linalg.pinv(np.transpose(f_centered) @ weight @ f_centered)

    # jacobian to revert back to original x parameters and results:
    J = np.array(
        [
            [1, 0, 0],  # converting a
            [-2 * np.mean(x), 1, 0],  # converting b
            [np.mean(x) ** 2, -np.mean(x), 1],
        ]
    )  # converting c

    cov_original = J @ cov_centered @ J.T  # covariance matrix in original parameters

    param = (
        J @ cov_centered @ (np.transpose(f_centered) @ weight @ y)
    )  # parameters matrix for minimum chi squared: P = (F_T * W * F)^-1 * (F_T * W * y)

    param_err = np.sqrt(np.diag(cov_original))

    def y_fit(x):
        return np.polyval(param, x)  # fitted parabolic function

    dof = len(x) - len(param)  # degrees of freedom

    chi_2 = np.sum(np.square(y_fit(x) - y) @ weight)
    chi_2_red = chi_2 / dof

    p_value = sp.stats.chi2.sf(chi_2, dof)

    # Extracting t_0, u_min and tau from parabolic parameters:

    t_0 = -param[1] / (2 * param[0])

    A_max = get_amplification_from_intensity(np.polyval(param, t_0), f_bl)

    if (
        A_max >= 3 / np.sqrt(5) and param[0] < 0
    ):  # validity check for u_min real and positive
        u_min = get_u_from_amplification(A_max)

        # calculating tau:
        a, b, c = param[0], param[1], param[2] - 3 / np.sqrt(5)
        tau = abs(((-b + np.sqrt(b**2 - 4 * a * c)) / (2 * a)) - t_0) / np.sqrt(
            1 - u_min**2
        )

        return (
            param,
            param_err,
            y_fit,
            chi_2_red,
            p_value,
            t_0,
            u_min,
            tau,
        )

    else:
        return (
            param,
            param_err,
            y_fit,
            chi_2_red,
            p_value,
            np.nan,
            np.nan,
            np.nan,
        )  # returning NaN if fit is invalid


def parabolic_bootstrap(y, y_err, x, f_bl):
    """Bootstrap method to estimate uncertainties in parabolic fit parameters.
    Returns arrays of bootstrap estimates for t_0, u_0, and tau."""

    param_boot_array = []

    for i in range(10000):
        indices = np.random.randint(0, len(y), size=len(y))

        # Create the resampled dataset
        x_boot = x[indices]
        y_boot = y[indices]
        y_err_boot = y_err[indices]

        _, _, _, _, _, t_0, u_min, tau = fit_parabolic_LLS(
            y_boot, y_err_boot, x_boot, f_bl
        )

        if len(np.unique(x_boot)) > 3:  # ensuring enough unique x values for fit
            param_boot_array.append([t_0, u_min, tau])

    param_boot_array = np.array(param_boot_array)
    t_0_array = param_boot_array[:, 0]
    u_0_array = param_boot_array[:, 1]
    tau_array = param_boot_array[:, 2]

    # Remove NaNs from tau_array for mean/std calculation
    t_0_array_clean = t_0_array[~np.isnan(t_0_array)]
    u_0_array_clean = u_0_array[~np.isnan(u_0_array)]
    tau_array_clean = tau_array[~np.isnan(tau_array)]

    param_boot = [(t_0_array_clean), (u_0_array_clean), (tau_array_clean)]
    return param_boot
