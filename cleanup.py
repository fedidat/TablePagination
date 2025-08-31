import os

to_keep = [
    "english_latin_rivalry_1887_2012",
    "australia_demographics_1900_2010",
    "elements",
    "rock_band_downloadable_2011",
    "living_proof_the_farewell_tour",
    "portuguese_grape_varieties",
    "republican_straw_polls_2012",
    "miss_new_york_usa_delegates_2012",
    "cross_country_junior_women_1996",
    "tour_de_france_2009",
    "anaheim_ducks_draft_picks_1998_2013",
    "belgium_demographics_1900_2011",
    "men_butterfly_100m_2009",
]


# Folder to clean
folder = "processing/2_fetched_pages/20250831_111058"

folder_path = os.path.join(os.path.dirname(__file__), folder)

for filename in os.listdir(folder_path):
    file_path = os.path.join(folder_path, filename)
    if os.path.isfile(file_path):
        if not any(s in filename for s in to_keep):
            print(f"Removing {filename}")
            os.remove(file_path)
