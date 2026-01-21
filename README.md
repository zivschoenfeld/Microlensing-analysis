# OGLE-IV Gravitational Microlensing Analysis Pipeline

![Status](https://img.shields.io/badge/Status-Active-success)
![Python](https://img.shields.io/badge/Python-3.x-blue)
![License](https://img.shields.io/badge/License-MIT-green)
## 📌 Overview
This repository hosts an **independent reanalysis pipeline** for gravitational microlensing events from the **OGLE-IV survey**.

Developed as part of a lab project for the **Physics Laboratory C** course at **Tel Aviv University**, this tool validates the physical parameters of microlensing events (e.g., OGLE-2024-BLG-0393) by implementing a custom statistical pipeline that performs:
1.  **Data Processing:** Processing raw photometric data from the Early Warning System.
2.  **Theoretical Modeling:** Fitting the Paczyński Single Lens Model (PSPL).
3.  **Statistical Inference:** robust parameter estimation and data fitting using statistical methods such as: Linear Least Squares, Bootstrap, Non-Linear Optimization, and Likelihood Grid Search.

## 🚀 Key Features & Methodology
The pipeline executes the following scientific workflow:

1.  **Data Ingestion:** User-configurable loading of photometric data.
2.  **Preprocessing:** Automated cleaning and conversion of astronomical Magnitude to linear Flux.
3.  **Initialization (Linear Fit):** Fits a Paczyński curve using **Linear Least Squares (LLS)** by approximating the peak as a parabola to derive initial parameter guesses ($t_0, u_{min}, \tau$).
4.  **Bootstrap Analysis:** Estimates confidence intervals for the linear fit using **Bootstrap Resampling**.
5.  **Optimization (Non-Linear Fit):** Performs a full **Non-Linear Least Squares** fit (Levenberg-Marquardt algorithm) to refine the physical model over the entire dataset.
6.  **Uncertainty Quantification:** Visualizes parameter probability distributions and correlations using a **4D Grid Search** and **Corner Plots**.

## ⚠️ Data Usage (Manual Action Required)
**Important:** The raw photometric data is proprietary to the OGLE project and is **not included** in this repository.

To reproduce the analysis for a specific event (e.g., `OGLE-2024-BLG-0393`):

1.  Visit the [OGLE Early Warning System (EWS)](https://ogle.astrouw.edu.pl/ogle4/ews/ews.html).
2.  Navigate to the specific event page.
3.  Download the file named `phot.dat`.
4.  **Rename** the file to match the format: `OGLE-YYYY-BLG-XXXX.dat`.
5.  Place the file in the root directory of this repository.

**Citation:**
> Udalski et al., 2015, Acta Astron., 65, 1.

## 🛠️ Tech Stack
* **Core:** `Python 3.x`, `NumPy`, `Pandas`
* **Scientific Computing:** `SciPy` (Optimization & Signal Processing)
* **Visualization:** `Matplotlib`, `Seaborn`, `Corner.py`

## 📂 Project Structure
```text
├── main.ipynb            # Main analysis notebook (Configuration, Fitting, Visualization)
├── model_utils.py        # Library of physical models (Paczyński) and analysis functions.
├── requirements.txt      # Python dependencies           
└── README.md             # Project documentation
 ```




## Collaborators

<!-- readme: collaborators -start -->
<!-- readme: collaborators -end -->

## Contributors

<!-- readme: contributors -start -->
<!-- readme: contributors -end -->
Thanks to the following contributors:
- [Ziv Schoenfeld](https://github.com/zivschoenfeld)
- [Tomer Lahav](https://github.com/TomerLahav)
