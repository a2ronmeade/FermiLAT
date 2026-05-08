#Set the focus to the name of wherever your data files are saved (inside a folder called data).
#Plots will automatically be saved to a folder under the same name located in "images".
focus = "crab-6m"

#-------------------------------------------------------------#
#                      FermiLAT Query                         #
#-------------------------------------------------------------#

# query_object requires the name of the object, the energy range, and the dates ov observation.
result = FermiLAT.query_object('Crab', energyrange_MeV='100, 300000', obsdates='2019-01-01 00:00:00, 2019-06-01 00:00:00')

os.makedirs(f"data/{focus}", exist_ok=True)
os.makedirs(f"images/{focus}", exist_ok=True)

for url in result:
    raw = url.split("/")[-1]
    filename = raw.split("_", 1)[1]
    print("Downloading:", filename)
    r = requests.get(url, stream=True)
    r.raise_for_status()
    with open(f"data/{focus}/{filename}", "wb") as f:
        for chunk in r.iter_content(chunk_size=8192):
            f.write(chunk)

print("FermiLAT download complete.")

#-------------------------------------------------------------#
#              Gamma-Ray Burst Monitor Query                  #
#-------------------------------------------------------------#
'''
heasarc = Heasarc()

gbm_result = heasarc.query_region(
    "Crab",
    mission="fermigtrig",
    radius="15 deg"
)

for row in gbm_result:
    
    # trigger ID column (may vary slightly depending on catalog version)
    trig_id = row["TRIGGER_ID"]
    
    base_url = f"https://heasarc.gsfc.nasa.gov/FTP/fermi/data/gbm/triggers/{trig_id}/current/"
    
    print("Processing trigger:", trig_id)

    # common GBM files (not all triggers will have all of these)
    files = [
        "glg_tte_b0.fit",
        "glg_cspec_b0.fit"
    ]

    for fname in files:
        url = base_url + fname
        
        try:
            r = requests.get(url, stream=True)
            r.raise_for_status()
            outpath = f"data/{focus}/gbm/{trig_id}_{fname}"
            with open(outpath, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)

            print("Downloaded:", outpath)

        except Exception:
            print("Missing:", url)

print("GBM download complete.")

'''

#-------------------------------------------------------------#
#                          JWST Query                         #
#-------------------------------------------------------------#
'''
target_name = "Crab Nebula"

obs = Observations.query_object(target_name, radius="0.2 deg")
jwst_obs = obs[obs["obs_collection"] == "JWST"]

print(f"Total JWST observations: {len(jwst_obs)}")


products = Observations.get_product_list(jwst_obs)

products = Observations.filter_products(
    products,
    productType="SCIENCE",
    extension="fits"
)
manifest = Observations.download_products(
    products,
    download_dir="data/jwst",
    mrp_only=False
)
print("JWST download complete.")
'''
