# Supplement Knowledge Base — v0.2-expanded (Group 101)

## Overview & Canonical Architecture
The `dataset/` directory contains the authoritative knowledge base builder and definitions for the **Open Source Supplement Recommendation Platform**.

- Canonical Data Definitions: `dataset/supplement_data.py`
- Canonical Dataset Output: `dataset/data/` (19 CSV files)
- Reproducible Dataset Builder: `dataset/build.py`
- Dataset Validator: `dataset/validate_dataset.py`
- Database Schema DDL: `dataset/schema.sql`

## Dataset Expansion Summary
The catalogue has been expanded from the baseline 24 records to **130 distinct generic supplement records** across 11 balanced categories:

1. **Vitamins & Complexes (17):** Vitamin D, Vitamin B12, B6, C, E, K, A, Folate, Biotin, B1, B2, B3, B5, B-Complex, Vitamin K2 (MK-7), Beta-Carotene, Inositol.
2. **Minerals & Trace Elements (15):** Calcium, Iron, Magnesium, Zinc, Selenium, Iodine, Potassium, Copper, Manganese, Chromium, Molybdenum, Boron, Silicon, Vanadium, Multi-Mineral Complex.
3. **Omega-3 & Fatty Acids (13):** Omega-3 Fatty Acids, EPA, DHA, Algal Oil, Cod Liver Oil, Krill Oil, Flaxseed Oil, Evening Primrose Oil, Borage Oil, Black Currant Seed Oil, CLA, ALA, MCT Oil.
4. **Protein Supplements (9):** Whey Protein Isolate, Whey Protein Concentrate, Micellar Casein, Pea Protein, Soy Protein Isolate, Rice Protein, Hemp Protein, Egg White Protein, Collagen Peptides.
5. **Amino Acids & Derivatives (14):** Creatine, L-Glutamine, BCAA, EAA, L-Arginine, L-Citrulline, Beta-Alanine, L-Carnitine, Taurine, L-Tyrosine, L-Theanine, Glycine, N-Acetyl Cysteine (NAC), L-Lysine.
6. **Electrolytes & Hydration (5):** Electrolyte Replacement Complex, Sodium Chloride, Potassium Citrate, Magnesium Malate, Oral Rehydration Salts (ORS).
7. **Fiber & Prebiotics (8):** Psyllium Husk, Inulin / FOS, Acacia Fiber, Glucomannan, Partially Hydrolyzed Guar Gum (PHGG), Apple Pectin, Arabinogalactan, Resistant Starch.
8. **Probiotics (6):** Probiotics (Multi-strain), Saccharomyces boulardii, Lactobacillus rhamnosus GG, Bifidobacterium infantis, Bacillus coagulans, Synbiotic Complex.
9. **Herbal & Botanicals (29):** Ashwagandha, Turmeric / Curcumin, Ginkgo, Echinacea, Garlic Extract, Panax Ginseng, Rhodiola Rosea, Milk Thistle (Silymarin), Valerian Root, St. John's Wort, Green Tea Extract (EGCG), Ginger Root, Boswellia Serrata, Elderberry, Saw Palmetto, Fenugreek, Berberine, Maca Root, Holy Basil (Tulsi), Bacopa Monnieri, Cordyceps Mushroom, Lion's Mane Mushroom, Reishi Mushroom, Bilberry Extract, Cranberry Extract, Hawthorn Berry, Passionflower, Tart Cherry Extract, Red Yeast Rice.
10. **Nutrients & Cellular Factors (13):** Choline, Coenzyme Q10 (CoQ10), Alpha-Lipoic Acid, Resveratrol, Astaxanthin, Lutein & Zeaxanthin, Quercetin, Spirulina, Chlorella, Glucosamine Sulfate, Chondroitin Sulfate, Methylsulfonylmethane (MSM), SAMe.
11. **Hormone Supplements (1):** Melatonin.

Total: **130 distinct supplement records**.

## Data Roles: Draft vs. Verified
- **`dataset/data/` (Canonical Draft):** Contains all 130 supplements in draft status (`verification_status="needs_review"`), where candidate mappings are inactive. Demonstrates the strict behavior of Rule R000: unverified datasets result in zero eligible recommendations.
- **`backend/data/`:** Exact replica of `dataset/data/` for test isolation.
- **`backend/data_verified/`:** Contains 46 fully verified monographs, 42 activated goal mappings, and 41 verified safety rules. Unverified candidate items remain `needs_review` so they route to review and never enter recommendations.

## Build & Validation Commands (PowerShell)
```powershell
# Reproduce dataset CSVs and synchronize across targets
python dataset\build.py

# Validate dataset integrity
python dataset\validate_dataset.py dataset\data

# Validate active verified dataset with cross-directory synchronization check
python dataset\validate_dataset.py backend\data_verified --compare-with dataset\data
```
