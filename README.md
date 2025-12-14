# OGLE-IV Gravitational Microlensing Analysis Pipeline

![Status](https://img.shields.io/badge/Status-Work_in_Progress-yellow)
![Python](https://img.shields.io/badge/Python-3.x-blue)
![License](https://img.shields.io/badge/License-MIT-green)

## 📌 Overview
This repository contains a Python-based data analysis pipeline designed to process and model astronomical light curves from the **OGLE-IV (Optical Gravitational Lensing Experiment)** survey.

The goal of this project is to automate the detection and parameter extraction of gravitational microlensing events using statistical modeling and non-linear curve fitting.

> **Note:** This project is currently under active development. Some modules, particularly the error propagation analysis, are being refined.

## 🚀 Key Features
* **Data Processing:** Automated cleaning and conversion of photometric magnitude data to flux.
* **Statistical Modeling:** Implementation of **Chi-Squared ($\chi^2$) minimization** to fit theoretical microlensing models to observational data.
* **Parameter Extraction:** automatic estimation of key event parameters:
    * $t_0$ (Time of maximum magnification)
    * $t_E$ (Einstein crossing time)
    * $u_{min}$ (Impact parameter)
* **Error Analysis:** (In Progress) Robust error estimation using **Bootstrap resampling** methods to generate confidence intervals for fitted parameters.

## 🛠️ Tech Stack
* **Language:** Python
* **Libraries:**
    * `NumPy` & `Pandas`: Vectorized data manipulation and time-series handling.
    * `SciPy`: Optimization and statistical functions (`scipy.optimize.curve_fit`, `scipy.stats`).
    * `Matplotlib`& `Seaborn`: Visualization of light curves and residual plots.

## 📂 Project Structure
```text
├── data/               # Sample OGLE light curve datasets
├── src/
│   ├── preprocessing.py # Functions for flux conversion and data cleaning
│   ├── fitting.py       # Chi-Squared minimization and model logic
│   └── statistics.py    # Bootstrap and error analysis modules
├── notebooks/          # Jupyter notebooks for exploratory data analysis (EDA)
└── README.md
