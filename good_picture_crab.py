from astropy.io import fits
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter
import os

# ----- Photon files -----
files = [
    "data/crab/PH00.fits",
    "data/crab/PH01.fits",
    "data/crab/PH02.fits"
]

# ----- Setup lists -----
ras = []
decs = []
energies = []

# ----- Load data -----
for f in files:
    hdul = fits.open(f)
    data = hdul[1].data

    ras.extend(data["RA"])
    decs.extend(data["DEC"])
    energies.extend(data["ENERGY"])

ras = np.array(ras)
decs = np.array(decs)
energies = np.array(energies)

# ----- Filter photons -----
# High-energy photons (>1 GeV)
high_energy_mask = energies >= 1000

# Zoom region around Crab Nebula
zoom_mask = (decs >= 21.7) & (decs <= 22.2) & (ras >= 83.3) & (ras <= 83.9)

# Combine filters
mask = high_energy_mask & zoom_mask
ras_zoom = ras[mask]
decs_zoom = decs[mask]

print(f"Number of photons in zoomed high-energy region: {len(ras_zoom)}")

# ----- 2D histogram -----
bins = 200  # high resolution
counts, xedges, yedges = np.histogram2d(ras_zoom, decs_zoom, bins=bins)

# ----- Gaussian smoothing -----
sigma = 2  # controls blur
counts_smooth = gaussian_filter(counts, sigma=sigma)

# ----- Plot -----
plt.figure(figsize=(8,6))
im = plt.imshow(
    counts_smooth.T,              # transpose to match axes
    origin='lower',
    extent=[xedges[0], xedges[-1], yedges[0], yedges[-1]],
    cmap='inferno',               # glowing color map
    aspect='auto'
)
plt.colorbar(im, label="Photon Counts")
plt.xlabel("Right Ascension (deg)")
plt.ylabel("Declination (deg)")
plt.title("Crab Nebula: Smoothed High-Energy Gamma-ray Map")

plt.savefig(os.path.join("images/crab/good_pic.png"), dpi=300, bbox_inches='tight')

plt.show()