#imports
from astropy.io import fits
import numpy as np
import matplotlib.pyplot as plt
import os

#choose data set to use
focus = "cenA"

# Make images folder
os.makedirs(f"images/{focus}", exist_ok=True)

#photon files
files = [
    f"data/{focus}/PH00.fits",
    f"data/{focus}/PH01.fits",
    f"data/{focus}/PH02.fits"
]

#setup
energies = []
ras = []
decs = []
times = []

for f in files:
    hdul = fits.open(f)
    data = hdul[1].data

    energies.extend(data["ENERGY"])
    ras.extend(data["RA"])
    decs.extend(data["DEC"])
    times.extend(data["TIME"])

energies = np.array(energies)
times = np.array(times)
ras = np.array(ras)
decs = np.array(decs)


##### PLOTS ####

# energy spectrum plot
plt.hist(energies, bins=100, log=True)
plt.xlabel("Energy (MeV)")
plt.ylabel("Photon counts")
plt.title("Fermi-LAT Energy Spectrum")
plt.savefig(f"images/{focus}/energy_spectrum.png", dpi=300)
plt.show()

# sky map
plt.scatter(ras, decs, s=1)
plt.xlabel("Right Ascension")
plt.ylabel("Declination")
plt.title("Gamma-ray Photon Sky Map")
plt.savefig(f"images/{focus}/GR_photon_map.png", dpi=300)
plt.show()

#light-time curve
times_days = (times - times.min()) / 86400
bins = 50
counts, edges = np.histogram(times_days, bins=bins)

centers = (edges[:-1] + edges[1:]) / 2

plt.figure(figsize=(8,5))
plt.plot(centers, counts, marker="o")

plt.xlabel("Time (days since start of observation)")
plt.ylabel("Photon counts")
plt.title("Fermi-LAT Light Curve")
plt.savefig(f"images/{focus}/LT_curve.png", dpi=300)
plt.show()

#heatmap gamma rays
plt.figure(figsize=(8,6))
counts, xedges, yedges, img = plt.hist2d(
    ras,
    decs,
    bins=200
)

plt.colorbar(label="Photon Counts")
plt.xlabel("Right Ascension (deg)")
plt.ylabel("Declination (deg)")
plt.title(f"Fermi-LAT Gamma-ray Intensity Map: {focus}")
plt.savefig(f"images/{focus}/GR_intensity_map.png", dpi=300)
plt.show()

# filter for zoom region
mask = (decs >= 20) & (decs <= 24) & (ras >= 81) & (ras <= 85)
ras_zoom = ras[mask]
decs_zoom = decs[mask]

plt.figure(figsize=(8,6))

# 2D histogram = zoomed heat map
counts, xedges, yedges, img = plt.hist2d(
    ras_zoom,
    decs_zoom,
    bins=200
)
plt.colorbar(label="Photon Counts")
plt.xlabel("Right Ascension (deg)")
plt.ylabel("Declination (deg)")
plt.title(f"Zoomed Fermi-LAT Gamma-ray Intensity Map: {focus}")

# save figure
plt.savefig(f"images/{focus}/zoom_heatmap.png", dpi=300)

plt.show()

print("hello world")