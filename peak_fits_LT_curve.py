from astropy.io import fits
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.signal import find_peaks
import os

#choose data set to focus on
focus = "crab"

# Make images folder
os.makedirs(f"images/{focus}", exist_ok=True)

# Photon files
files = [f"data/{focus}/PH00.fits",
         f"data/{focus}/PH01.fits",
         f"data/{focus}/PH02.fits"
]

# Load data
energies, ras, decs, times = [], [], [], []
for f in files:
    hdul = fits.open(f)
    data = hdul[1].data
    energies.extend(data["ENERGY"])
    ras.extend(data["RA"])
    decs.extend(data["DEC"])
    times.extend(data["TIME"])
energies = np.array(energies)
ras = np.array(ras)
decs = np.array(decs)
times = np.array(times)

# Bin light curve
times_days = (times - times.min()) / 86400
bins = 50
counts, edges = np.histogram(times_days, bins=bins)
centers = (edges[:-1] + edges[1:]) / 2

plt.figure(figsize=(10,6))
plt.plot(centers, counts, marker='o', label="Light Curve")

# Gaussian function
def gaussian(x, A, t0, sigma):
    return A * np.exp(-0.5*((x-t0)/sigma)**2)

# Detect peaks (force 6 peaks)
peak_indices, _ = find_peaks(counts, height=np.mean(counts), distance=5)
if len(peak_indices) > 6:
    peak_indices = peak_indices[:6]  # keep first 6 largest peaks

sigma_list = []
t0_list = []

# Fit a Gaussian locally around each peak
window = 5  # number of bins on each side of peak to fit
for idx in peak_indices:
    # select local region
    left = max(idx-window,0)
    right = min(idx+window,len(counts)-1)
    x_fit = centers[left:right+1]
    y_fit = counts[left:right+1]

    p0 = [counts[idx], centers[idx], 0.1]  # initial guess
    try:
        popt, _ = curve_fit(gaussian, x_fit, y_fit, p0=p0)
        A_fit, t0_fit, sigma_fit = popt
        sigma_list.append(sigma_fit)
        t0_list.append(t0_fit)
        plt.plot(x_fit, gaussian(x_fit, *popt), '--', label=f'peak t0={t0_fit:.2f}d')
    except RuntimeError:
        print(f"Failed to fit peak at index {idx}")

# Compute time differences between consecutive Gaussian centers
t0_list = np.array(t0_list)
periods = np.diff(np.sort(t0_list))


plt.xlabel("Time (days since start)")
plt.ylabel("Photon counts")
plt.title("Fermi-LAT Light Curve with Peaks")
plt.legend()
plt.savefig(f"images/{focus}/light_curve_peaks.png", dpi=300)
plt.show()

with open(f"peaks_output_{focus}.txt", "w") as f:
    f.write(f"peaks located at (days): {t0_list}\n")
    f.write(f"time between each peak (days): {periods}\n")
    f.write(f"average time between peaks (days): {np.mean(periods)}\n")
    f.write("from a quick google search: 53.4 days is the precession period of the spacecraft. this matches the average period time well.\n")