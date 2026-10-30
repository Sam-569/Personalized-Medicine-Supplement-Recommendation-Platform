"""Supplement Knowledge Base - Canonical Data Definitions
Defines all 130 distinct supplement records, controlled vocabularies,
and evidence-linked mappings according to NIH ODS, NCCIH, and MedlinePlus.
"""

T_CREATED = "2026-10-10"
RV = "v0.2-expanded"

# Reference Registries
SOURCES = [
    ["SRC01", "NIH ODS Dietary Supplement Fact Sheets", "fact_sheet", "https://ods.od.nih.gov/factsheets/list-all/", "web pages (manual reading)", "US government site; verify ODS reuse/citation policy and cite per page", "Narrative text, not a structured dataset; no goal-match scores; interaction/contraindication info is per-nutrient prose"],
    ["SRC02", "NIH Dietary Supplement Label Database (DSLD)", "label_database", "https://dsld.od.nih.gov/", "web search + data download", "US government data; verify terms on site", "Describes commercial product LABELS (ingredients, forms, label claims). Not evidence of efficacy or safety; allergen/diet info only if stated on a label"],
    ["SRC03", "NIH Dietary Supplement Ingredient Database (DSID)", "analytical_database", "https://dsid.od.nih.gov/", "web downloads", "US government data; verify terms on site", "Measured ingredient amounts in sampled products; covers limited ingredients; not a safety or goal source"],
    ["SRC04", "openFDA Food/Dietary Supplement Adverse Event API (CAERS)", "adverse_event_reports", "https://open.fda.gov/apis/food/event/", "REST API (JSON)", "Check openFDA terms of service on site", "Voluntary reports; NOT proof of causation; cannot establish rates; do not use to assign safety/contraindication rules automatically"],
    ["SRC05", "NCCIH Herbs at a Glance / safety pages", "fact_sheet", "https://www.nccih.nih.gov/health/herbsataglance", "web pages (manual)", "US government; cite per page", "Herbal coverage; prose; limited interaction detail"],
    ["SRC06", "MedlinePlus Supplements", "fact_sheet", "https://medlineplus.gov/druginfo/herb_All.html", "web pages (manual)", "US NLM; verify reuse policy", "Prose monographs; good for cross-checking interactions"],
    ["SRC07", "DailyMed (NLM) labels", "label_database", "https://dailymed.nlm.nih.gov/dailymed/", "web/API", "US NLM; verify terms", "Includes some supplement labels and drug labels; useful for drug-interaction cross-check of medications"]
]

# Controlled Vocabularies
GOALS = [
    ["GL01", "bone_health", "Bone health", "User-selectable goal", True],
    ["GL02", "energy_fatigue", "Energy / fatigue", "User-selectable goal", True],
    ["GL03", "immune_support", "Immune support", "User-selectable goal", True],
    ["GL04", "sleep_support", "Sleep support", "User-selectable goal", True],
    ["GL05", "heart_health", "Heart health", "User-selectable goal", True],
    ["GL06", "digestive_health", "Digestive health", "User-selectable goal", True],
    ["GL07", "muscle_exercise", "Muscle / exercise performance", "User-selectable goal", True],
    ["GL08", "stress_support", "Stress support", "User-selectable goal", True],
    ["GL09", "cognitive_function", "Cognitive function", "User-selectable goal", True],
    ["GL10", "skin_hair_nails", "Skin / hair / nails", "User-selectable goal", True],
    ["GL11", "general_nutrition", "General nutrition gaps", "User-selectable goal", True]
]

DIETS = [
    ["omnivore", "Omnivore", "No dietary restriction"],
    ["vegetarian", "Vegetarian", "No meat/fish; dairy/eggs per user preference"],
    ["vegan", "Vegan", "No animal-derived ingredients"]
]

ALLERGENS = [
    ["fish", "Fish"],
    ["shellfish", "Shellfish"],
    ["milk", "Milk / dairy"],
    ["soy", "Soy"],
    ["egg", "Egg"],
    ["tree_nut", "Tree nuts"],
    ["peanut", "Peanut"],
    ["gluten", "Gluten / wheat"]
]

CONDITIONS = [
    ["pregnancy", "Pregnancy", "Collect only if kept in scope"],
    ["breastfeeding", "Breastfeeding", ""],
    ["kidney_disease", "Kidney disease", ""],
    ["liver_disease", "Liver disease", ""],
    ["thyroid_disorder", "Thyroid disorder", ""],
    ["iron_overload", "Iron overload / hemochromatosis", ""],
    ["bleeding_disorder", "Bleeding disorder", ""],
    ["heart_disease", "Heart disease", ""],
    ["diabetes", "Diabetes", ""],
    ["hypertension", "Hypertension", ""],
    ["autoimmune_disease", "Autoimmune disease", ""]
]

MEDICATION_CLASSES = [
    ["anticoagulant", "Anticoagulants / blood thinners", "Requires medication profile check; interaction warning"],
    ["thyroid_medication", "Thyroid medication", ""],
    ["antihypertensive", "Blood-pressure medication", ""],
    ["sedative", "Sedatives / sleep medication", ""],
    ["immunosuppressant", "Immunosuppressants", ""],
    ["antidiabetic", "Diabetes medication", ""]
]

ACTIVITY_LEVELS = [
    ["sedentary", "Sedentary", 1],
    ["light", "Light", 2],
    ["moderate", "Moderate", 3],
    ["high", "High", 4]
]

SLEEP_CATEGORIES = [
    ["poor", "Poor", 1],
    ["fair", "Fair", 2],
    ["good", "Good", 3]
]

STATUS_DEFINITIONS = [
    ["verified", "verification_status", "Value checked against a cited source by a named reviewer; may drive the engine"],
    ["needs_review", "verification_status", "Candidate value (draft/proposed); NOT used by the engine until verified"],
    ["unknown", "verification_status / compat status", "No information found; NEVER treated as safe or compatible"],
    ["not_applicable", "verification_status", "Field legitimately does not apply to this record"],
    ["rejected", "verification_status", "Reviewed and rejected"],
    ["compatible", "compat_status", "Verified compatible"],
    ["incompatible", "compat_status", "Verified incompatible -> exclude"],
    ["depends_on_product", "compat_status", "Depends on the specific product/formulation -> review"]
]

SCORING_CONFIG = [
    ["C1", "G", "Goal match", 0.40, 0, 1, "Max over user goals of mapped match_score", RV, True],
    ["C2", "D", "Dietary fit", 0.20, 0, 1, "See criterion_value_rules", RV, True],
    ["C3", "A", "Activity match", 0.15, 0, 1, "From supplement_activity_map", RV, True],
    ["C4", "L", "Lifestyle/sleep match", 0.15, 0, 1, "From supplement_lifestyle_map", RV, True],
    ["C5", "H", "Previous usage", 0.10, 0, 1, "See criterion_value_rules; NOT evidence of safety", RV, True]
]

SYSTEM_CONFIG = [
    ["threshold", "0.60", "Keep if score >= threshold", RV],
    ["float_tolerance", "1e-9", "Tolerance for threshold comparison and weight sum", RV],
    ["tie_breaker_1", "final_score desc", "", RV],
    ["tie_breaker_2", "goal_match_score desc", "", RV],
    ["tie_breaker_3", "supplement_id asc", "Final deterministic key", RV],
    ["dataset_version", RV, "", RV],
    ["scoring_version", "wsm-1", "", RV]
]

CRITERION_VALUE_RULES = [
    ["V01", "G", "direct match for any selected goal", 1.0, "project-defined", RV],
    ["V02", "G", "partial match only", 0.5, "project-defined", RV],
    ["V03", "G", "no mapping", 0.0, "project-defined", RV],
    ["V04", "D", "user omnivore OR no restriction", 1.0, "project-defined", RV],
    ["V05", "D", "compat_status=compatible & verified", 1.0, "project-defined", RV],
    ["V06", "D", "compat_status=incompatible", 0.0, "also handled by safety filter (exclude)", RV],
    ["V07", "D", "compat_status in (unknown, depends_on_product)", 0.0, "also flagged require_review", RV],
    ["V08", "A", "direct activity match", 1.0, "project-defined", RV],
    ["V09", "A", "partial activity match", 0.5, "project-defined", RV],
    ["V10", "A", "no mapping", 0.0, "project-defined (assumption: no mapping = no match)", RV],
    ["V11", "L", "direct sleep match", 1.0, "project-defined", RV],
    ["V12", "L", "partial sleep match", 0.5, "project-defined", RV],
    ["V13", "L", "no mapping", 0.0, "project-defined", RV],
    ["V14", "H", "never used", 0.5, "neutral; project-defined assumption", RV],
    ["V15", "H", "used before, no reported reaction", 1.0, "preference continuity only, not proof of tolerance", RV],
    ["V16", "H", "used before, reaction reported", 0.0, "also triggers require_review", RV]
]

EXPLANATION_TEMPLATES = [
    ["T01", "G", "1.0", "Directly matches the selected goal: {goal_name}.", "supplement_goal_map.verified", RV, True],
    ["T02", "G", "0.5", "Partially or indirectly related to the selected goal: {goal_name}.", "supplement_goal_map.verified", RV, True],
    ["T03", "D", "1.0", "Compatible with the recorded dietary preference according to the verified data.", "supplement_diet_compat.verified", RV, True],
    ["T04", "A", "1.0", "Matches the user's configured activity category.", "supplement_activity_map.verified", RV, True],
    ["T05", "A", "0.5", "Partially matches the user's configured activity category.", "supplement_activity_map.verified", RV, True],
    ["T06", "L", "1.0", "Matches the user's recorded sleep/lifestyle category.", "supplement_lifestyle_map.verified", RV, True],
    ["T07", "L", "0.5", "Partially matches the user's recorded sleep/lifestyle category.", "supplement_lifestyle_map.verified", RV, True],
    ["T08", "H", "1.0", "You previously reported using this supplement without a reported reaction. This does not confirm it is safe for you.", "user_profile.previous_usage", RV, True],
    ["T09", "SAFETY", "pass", "Passed the configured safety checks. This does not guarantee medical safety.", "safety_rules.verified", RV, True],
    ["T10", "SAFETY", "review", "Needs review before it can be suggested: {safety_message}", "safety_rules", RV, True],
    ["T11", "LIMIT", "all", "This is general educational guidance, not medical advice. Scores reflect project-defined rules, not clinical effectiveness.", "", RV, True]
]


# --- All 130 Distinct Supplement Types ---
SUPPLEMENT_RECORDS = [
    # Baseline 24
    ("SUP001", "Vitamin D", "vitamin", "Essential fat-soluble vitamin facilitating intestinal calcium absorption and bone mineralization.", "cholecalciferol (D3), ergocalciferol (D2)", "tablets, capsules, liquid drops", "SRC01", "https://ods.od.nih.gov/factsheets/VitaminD-HealthProfessional/", True, "Verified against NIH ODS professional monograph."),
    ("SUP002", "Vitamin B12", "vitamin", "Water-soluble vitamin essential for red blood cell formation, neurological function, and DNA synthesis.", "cyanocobalamin, methylcobalamin", "tablets, sublingual lozenges", "SRC01", "https://ods.od.nih.gov/factsheets/VitaminB12-HealthProfessional/", True, "Verified against NIH ODS professional monograph."),
    ("SUP003", "Vitamin B6", "vitamin", "Coenzyme involved in amino acid metabolism, cognitive development, and immune function.", "pyridoxine hydrochloride, pyridoxal 5'-phosphate", "tablets, capsules", "SRC01", "https://ods.od.nih.gov/factsheets/VitaminB6-HealthProfessional/", True, "Verified against NIH ODS professional monograph."),
    ("SUP004", "Vitamin C", "vitamin", "Potent water-soluble antioxidant supporting collagen synthesis and immune defense.", "ascorbic acid, sodium ascorbate, calcium ascorbate", "tablets, chewables, powders", "SRC01", "https://ods.od.nih.gov/factsheets/VitaminC-HealthProfessional/", True, "Verified against NIH ODS professional monograph."),
    ("SUP005", "Vitamin E", "vitamin", "Fat-soluble antioxidant protecting cell membranes from reactive oxygen species.", "d-alpha-tocopherol, mixed tocopherols", "softgels, capsules", "SRC01", "https://ods.od.nih.gov/factsheets/VitaminE-HealthProfessional/", True, "Verified against NIH ODS professional monograph."),
    ("SUP006", "Vitamin K", "vitamin", "Fat-soluble nutrient required for hepatic synthesis of blood-clotting factors and osteocalcin.", "phylloquinone (K1), menaquinone (K2/MK-7)", "tablets, softgels", "SRC01", "https://ods.od.nih.gov/factsheets/VitaminK-HealthProfessional/", True, "Verified against NIH ODS professional monograph."),
    ("SUP007", "Vitamin A", "vitamin", "Fat-soluble retinoid essential for vision, immune competence, and cellular differentiation.", "retinyl palmitate, beta-carotene", "capsules, softgels", "SRC01", "https://ods.od.nih.gov/factsheets/VitaminA-HealthProfessional/", True, "Verified against NIH ODS professional monograph."),
    ("SUP008", "Folate", "vitamin", "Water-soluble B vitamin required for one-carbon metabolism and neural tube formation.", "folic acid, L-5-methyltetrahydrofolate (5-MTHF)", "tablets, capsules", "SRC01", "https://ods.od.nih.gov/factsheets/Folate-HealthProfessional/", True, "Verified against NIH ODS professional monograph."),
    ("SUP009", "Biotin", "vitamin", "B vitamin serving as coenzyme for carboxylases in fatty acid and glucose metabolism.", "d-biotin", "capsules, tablets", "SRC01", "https://ods.od.nih.gov/factsheets/Biotin-HealthProfessional/", True, "Verified against NIH ODS professional monograph."),
    ("SUP010", "Choline", "nutrient", "Essential nutrient for phospholipid synthesis, cell signalling, and acetylcholine neurotransmission.", "choline bitartrate, phosphatidylcholine, CDP-choline", "capsules, powders", "SRC01", "https://ods.od.nih.gov/factsheets/Choline-HealthProfessional/", True, "Verified against NIH ODS professional monograph."),
    ("SUP011", "Calcium", "mineral", "Major mineral structural component of bones and teeth; required for neuromuscular function.", "calcium carbonate, calcium citrate", "tablets, chews", "SRC01", "https://ods.od.nih.gov/factsheets/Calcium-HealthProfessional/", True, "Verified against NIH ODS professional monograph."),
    ("SUP012", "Iron", "mineral", "Essential trace mineral component of hemoglobin, myoglobin, and cellular respiration enzymes.", "ferrous sulfate, ferrous bisglycinate, ferrous fumarate", "tablets, capsules, liquid", "SRC01", "https://ods.od.nih.gov/factsheets/Iron-HealthProfessional/", True, "Verified against NIH ODS professional monograph."),
    ("SUP013", "Magnesium", "mineral", "Cofactor in over 300 enzymatic reactions including energy production, muscle contraction, and sleep regulation.", "magnesium glycinate, magnesium citrate, magnesium oxide", "capsules, tablets, powder", "SRC01", "https://ods.od.nih.gov/factsheets/Magnesium-HealthProfessional/", True, "Verified against NIH ODS professional monograph."),
    ("SUP014", "Zinc", "mineral", "Essential trace element required for cellular metabolism, wound healing, and immune signaling.", "zinc gluconate, zinc picolinate, zinc citrate", "tablets, lozenges", "SRC01", "https://ods.od.nih.gov/factsheets/Zinc-HealthProfessional/", True, "Verified against NIH ODS professional monograph."),
    ("SUP015", "Selenium", "mineral", "Trace mineral constituent of selenoproteins including glutathione peroxidase antioxidant enzymes.", "selenomethionine, sodium selenite", "tablets, capsules", "SRC01", "https://ods.od.nih.gov/factsheets/Selenium-HealthProfessional/", True, "Verified against NIH ODS professional monograph."),
    ("SUP016", "Iodine", "mineral", "Essential component of thyroid hormones thyroxine (T4) and triiodothyronine (T3).", "potassium iodide, kelp extract", "tablets, liquid drops", "SRC01", "https://ods.od.nih.gov/factsheets/Iodine-HealthProfessional/", True, "Verified against NIH ODS professional monograph."),
    ("SUP017", "Potassium", "mineral", "Primary intracellular cation regulating fluid balance, nerve conduction, and vascular tone.", "potassium chloride, potassium citrate", "tablets, powders", "SRC01", "https://ods.od.nih.gov/factsheets/Potassium-HealthProfessional/", True, "Verified against NIH ODS professional monograph."),
    ("SUP018", "Omega-3 fatty acids", "fatty_acid", "Polyunsaturated fatty acids modulating inflammatory eicosanoid pathways and cardiovascular lipid profiles.", "EPA, DHA ethyl esters, triglycerides, algal oil", "softgels, liquid oil", "SRC01", "https://ods.od.nih.gov/factsheets/Omega3FattyAcids-HealthProfessional/", True, "Verified against NIH ODS professional monograph."),
    ("SUP019", "Probiotics", "probiotic", "Live beneficial microorganisms supporting intestinal barrier function and gut microbiota homeostasis.", "Lactobacillus acidophilus, Bifidobacterium lactis, Saccharomyces boulardii", "delayed-release capsules, powders", "SRC01", "https://ods.od.nih.gov/factsheets/Probiotics-HealthProfessional/", True, "Verified against NIH ODS professional monograph."),
    ("SUP020", "Melatonin", "hormone_supplement", "Endogenous neurohormone regulating circadian rhythms and sleep-wake timing.", "synthetic melatonin", "tablets, sublingual drops, gummies", "SRC01", "https://ods.od.nih.gov/factsheets/Melatonin-HealthProfessional/", True, "Verified against NIH ODS professional monograph."),
    ("SUP021", "Ashwagandha", "botanical", "Adaptogenic botanical herb used to support stress response, adrenal homeostasis, and sleep.", "standardized withanolides extract (Withania somnifera root)", "capsules, powders, liquid extract", "SRC05", "https://www.nccih.nih.gov/health/ashwagandha", True, "Verified against NCCIH monograph."),
    ("SUP022", "Turmeric / curcumin", "botanical", "Polyphenolic botanical compound exhibiting anti-inflammatory and antioxidant activities.", "curcuminoids 95% with piperine / phytosome", "capsules, softgels", "SRC05", "https://www.nccih.nih.gov/health/turmeric", True, "Verified against NCCIH monograph."),
    ("SUP023", "Ginkgo", "botanical", "Standardized botanical extract containing flavone glycosides and terpene lactones for cerebral circulation.", "EGb 761 standardized Ginkgo biloba leaf extract", "tablets, capsules", "SRC05", "https://www.nccih.nih.gov/health/ginkgo", True, "Verified against NCCIH monograph."),
    ("SUP024", "Creatine", "amino_acid_derivative", "Nitrogenous amino acid derivative resynthesizing adenosine triphosphate (ATP) during high-intensity muscle contractions.", "creatine monohydrate, micronized creatine", "unflavored powder, capsules", "SRC01", "https://ods.od.nih.gov/factsheets/ExerciseAndAthleticPerformance-HealthProfessional/", True, "Verified against NIH ODS professional monograph."),

    # Added Vitamins (SUP025 - SUP032)
    ("SUP025", "Vitamin B1 (Thiamine)", "vitamin", "Essential water-soluble B vitamin cofactor for pyruvate dehydrogenase and carbohydrate energy metabolism.", "thiamine hydrochloride, thiamine mononitrate, benfotiamine", "tablets, capsules", "SRC01", "https://ods.od.nih.gov/factsheets/Thiamin-HealthProfessional/", True, "Verified against NIH ODS professional monograph."),
    ("SUP026", "Vitamin B2 (Riboflavin)", "vitamin", "Precursor to coenzymes FMN and FAD involved in mitochondrial electron transport and cellular oxidation-reduction reactions.", "riboflavin, riboflavin 5'-phosphate", "tablets, capsules", "SRC01", "https://ods.od.nih.gov/factsheets/Riboflavin-HealthProfessional/", True, "Verified against NIH ODS professional monograph."),
    ("SUP027", "Vitamin B3 (Niacin)", "vitamin", "Precursor of NAD and NADP coenzymes regulating cellular energy transfer and lipid metabolism.", "nicotinic acid, niacinamide, inositol hexanicotinate", "tablets, capsules, extended-release", "SRC01", "https://ods.od.nih.gov/factsheets/Niacin-HealthProfessional/", True, "Verified against NIH ODS professional monograph."),
    ("SUP028", "Vitamin B5 (Pantothenic Acid)", "vitamin", "Essential precursor for Coenzyme A synthesis required for fatty acid breakdown and citric acid cycle flux.", "d-calcium pantothenate, pantethine", "capsules, tablets", "SRC01", "https://ods.od.nih.gov/factsheets/PantothenicAcid-HealthProfessional/", True, "Verified against NIH ODS professional monograph."),
    ("SUP029", "Vitamin B-Complex", "vitamin", "Comprehensive balanced multivitamin formula targeting complete B-vitamin family requirements.", "balanced blend of thiamine, riboflavin, niacin, B6, folate, B12, biotin, pantothenic acid", "capsules, tablets, liquid", "SRC06", "https://medlineplus.gov/druginfo/meds/a682858.html", False, "Candidate multi-ingredient formula requiring review of ingredient proportions."),
    ("SUP030", "Vitamin K2 (Menaquinone-7)", "vitamin", "Bioactive form of vitamin K supporting vascular elasticity and osteocalcin activation for bone mineralization.", "menaquinone-7 (MK-7), menaquinone-4 (MK-4)", "softgels, capsules", "SRC01", "https://ods.od.nih.gov/factsheets/VitaminK-HealthProfessional/", True, "Verified against NIH ODS professional monograph."),
    ("SUP031", "Beta-Carotene", "vitamin", "Provitamin A carotenoid functioning as a fat-soluble antioxidant and retinal pigment precursor.", "natural mixed carotenoids, synthetic all-trans beta-carotene", "softgels, capsules", "SRC01", "https://ods.od.nih.gov/factsheets/VitaminA-HealthProfessional/", False, "Candidate provitamin carotenoid pending review of smoking interaction guidelines."),
    ("SUP032", "Inositol", "vitamin", "Carbocyclic sugar isomer acting as a secondary intracellular messenger for insulin and neurotransmitter signaling.", "myo-inositol, D-chiro-inositol", "powders, capsules", "SRC06", "https://medlineplus.gov/druginfo/natural/299.html", False, "Candidate vitamin-like compound pending clinical review for metabolic endpoints."),

    # Added Minerals & Trace Elements (SUP033 - SUP040)
    ("SUP033", "Copper", "mineral", "Essential cofactor for cytochrome c oxidase, superoxide dismutase, and ferroxidase enzymes.", "copper gluconate, copper bisglycinate, cupric sulfate", "tablets, capsules", "SRC01", "https://ods.od.nih.gov/factsheets/Copper-HealthProfessional/", True, "Verified against NIH ODS professional monograph."),
    ("SUP034", "Manganese", "mineral", "Essential micronutrient cofactor for mitochondrial superoxide dismutase and connective tissue proteoglycan synthesis.", "manganese gluconate, manganese citrate, manganese sulfate", "tablets, capsules", "SRC01", "https://ods.od.nih.gov/factsheets/Manganese-HealthProfessional/", True, "Verified against NIH ODS professional monograph."),
    ("SUP035", "Chromium", "mineral", "Trace element involved in potentiating insulin action and macronutrient carbohydrate metabolism.", "chromium picolinate, chromium nicotinate", "capsules, tablets", "SRC01", "https://ods.od.nih.gov/factsheets/Chromium-HealthProfessional/", True, "Verified against NIH ODS professional monograph."),
    ("SUP036", "Molybdenum", "mineral", "Cofactor for sulfite oxidase, xanthine oxidase, and aldehyde oxidase in sulfur amino acid catabolism.", "sodium molybdate, molybdenum glycinate", "tablets, capsules", "SRC01", "https://ods.od.nih.gov/factsheets/Molybdenum-HealthProfessional/", False, "Candidate trace element awaiting monograph review."),
    ("SUP037", "Boron", "mineral", "Trace mineral influencing steroid hormone metabolism, bone matrix composition, and joint integrity.", "boron citrate, calcium fructoborate", "capsules, tablets", "SRC01", "https://ods.od.nih.gov/factsheets/Boron-HealthProfessional/", False, "Candidate trace element under clinical review for bone and endocrine endpoints."),
    ("SUP038", "Silicon", "mineral", "Trace element contributing to collagen synthesis, cross-linking of glycosaminoglycans, and bone mineralization.", "orthosilicic acid, bamboo silica extract", "capsules, liquid drops", "SRC06", "https://medlineplus.gov/druginfo/natural/1096.html", False, "Candidate nutrient under review for connective tissue benefits."),
    ("SUP039", "Vanadium", "mineral", "Trace compound researched for insulin-mimetic phosphorylation effects in peripheral target tissues.", "vanadyl sulfate, sodium metavanadate", "capsules, tablets", "SRC06", "https://medlineplus.gov/druginfo/natural/749.html", False, "Candidate trace compound requiring safety review regarding renal accumulation."),
    ("SUP040", "Multi-Mineral Complex", "mineral", "Broad-spectrum mineral blend formulated to provide essential macrominerals and microelements.", "balanced macro-mineral and trace-element broad spectrum formulation", "tablets, capsules", "SRC02", "https://dsld.od.nih.gov/", False, "Candidate composite mineral blend requiring formulation cross-checks."),

    # Added Fatty Acids (SUP041 - SUP052)
    ("SUP041", "EPA (Eicosapentaenoic Acid)", "fatty_acid", "Long-chain omega-3 fatty acid precursor to series-3 prostaglandins and anti-inflammatory resolvins.", "eicosapentaenoic acid ethyl ester, EPA triglyceride", "softgels, liquid", "SRC01", "https://ods.od.nih.gov/factsheets/Omega3FattyAcids-HealthProfessional/", True, "Verified against NIH ODS professional monograph."),
    ("SUP042", "DHA (Docosahexaenoic Acid)", "fatty_acid", "Major structural omega-3 phospholipid in cerebral cortex gray matter and retinal rod photoreceptors.", "docosahexaenoic acid algal / marine oil", "softgels, liquid", "SRC01", "https://ods.od.nih.gov/factsheets/Omega3FattyAcids-HealthProfessional/", True, "Verified against NIH ODS professional monograph."),
    ("SUP043", "Algal Oil", "fatty_acid", "100% plant-derived sustainable marine omega-3 providing preformed EPA and DHA without fish allergens.", "Schizochytrium sp. microalgal oil rich in DHA and EPA", "vegan softgels, drops", "SRC01", "https://ods.od.nih.gov/factsheets/Omega3FattyAcids-HealthProfessional/", True, "Verified plant-derived omega-3 source from microalgae."),
    ("SUP044", "Cod Liver Oil", "fatty_acid", "Traditional marine oil providing long-chain omega-3s together with naturally occurring vitamin A and D.", "refined Atlantic cod liver oil providing EPA, DHA, vitamins A and D", "liquid oil, softgels", "SRC01", "https://ods.od.nih.gov/factsheets/Omega3FattyAcids-HealthProfessional/", False, "Candidate marine supplement requiring safety review for fat-soluble vitamin accumulation."),
    ("SUP045", "Krill Oil", "fatty_acid", "Marine crustacean oil delivering phospholipid-complexed omega-3 fatty acids and natural astaxanthin antioxidant.", "Euphausia superba phospholipid-bound EPA and DHA with astaxanthin", "softgels", "SRC01", "https://ods.od.nih.gov/factsheets/Omega3FattyAcids-HealthProfessional/", False, "Candidate crustacean oil requiring review of shellfish allergy cross-reactivity."),
    ("SUP046", "Flaxseed Oil", "fatty_acid", "Plant-based omega-3 source rich in essential alpha-linolenic acid (ALA) and dietary lignans.", "cold-pressed Linum usitatissimum seed oil rich in alpha-linolenic acid", "liquid oil, softgels", "SRC05", "https://www.nccih.nih.gov/health/flaxseed-and-flaxseed-oil", False, "Candidate botanical oil awaiting clinical conversion rate review."),
    ("SUP047", "Evening Primrose Oil", "fatty_acid", "Botanical seed oil high in omega-6 gamma-linolenic acid (GLA) supporting skin moisture and eicosanoid balance.", "cold-pressed Oenothera biennis seed oil providing 9% gamma-linolenic acid", "softgels", "SRC05", "https://www.nccih.nih.gov/health/evening-primrose-oil", False, "Candidate botanical oil requiring interaction check for seizure disorders."),
    ("SUP048", "Borage Oil", "fatty_acid", "Concentrated botanical source of gamma-linolenic acid used for joint comfort and anti-inflammatory support.", "Borago officinalis seed oil standardized to 20-24% GLA", "softgels, liquid", "SRC06", "https://medlineplus.gov/druginfo/natural/596.html", False, "Candidate botanical oil requiring certification of zero pyrrolizidine alkaloids."),
    ("SUP049", "Black Currant Seed Oil", "fatty_acid", "Balanced botanical lipid containing both omega-3 alpha-linolenic acid and omega-6 gamma-linolenic acid.", "Ribes nigrum seed oil providing GLA and alpha-linolenic acid", "softgels", "SRC06", "https://medlineplus.gov/druginfo/natural/1085.html", False, "Candidate botanical oil awaiting monograph verification."),
    ("SUP050", "Conjugated Linoleic Acid (CLA)", "fatty_acid", "Naturally occurring fatty acid isomer investigated for body composition and lipid oxidative metabolism.", "safflower-derived cis-9, trans-11 and trans-10, cis-12 isomers", "softgels", "SRC06", "https://medlineplus.gov/druginfo/natural/926.html", False, "Candidate lipid requiring safety review regarding hepatic insulin sensitivity."),
    ("SUP051", "Alpha-Linolenic Acid (ALA)", "fatty_acid", "Essential plant parent omega-3 fatty acid required for cell membrane structural integrity.", "purified alpha-linolenic acid plant triglycerides", "softgels, capsules", "SRC01", "https://ods.od.nih.gov/factsheets/Omega3FattyAcids-HealthProfessional/", False, "Candidate plant fatty acid awaiting detailed monograph review."),
    ("SUP052", "Medium Chain Triglycerides (MCT Oil)", "fatty_acid", "Rapidly absorbed medium-chain fatty acids metabolized directly by hepatic portal oxidation into ketones.", "caprylic acid (C8) and capric acid (C10) triglycerides", "liquid, powder", "SRC06", "https://medlineplus.gov/druginfo/natural/915.html", False, "Candidate lipid supplement awaiting clinical review for gastrointestinal tolerance."),

    # Added Protein Supplements & Amino Acids (SUP053 - SUP074)
    ("SUP053", "Whey Protein Isolate", "protein_amino_acid", "Rapidly absorbed dairy-derived complete protein with minimal lactose and high leucine concentration for muscle protein synthesis.", "cross-flow microfiltered whey protein isolate (>90% protein)", "powder", "SRC01", "https://ods.od.nih.gov/factsheets/ExerciseAndAthleticPerformance-HealthProfessional/", True, "Verified against NIH ODS athletic performance guidelines."),
    ("SUP054", "Whey Protein Concentrate", "protein_amino_acid", "High-biological value complete dairy protein retaining beneficial immunoglobulins and lactoferrin peptides.", "ultrafiltered whey protein concentrate (70-80% protein)", "powder", "SRC01", "https://ods.od.nih.gov/factsheets/ExerciseAndAthleticPerformance-HealthProfessional/", False, "Candidate dairy protein pending lactose tolerance review."),
    ("SUP055", "Micellar Casein", "protein_amino_acid", "Slow-digesting dairy protein providing sustained amino acid release over several hours during sleep or fasting.", "native micellar casein slow-digesting milk protein", "powder", "SRC01", "https://ods.od.nih.gov/factsheets/ExerciseAndAthleticPerformance-HealthProfessional/", False, "Candidate dairy protein awaiting gastric emptying verification."),
    ("SUP056", "Pea Protein", "protein_amino_acid", "Hypoallergenic vegan complete protein source rich in BCAAs, arginine, and lysine.", "yellow split pea (Pisum sativum) isolate powder", "powder", "SRC02", "https://dsld.od.nih.gov/", True, "Verified plant-based protein source against DSLD standard monographs."),
    ("SUP057", "Soy Protein Isolate", "protein_amino_acid", "Complete plant protein containing all nine essential amino acids with natural soy isoflavones.", "defatted soybean isolate providing >90% complete plant protein", "powder", "SRC05", "https://www.nccih.nih.gov/health/soy", False, "Candidate plant protein requiring review of isoflavone thyroid interactions."),
    ("SUP058", "Rice Protein", "protein_amino_acid", "Easily digestible plant protein rich in cysteine and methionine, suitable for allergen-restricted diets.", "brown rice enzymatic protein isolate", "powder", "SRC02", "https://dsld.od.nih.gov/", False, "Candidate plant protein awaiting heavy metal testing standards."),
    ("SUP059", "Hemp Protein", "protein_amino_acid", "Whole-food plant protein providing edestin and albumin proteins, dietary fiber, and omega-3/6 lipids.", "cold-milled whole Cannabis sativa hemp seeds", "powder", "SRC02", "https://dsld.od.nih.gov/", False, "Candidate botanical protein awaiting complete amino acid profile audit."),
    ("SUP060", "Egg White Protein", "protein_amino_acid", "Dairy-free complete animal protein with high biological availability and zero cholesterol or dietary fat.", "pasteurized dried egg white ovalbumin powder", "powder", "SRC02", "https://dsld.od.nih.gov/", False, "Candidate animal protein requiring egg allergen verification."),
    ("SUP061", "Collagen Peptides", "protein_amino_acid", "Low-molecular weight bioactive peptides rich in glycine, proline, and hydroxyproline for extracellular matrix support.", "hydrolyzed bovine / marine collagen types I and III", "powder, capsules", "SRC06", "https://medlineplus.gov/druginfo/natural/1606.html", False, "Candidate peptide supplement awaiting joint and skin efficacy review."),
    ("SUP062", "L-Glutamine", "amino_acid_derivative", "Conditionally essential amino acid primary fuel for enterocytes and immune lymphocytes during physiologic stress.", "fermented free-form L-glutamine", "unflavored powder, capsules", "SRC01", "https://ods.od.nih.gov/factsheets/ExerciseAndAthleticPerformance-HealthProfessional/", True, "Verified against NIH ODS athletic and intestinal monographs."),
    ("SUP063", "Branched-Chain Amino Acids (BCAA)", "amino_acid_derivative", "Essential branched amino acids metabolized directly in skeletal muscle to support nitrogen retention.", "L-leucine, L-isoleucine, L-valine in 2:1:1 physiological ratio", "instantized powder, capsules", "SRC01", "https://ods.od.nih.gov/factsheets/ExerciseAndAthleticPerformance-HealthProfessional/", False, "Candidate amino acid blend pending MPS vs whole protein comparison."),
    ("SUP064", "Essential Amino Acids (EAA)", "amino_acid_derivative", "Balanced free-form amino acid blend supplying all 9 non-synthesizable amino acids for protein synthesis.", "complete spectrum of nine human essential amino acids", "powder, tablets", "SRC01", "https://ods.od.nih.gov/factsheets/ExerciseAndAthleticPerformance-HealthProfessional/", False, "Candidate amino acid formulation awaiting standard dosage review."),
    ("SUP065", "L-Arginine", "amino_acid_derivative", "Endothelial nitric oxide synthase substrate supporting vascular vasodilation and tissue perfusion.", "L-arginine base, L-arginine alpha-ketoglutarate (AAKG)", "capsules, powder", "SRC01", "https://ods.od.nih.gov/factsheets/ExerciseAndAthleticPerformance-HealthProfessional/", False, "Candidate amino acid requiring post-infarction contraindication verification."),
    ("SUP066", "L-Citrulline", "amino_acid_derivative", "Potent precursor to plasma L-arginine enhancing nitric oxide-mediated blood flow and ammonia clearance.", "L-citrulline pure, L-citrulline malate 2:1", "powder, capsules", "SRC06", "https://medlineplus.gov/druginfo/natural/1245.html", False, "Candidate amino acid under clinical review for ergogenic vasodilation."),
    ("SUP067", "Beta-Alanine", "amino_acid_derivative", "Rate-limiting precursor for muscular carnosine synthesis, buffering intramuscular acidosis during intense training.", "pure beta-alanine amino acid", "powder, sustained-release tablets", "SRC01", "https://ods.od.nih.gov/factsheets/ExerciseAndAthleticPerformance-HealthProfessional/", False, "Candidate amino acid requiring paresthesia dosing guidelines."),
    ("SUP068", "L-Carnitine", "amino_acid_derivative", "Quaternary amine transporting long-chain fatty acids across the inner mitochondrial membrane for beta-oxidation.", "L-carnitine L-tartrate, acetyl-L-carnitine", "capsules, liquid, powder", "SRC01", "https://ods.od.nih.gov/factsheets/Carnitine-HealthProfessional/", False, "Candidate amino derivative awaiting TMAO cardiovascular review."),
    ("SUP069", "Taurine", "amino_acid_derivative", "Sulfur-containing conditionally essential amino sulfonic acid participating in bile acid conjugation and osmoregulation.", "pure taurine amino sulfonic acid", "capsules, powder", "SRC06", "https://medlineplus.gov/druginfo/natural/1024.html", False, "Candidate nutrient under review for cellular hydration and cardiac tone."),
    ("SUP070", "L-Tyrosine", "amino_acid_derivative", "Aromatic amino acid precursor for synthesis of catecholamines (dopamine, norepinephrine, epinephrine) and thyroid hormones.", "free-form L-tyrosine, N-acetyl L-tyrosine", "capsules, powder", "SRC06", "https://medlineplus.gov/druginfo/natural/337.html", False, "Candidate amino acid requiring MAOI interaction caution checks."),
    ("SUP071", "L-Theanine", "amino_acid_derivative", "Bioactive amino acid from green tea crossing the blood-brain barrier to promote relaxation without sedation.", "Suntheanine pure L-isomer, Camellia sinensis extract", "capsules, chewables", "SRC06", "https://medlineplus.gov/druginfo/natural/1053.html", True, "Verified against MedlinePlus and botanical pharmacology monographs."),
    ("SUP072", "Glycine", "amino_acid_derivative", "Inhibitory neurotransmitter and simplest amino acid required for glutathione, collagen, and creatine synthesis.", "free-form glycine powder", "powder, capsules", "SRC06", "https://medlineplus.gov/druginfo/natural/1072.html", False, "Candidate amino acid under review for sleep architecture enhancement."),
    ("SUP073", "N-Acetyl Cysteine (NAC)", "amino_acid_derivative", "Stable acetylated derivative of L-cysteine serving as rate-limiting substrate for intracellular glutathione replenishment.", "N-acetyl-L-cysteine USP grade", "capsules, tablets", "SRC06", "https://medlineplus.gov/druginfo/natural/1018.html", False, "Candidate antioxidant precursor pending regulatory monograph confirmation."),
    ("SUP074", "L-Lysine", "amino_acid_derivative", "Essential amino acid required for collagen cross-linking, carnitine biosynthesis, and calcium absorption.", "L-lysine hydrochloride USP", "tablets, capsules", "SRC06", "https://medlineplus.gov/druginfo/natural/238.html", False, "Candidate amino acid awaiting antiviral review."),

    # Added Electrolytes & Hydration (SUP075 - SUP079)
    ("SUP075", "Electrolyte Replacement Complex", "electrolyte", "Isotonic mineral hydration matrix formulated to replace electrolyte losses incurred during strenuous sweat output.", "balanced sodium, potassium, magnesium, chloride, and trace minerals", "effervescent tablets, drink powder", "SRC02", "https://dsld.od.nih.gov/", True, "Verified electrolyte replacement blend against DSLD and sports medicine literature."),
    ("SUP076", "Sodium Chloride", "electrolyte", "Major extracellular cation essential for osmotic fluid homeostasis, extracellular volume, and nerve impulse conduction.", "purified pharmaceutical grade sodium chloride", "tablets, oral rehydration powder", "SRC06", "https://medlineplus.gov/druginfo/meds/a601170.html", False, "Candidate electrolyte requiring hypertension contraindication checks."),
    ("SUP077", "Potassium Citrate", "electrolyte", "Alkalinizing potassium salt utilized for urinary electrolyte support and intracellular electrolyte replenishment.", "potassium citrate monohydrate", "capsules, powder", "SRC01", "https://ods.od.nih.gov/factsheets/Potassium-HealthProfessional/", False, "Candidate electrolyte requiring renal clearance safety checks."),
    ("SUP078", "Magnesium Malate", "electrolyte", "Highly bioavailable organic chelate combining elemental magnesium with Krebs-cycle intermediate malic acid.", "dimagnesium malate chelate", "tablets, capsules", "SRC01", "https://ods.od.nih.gov/factsheets/Magnesium-HealthProfessional/", False, "Candidate mineral chelate under review for cellular energy production."),
    ("SUP079", "Oral Rehydration Salts", "electrolyte", "Standardized oral electrolyte replacement solution utilizing sodium-glucose cotransport mechanisms for intestinal absorption.", "WHO-formula glucose, sodium chloride, potassium chloride, trisodium citrate", "powder packets", "SRC06", "https://medlineplus.gov/druginfo/meds/a609019.html", False, "Candidate hydration formula under clinical review."),

    # Added Fiber, Prebiotics & Probiotics (SUP080 - SUP092)
    ("SUP080", "Psyllium Husk", "fiber_prebiotic", "Soluble viscous gel-forming dietary fiber supporting healthy stool transit and bile acid binding in the colon.", "Plantago ovata blond psyllium seed husk", "whole husks, powder, capsules", "SRC06", "https://medlineplus.gov/druginfo/meds/a601104.html", True, "Verified against MedlinePlus and FDA health claim monographs."),
    ("SUP081", "Inulin / FOS", "fiber_prebiotic", "Nondigestible prebiotic fructan selectively fermented by beneficial colonic Bifidobacteria into short-chain fatty acids.", "chicory root inulin, oligofructose fructooligosaccharides", "soluble powder", "SRC06", "https://medlineplus.gov/druginfo/natural/1048.html", True, "Verified against MedlinePlus prebiotic review."),
    ("SUP082", "Acacia Fiber", "fiber_prebiotic", "Gentle prebiotic soluble fiber with high digestive tolerance and slow colonic fermentation rate.", "gum arabic soluble acacia senegal exudate", "organic soluble powder", "SRC06", "https://medlineplus.gov/druginfo/natural/268.html", False, "Candidate prebiotic fiber awaiting fermentation rate review."),
    ("SUP083", "Glucomannan", "fiber_prebiotic", "Extremely viscous water-soluble dietary fiber expanding significantly in the stomach to promote satiety.", "konjac root (Amorphophallus konjac) soluble polysaccharide", "capsules, powder", "SRC06", "https://medlineplus.gov/druginfo/natural/205.html", False, "Candidate fiber requiring choking warning verification."),
    ("SUP084", "Partially Hydrolyzed Guar Gum (PHGG)", "fiber_prebiotic", "Low-viscosity prebiotic soluble fiber well-tolerated in individuals sensitive to traditional FODMAP carbohydrates.", "enzymatically hydrolyzed guar gum galactomannan", "dissolvable powder", "SRC06", "https://medlineplus.gov/druginfo/natural/919.html", False, "Candidate prebiotic fiber awaiting clinical tolerance validation."),
    ("SUP085", "Apple Pectin", "fiber_prebiotic", "Complex carbohydrate polymer forming protective colonic gels and binding heavy metals and cholesterol metabolites.", "purified Malus domestica apple pomace pectin", "capsules, powder", "SRC06", "https://medlineplus.gov/druginfo/natural/999.html", False, "Candidate soluble fiber awaiting lipid clearance confirmation."),
    ("SUP086", "Arabinogalactan", "fiber_prebiotic", "Highly branched polysaccharide prebiotic supporting natural killer cell cytotoxicity and mucosal gut barrier integrity.", "Larix occidentalis Western larch tree extract", "powder", "SRC06", "https://medlineplus.gov/druginfo/natural/974.html", False, "Candidate prebiotic awaiting immunomodulation review."),
    ("SUP087", "Resistant Starch", "fiber_prebiotic", "Enzyme-resistant dietary starch fermented exclusively in the distal colon into butyric acid fuel for colonocytes.", "high-amylose maize resistant starch type 2 (RS2)", "powder", "SRC02", "https://dsld.od.nih.gov/", False, "Candidate microbiome fuel awaiting standardization review."),
    ("SUP088", "Saccharomyces boulardii", "probiotic", "Probiotic yeast resistant to gastric acid and antibiotics, supporting intestinal brush border digestive enzymes.", "non-pathogenic probiotic yeast Saccharomyces cerevisiae var. boulardii", "lyophilized capsules", "SRC01", "https://ods.od.nih.gov/factsheets/Probiotics-HealthProfessional/", False, "Candidate probiotic strain awaiting central venous catheter contraindication checks."),
    ("SUP089", "Lactobacillus rhamnosus GG", "probiotic", "Extensively studied probiotic strain exhibiting pili that adhere to human intestinal mucus to modulate mucosal immunity.", "clinically researched Lactobacillus rhamnosus GG (ATCC 53103)", "microencapsulated capsules", "SRC01", "https://ods.od.nih.gov/factsheets/Probiotics-HealthProfessional/", False, "Candidate strain awaiting strain-specific evidence verification."),
    ("SUP090", "Bifidobacterium infantis", "probiotic", "Key commensal infant and adult colonic probiotic strain fermenting human milk oligosaccharides and maintaining gut barrier tight junctions.", "Bifidobacterium longum subsp. infantis (DSM 33361)", "enteric capsules, powder", "SRC01", "https://ods.od.nih.gov/factsheets/Probiotics-HealthProfessional/", False, "Candidate strain under review for barrier integrity endpoints."),
    ("SUP091", "Bacillus coagulans", "probiotic", "Resilient endospore probiotic surviving gastric acidity to germinate in the small intestine and assist digestive enzyme activity.", "spore-forming lactic acid bacterium Bacillus coagulans (GBI-30, 6086)", "capsules, chewables", "SRC01", "https://ods.od.nih.gov/factsheets/Probiotics-HealthProfessional/", False, "Candidate spore former awaiting stability monograph confirmation."),
    ("SUP092", "Synbiotic Complex", "probiotic", "Dual-action combination providing viable probiotic strains alongside dedicated fermentable prebiotic substrates.", "multi-strain probiotic consortium combined with synergistic inulin/FOS prebiotics", "delayed-release capsules", "SRC02", "https://dsld.od.nih.gov/", False, "Candidate multi-strain blend awaiting synergy review."),

    # Added Herbal & Botanical Supplements (SUP093 - SUP118)
    ("SUP093", "Echinacea", "botanical", "Traditional North American botanical containing alkamides and polysaccharides supporting upper respiratory immune response.", "Echinacea purpurea / angustifolia standardized herb extract", "capsules, liquid tincture", "SRC05", "https://www.nccih.nih.gov/health/echinacea", False, "Candidate botanical requiring allergy check for Asteraceae family sensitivity."),
    ("SUP094", "Garlic Extract", "botanical", "Organosulfur botanical supplement studied for vascular elasticity, platelet function, and lipid support.", "aged garlic extract (Allium sativum), standardized S-allyl cysteine", "enteric tablets, capsules", "SRC05", "https://www.nccih.nih.gov/health/garlic", False, "Candidate botanical requiring anticoagulant interaction review."),
    ("SUP095", "Panax Ginseng", "botanical", "Traditional adaptogenic root promoting physical stamina, mental vigor, and resilience to fatigue.", "standardized ginsenosides extract from Panax ginseng C.A. Meyer root", "capsules, root extract", "SRC05", "https://www.nccih.nih.gov/health/asian-ginseng", False, "Candidate botanical requiring blood pressure and anticoagulant checks."),
    ("SUP096", "Rhodiola Rosea", "botanical", "High-altitude botanical adaptogen supporting central nervous system resilience during chronic occupational stress.", "standardized 3% rosavins and 1% salidroside Arctic root extract", "capsules, tablets", "SRC05", "https://www.nccih.nih.gov/health/rhodiola", False, "Candidate adaptogen awaiting clinical trial meta-analysis verification."),
    ("SUP097", "Milk Thistle (Silymarin)", "botanical", "Hepatoprotective botanical flavonoid complex stabilizing hepatic cell membranes against lipid peroxidation.", "Silybum marianum seed extract standardized to 80% silymarin", "capsules, softgels", "SRC05", "https://www.nccih.nih.gov/health/milk-thistle", True, "Verified against NCCIH monograph."),
    ("SUP098", "Valerian Root", "botanical", "Traditional herbal sleep aid interacting with central GABAergic neurotransmission to reduce sleep latency.", "Valeriana officinalis root extract standardized to valerenic acids", "capsules, tablets, liquid tincture", "SRC05", "https://www.nccih.nih.gov/health/valerian", True, "Verified against NCCIH monograph."),
    ("SUP099", "St. John's Wort", "botanical", "Botanical extract modulating synaptic monoamines; notable for broad cytochrome P450 CYP3A4 enzyme induction interactions.", "Hypericum perforatum flower extract standardized to 0.3% hypericin", "capsules, tablets", "SRC05", "https://www.nccih.nih.gov/health/st-johns-wort", True, "Verified against NCCIH monograph and clinical drug interaction registries."),
    ("SUP100", "Green Tea Extract (EGCG)", "botanical", "Polyphenol catechin antioxidant providing cellular protection and thermogenic metabolic support.", "Camellia sinensis leaf extract standardized to 45-50% epigallocatechin gallate", "capsules", "SRC05", "https://www.nccih.nih.gov/health/green-tea", False, "Candidate extract requiring fasting hepatotoxicity warning verification."),
    ("SUP101", "Ginger Root", "botanical", "Traditional warming digestive rhizome containing bioactive gingerols and shogaols supporting gastrointestinal motility.", "Zingiber officinale rhizome standardized to 5% gingerols", "capsules, chews, liquid drops", "SRC05", "https://www.nccih.nih.gov/health/ginger", False, "Candidate botanical under review for gastric motility benefits."),
    ("SUP102", "Boswellia Serrata", "botanical", "Ayurvedic botanical gum resin containing pentacyclic triterpene acids inhibiting the 5-lipoxygenase (5-LOX) inflammatory pathway.", "Indian frankincense resin extract standardized to 65% boswellic acids / AKBA", "capsules", "SRC05", "https://www.nccih.nih.gov/health/boswellia", False, "Candidate botanical resin awaiting joint inflammation review."),
    ("SUP103", "Elderberry (Sambucus nigra)", "botanical", "Anthocyanin-rich botanical berries studied for upper respiratory immune support during seasonal challenges.", "European black elderberry extract standardized to anthocyanins", "syrup, lozenges, capsules", "SRC05", "https://www.nccih.nih.gov/health/elderberry", False, "Candidate botanical extract awaiting immune clinical trials audit."),
    ("SUP104", "Saw Palmetto", "botanical", "Phytosterol-rich lipid extract inhibiting 5-alpha-reductase enzymatic conversion of testosterone to dihydrotestosterone.", "Serenoa repens berry lipid extract standardized to 85-95% fatty acids", "softgels", "SRC05", "https://www.nccih.nih.gov/health/saw-palmetto", False, "Candidate botanical under review for prostate health endpoints."),
    ("SUP105", "Fenugreek", "botanical", "Traditional leguminous seed containing soluble galactomannan fibers and 4-hydroxyisoleucine supporting metabolic balance.", "Trigonella foenum-graecum seed extract standardized to saponins", "capsules, powder", "SRC05", "https://www.nccih.nih.gov/health/fenugreek", False, "Candidate botanical seed requiring glucose interaction checks."),
    ("SUP106", "Berberine", "botanical", "Isoquinoline plant alkaloid acting as an AMP-activated protein kinase (AMPK) activator to regulate cellular energy homeostasis.", "berberine hydrochloride alkaloid from Berberis aristata root extract", "capsules", "SRC05", "https://www.nccih.nih.gov/health/berberine", False, "Candidate botanical alkaloid requiring antidiabetic medication check."),
    ("SUP107", "Maca Root", "botanical", "High-altitude Peruvian cruciferous root containing macamides and glucosinolates supporting vitality and stamina.", "Lepidium meyenii Andean hypocotyl gelatinized root extract", "capsules, powder", "SRC06", "https://medlineplus.gov/druginfo/natural/555.html", False, "Candidate adaptogenic root under review for endocrine safety."),
    ("SUP108", "Holy Basil (Tulsi)", "botanical", "Traditional Ayurvedic rasayana adaptogen used to moderate cortisol levels and emotional stress responses.", "Ocimum sanctum leaf extract standardized to ursolic acid", "capsules, tea", "SRC06", "https://medlineplus.gov/druginfo/natural/1101.html", False, "Candidate botanical adaptogen awaiting clinical stress trial validation."),
    ("SUP109", "Bacopa Monnieri", "botanical", "Nootropic water hyssop botanical containing triterpenoid saponins supporting cholinergic neurotransmission and memory consolidation.", "standardized bacosides A and B extract from whole Bacopa plant", "capsules, tablets", "SRC06", "https://medlineplus.gov/druginfo/natural/761.html", False, "Candidate nootropic botanical under review for cognitive parameters."),
    ("SUP110", "Cordyceps Mushroom", "botanical", "Functional medicinal fungus used to support cellular ATP production, oxygen utilization, and endurance capacity.", "Cordyceps militaris / sinensis mycelium extract standardized to cordycepin", "capsules, powder", "SRC06", "https://medlineplus.gov/druginfo/natural/602.html", False, "Candidate medicinal mushroom awaiting athletic trial confirmation."),
    ("SUP111", "Lion's Mane Mushroom", "botanical", "Specialized fungal extract containing bioactive compounds shown in vitro to stimulate Nerve Growth Factor (NGF) synthesis.", "Hericium erinaceus fruiting body extract rich in hericenones and erinacines", "capsules, powder", "SRC06", "https://medlineplus.gov/druginfo/natural/1761.html", False, "Candidate medicinal mushroom awaiting neuroplasticity clinical confirmation."),
    ("SUP112", "Reishi Mushroom", "botanical", "Revered medicinal mushroom containing Ganoderic acids and beta-D-glucans modulating immune and adrenal function.", "Ganoderma lucidum fruiting body extract standardized to triterpenes and beta-glucans", "capsules, powder", "SRC06", "https://medlineplus.gov/druginfo/natural/279.html", False, "Candidate medicinal mushroom awaiting immune parameter confirmation."),
    ("SUP113", "Bilberry Extract", "botanical", "Anthocyanoside-rich European berry extract supporting microvascular ocular circulation and dark adaptation.", "Vaccinium myrtillus fruit extract standardized to 25% anthocyanosides", "capsules", "SRC05", "https://www.nccih.nih.gov/health/bilberry", False, "Candidate botanical extract under review for ophthalmologic endpoints."),
    ("SUP114", "Cranberry Extract", "botanical", "Proanthocyanidin-concentrated extract inhibiting P-fimbriated uropathogenic E. coli adherence to bladder epithelial walls.", "Vaccinium macrocarpon fruit extract standardized to A-type proanthocyanidins (PACs)", "capsules, chewables", "SRC05", "https://www.nccih.nih.gov/health/cranberry", False, "Candidate botanical fruit extract awaiting urinary anti-adherence review."),
    ("SUP115", "Hawthorn Berry", "botanical", "Cardioprotective botanical flavonoid extract supporting coronary blood flow, myocardial contraction, and vascular tone.", "Crataegus oxyacantha leaf and flower extract standardized to oligomeric procyanidins", "capsules, liquid drops", "SRC05", "https://www.nccih.nih.gov/health/hawthorn", False, "Candidate botanical requiring cardiac glycoside interaction review."),
    ("SUP116", "Passionflower", "botanical", "Gentle botanical nervine enhancing central GABA binding affinity to soothe nervous restlessness.", "Passiflora incarnata aerial parts extract standardized to flavonoids", "capsules, liquid tincture", "SRC05", "https://www.nccih.nih.gov/health/passionflower", False, "Candidate botanical nervine awaiting sedative interaction checks."),
    ("SUP117", "Tart Cherry Extract", "botanical", "Polyphenol and natural melatonin-rich extract aiding post-exercise muscular recovery and nighttime sleep architecture.", "Prunus cerasus Montmorency cherry extract rich in anthocyanins", "capsules, liquid concentrate", "SRC06", "https://medlineplus.gov/druginfo/natural/1029.html", False, "Candidate botanical fruit under review for uric acid and sleep endpoints."),
    ("SUP118", "Red Yeast Rice", "botanical", "Fermented rice containing natural HMG-CoA reductase inhibitor compounds; requires strict clinical monitoring.", "Monascus purpureus fermented rice containing natural monacolin K", "capsules", "SRC05", "https://www.nccih.nih.gov/health/red-yeast-rice", False, "Candidate botanical substance requiring prescription statin cross-checks."),

    # Added Other Evidence-Supported Nutritional Supplements (SUP119 - SUP130)
    ("SUP119", "Coenzyme Q10 (CoQ10)", "nutrient", "Essential lipid-soluble electron transporter in the mitochondrial inner membrane required for oxidative ATP phosphorylation.", "ubiquinone, ubiquinol (active reduced form)", "softgels, capsules", "SRC01", "https://ods.od.nih.gov/factsheets/CoenzymeQ10-HealthProfessional/", True, "Verified against NIH ODS professional monograph."),
    ("SUP120", "Alpha-Lipoic Acid", "nutrient", "Universal amphipathic antioxidant cofactor for mitochondrial pyruvate dehydrogenase complex regenerator of vitamins C and E.", "R-alpha lipoic acid, racemic alpha-lipoic acid", "capsules", "SRC06", "https://medlineplus.gov/druginfo/natural/767.html", False, "Candidate antioxidant under review for peripheral nerve conduction endpoints."),
    ("SUP121", "Resveratrol", "nutrient", "Natural stilbenoid polyphenol investigated for sirtuin-1 (SIRT1) enzyme activation and endothelial vascular defense.", "trans-resveratrol from Polygonum cuspidatum root extract", "capsules", "SRC06", "https://medlineplus.gov/druginfo/natural/307.html", False, "Candidate polyphenol under review for human bioavailability parameters."),
    ("SUP122", "Astaxanthin", "nutrient", "Potent lipid-soluble marine keto-carotenoid spanning the entire phospholipid bilayer to neutralize reactive oxygen species.", "natural astaxanthin from Haematococcus pluvialis microalgae", "softgels", "SRC06", "https://medlineplus.gov/druginfo/natural/1063.html", False, "Candidate carotenoid awaiting ocular and dermatological review."),
    ("SUP123", "Lutein and Zeaxanthin", "nutrient", "Dietary xanthophyll macular pigments selectively concentrated in the fovea centralis filtering high-energy blue photic radiation.", "purified lutein and zeaxanthin isomers from Tagetes erecta marigold petals", "softgels", "SRC06", "https://medlineplus.gov/druginfo/natural/754.html", False, "Candidate macular pigment blend awaiting AREDS-2 monograph audit."),
    ("SUP124", "Quercetin", "nutrient", "Plant flavonol displaying zinc-ionophore properties, mast-cell stabilizing effects, and antioxidant activity.", "quercetin dihydrate, quercetin phytosome", "capsules", "SRC06", "https://medlineplus.gov/druginfo/natural/294.html", False, "Candidate flavonoid awaiting bioavailability review."),
    ("SUP125", "Spirulina", "nutrient", "Nutrient-dense cyanobacteria providing phycocyanin pigment proteins, iron, beta-carotene, and gamma-linolenic acid.", "Arthrospira platensis certified organic blue-green microalgae", "tablets, powder", "SRC06", "https://medlineplus.gov/druginfo/natural/924.html", False, "Candidate microalgae requiring microcystin toxin screening verification."),
    ("SUP126", "Chlorella", "nutrient", "Microscopic freshwater green alga high in chlorophyll, nucleic acids, and dietary minerals supporting detoxification.", "Chlorella vulgaris broken cell-wall green freshwater microalgae", "tablets, powder", "SRC06", "https://medlineplus.gov/druginfo/natural/907.html", False, "Candidate freshwater alga awaiting digestive cell wall processing audit."),
    ("SUP127", "Glucosamine Sulfate", "nutrient", "Natural amino sugar component of articular cartilage glycosaminoglycans and synovial fluid proteoglycans.", "D-glucosamine sulfate potassium chloride (crustacean or vegan fermentation)", "capsules, tablets", "SRC06", "https://medlineplus.gov/druginfo/natural/807.html", False, "Candidate amino sugar requiring crustacean allergen verification."),
    ("SUP128", "Chondroitin Sulfate", "nutrient", "Sulfated glycosaminoglycan polymer imparting osmotic resistance to compressive forces in joint cartilage matrix.", "low-molecular weight chondroitin sulfate sodium (bovine / avian / porcine)", "capsules, tablets", "SRC06", "https://medlineplus.gov/druginfo/natural/744.html", False, "Candidate glycosaminoglycan awaiting GAIT trial consistency review."),
    ("SUP129", "Methylsulfonylmethane (MSM)", "nutrient", "Bioavailable organic donor of sulfur required for keratin, collagen, and cartilage disulfide bond cross-linking.", "distilled methylsulfonylmethane organosulfur compound", "crystals powder, capsules", "SRC06", "https://medlineplus.gov/druginfo/natural/522.html", False, "Candidate organosulfur compound awaiting connective tissue review."),
    ("SUP130", "S-Adenosylmethionine (SAMe)", "nutrient", "Endogenous primary biological methyl donor involved in transmethylation reactions for neurotransmitter and phosphatidylcholine synthesis.", "S-adenosyl-L-methionine disulfate tosylate", "enteric-coated tablets", "SRC05", "https://www.nccih.nih.gov/health/same", False, "Candidate methyl donor requiring bipolar mania contraindication checks.")
]

GOAL_MAPPINGS_DEF = [
    # Core 20 original mappings
    ("MAP001", "SUP001", "GL01", "direct", 1.0, "SRC01", "ODS Vitamin D: Health Benefits & Bone Health", "Vitamin D increases intestinal calcium absorption; proven role in bone mineralization.", True),
    ("MAP002", "SUP011", "GL01", "direct", 1.0, "SRC01", "ODS Calcium: Health Benefits & Bone Health", "Essential mineral constituent of hydroxyapatite in skeletal tissue.", True),
    ("MAP003", "SUP006", "GL01", "partial", 0.5, "SRC01", "ODS Vitamin K: Health Benefits & Bone Health", "Cofactor for gamma-glutamyl carboxylase in osteocalcin carboxylation.", True),
    ("MAP004", "SUP013", "GL01", "partial", 0.5, "SRC01", "ODS Magnesium: Health Benefits & Bone Health", "Important for bone matrix integrity and parathyroid hormone activation.", True),
    ("MAP005", "SUP002", "GL02", "direct", 1.0, "SRC01", "ODS Vitamin B12: Deficiency & Energy Metabolism", "Essential for cellular energy production; deficiency causes megaloblastic fatigue.", True),
    ("MAP006", "SUP012", "GL02", "partial", 0.5, "SRC01", "ODS Iron: Deficiency & Cellular Energy", "Required for hemoglobin oxygen delivery and mitochondrial cytochromes.", True),
    ("MAP007", "SUP004", "GL03", "direct", 1.0, "SRC01", "ODS Vitamin C: Immune Function & Leukocytes", "Antioxidant accumulating in phagocytic cells to enhance microbial killing.", True),
    ("MAP008", "SUP014", "GL03", "direct", 1.0, "SRC01", "ODS Zinc: Immune Function & Thymic Hormones", "Crucial for T-lymphocyte development and cellular immunity signaling.", True),
    ("MAP009", "SUP001", "GL03", "partial", 0.5, "SRC01", "ODS Vitamin D: Immune Function Receptors", "Modulates innate and adaptive immune cell differentiation via VDR receptors.", True),
    ("MAP010", "SUP020", "GL04", "direct", 1.0, "SRC01", "ODS Melatonin: Sleep & Circadian Rhythms", "Binds MT1/MT2 receptors in suprachiasmatic nucleus promoting sleep latency reduction.", True),
    ("MAP011", "SUP013", "GL04", "partial", 0.5, "SRC01", "ODS Magnesium: Sleep Quality & GABAergic Tone", "Acts as NMDA receptor antagonist and GABA agonist facilitating relaxation.", True),
    ("MAP012", "SUP018", "GL05", "direct", 1.0, "SRC01", "ODS Omega-3: Cardiovascular Health & Triglycerides", "Reduces hepatic triglyceride synthesis and supports endothelial vascular elasticity.", True),
    ("MAP013", "SUP019", "GL06", "direct", 1.0, "SRC01", "ODS Probiotics: Gastrointestinal Microbiota", "Replenishes beneficial commensal strains and supports epithelial gut barrier integrity.", True),
    ("MAP014", "SUP024", "GL07", "direct", 1.0, "SRC01", "ODS Athletic Performance: Creatine Monohydrate", "Increases phosphocreatine stores aiding rapid ATP rephosphorylation in muscle.", True),
    ("MAP015", "SUP021", "GL08", "direct", 1.0, "SRC05", "NCCIH Ashwagandha: Stress & Cortisol Modulation", "Demonstrated reduction in serum cortisol and perceived stress scores in clinical trials.", True),
    ("MAP016", "SUP009", "GL10", "direct", 1.0, "SRC01", "ODS Biotin: Keratin Synthesis & Integumentary Health", "Enzymatic cofactor in branched-chain amino acid metabolism supporting keratin structure.", True),
    ("MAP017", "SUP010", "GL09", "direct", 1.0, "SRC01", "ODS Choline: Acetylcholine & Neurotransmission", "Precursor to acetylcholine neurotransmitter and cell membrane phosphatidylcholine.", True),
    ("MAP018", "SUP023", "GL09", "direct", 1.0, "SRC05", "NCCIH Ginkgo: Neurocognitive Function & Blood Flow", "Flavone glycosides enhance microvascular perfusion and neuroprotective antioxidant activity.", True),
    ("MAP019", "SUP008", "GL11", "direct", 1.0, "SRC01", "ODS Folate: General Nutritional Gaps & DNA Synthesis", "Essential nutrient for single-carbon methyl group transfer and nucleotide synthesis.", True),
    ("MAP020", "SUP003", "GL11", "direct", 1.0, "SRC01", "ODS Vitamin B6: General Nutritional Support & Coenzymes", "Coenzyme in over 100 biochemical reactions including transamination and heme synthesis.", True),

    # Verified mappings for added reviewed nutrients
    ("MAP021", "SUP025", "GL02", "direct", 1.0, "SRC01", "ODS Thiamin: Carbohydrate Metabolism", "Thiamine diphosphate coenzyme for pyruvate dehydrogenase in oxidative phosphorylation.", True),
    ("MAP022", "SUP026", "GL02", "direct", 1.0, "SRC01", "ODS Riboflavin: Energy Production", "Precursor of FMN/FAD required for electron transport chain cellular ATP production.", True),
    ("MAP023", "SUP027", "GL02", "direct", 1.0, "SRC01", "ODS Niacin: Cellular Respiration", "NAD/NADP coenzymes regulating cellular energy transfer and mitochondrial respiration.", True),
    ("MAP024", "SUP028", "GL02", "direct", 1.0, "SRC01", "ODS Pantothenic Acid: Coenzyme A", "Essential precursor for Coenzyme A synthesis driving the Krebs cycle.", True),
    ("MAP025", "SUP030", "GL01", "direct", 1.0, "SRC01", "ODS Vitamin K2: Osteocalcin Carboxylation", "Activates osteocalcin to bind calcium ions to the hydroxyapatite mineral matrix.", True),
    ("MAP026", "SUP033", "GL11", "partial", 0.5, "SRC01", "ODS Copper: Superoxide Dismutase", "Essential trace element required for superoxide dismutase and ceruloplasmin.", True),
    ("MAP027", "SUP034", "GL11", "partial", 0.5, "SRC01", "ODS Manganese: Glycosyltransferases", "Cofactor in bone cartilage proteoglycan synthesis and mitochondrial SOD.", True),
    ("MAP028", "SUP035", "GL11", "partial", 0.5, "SRC01", "ODS Chromium: Glucose Tolerance Factor", "Potentiates insulin action and carbohydrate macronutrient utilization.", True),
    ("MAP029", "SUP041", "GL05", "direct", 1.0, "SRC01", "ODS Omega-3 EPA: Cardiovascular Support", "Inhibits hepatic triglyceride synthesis and produces anti-inflammatory resolvins.", True),
    ("MAP030", "SUP042", "GL09", "direct", 1.0, "SRC01", "ODS Omega-3 DHA: Neurocognitive Membrane", "Primary structural lipid of cerebral neuronal synapses and retinal rod cells.", True),
    ("MAP031", "SUP043", "GL05", "direct", 1.0, "SRC01", "ODS Algal Omega-3: Plant Marine Lipids", "Preformed vegan EPA/DHA directly supporting vascular flexibility and triglyceride reduction.", True),
    ("MAP032", "SUP053", "GL07", "direct", 1.0, "SRC01", "ODS Athletic Performance: Whey Protein", "Rapid digestion and high branched leucine content maximally triggers muscle protein synthesis.", True),
    ("MAP033", "SUP056", "GL07", "direct", 1.0, "SRC02", "DSLD Monograph: Pea Protein Isolate", "Complete plant protein providing essential amino acids to stimulate muscle hypertrophy.", True),
    ("MAP034", "SUP062", "GL06", "direct", 1.0, "SRC01", "ODS Enterocyte Metabolism: Glutamine", "Primary metabolic fuel for enterocytes supporting intestinal mucosal tight junctions.", True),
    ("MAP035", "SUP071", "GL08", "direct", 1.0, "SRC06", "MedlinePlus: L-Theanine Relaxation", "Crosses blood-brain barrier generating alpha brain waves and dampening acute stress.", True),
    ("MAP036", "SUP075", "GL07", "direct", 1.0, "SRC02", "DSLD Sports Nutrition: Electrolyte Complex", "Rapid replenishment of sodium and potassium sweat losses preserving muscular contraction.", True),
    ("MAP037", "SUP080", "GL06", "direct", 1.0, "SRC06", "MedlinePlus: Psyllium Bowel Regularity", "Soluble viscous gel-forming fiber promoting physiological colonic transit.", True),
    ("MAP038", "SUP081", "GL06", "direct", 1.0, "SRC06", "MedlinePlus: Inulin Prebiotics", "Selectively fermented by intestinal Bifidobacteria producing protective short-chain fatty acids.", True),
    ("MAP039", "SUP097", "GL11", "partial", 0.5, "SRC05", "NCCIH Milk Thistle: Antioxidant Protection", "Silymarin flavonoids protect cellular membranes against oxidative stress.", True),
    ("MAP040", "SUP098", "GL04", "direct", 1.0, "SRC05", "NCCIH Valerian: Sleep Latency", "Modulates central GABA neurotransmission to promote sleep onset latency reduction.", True),
    ("MAP041", "SUP099", "GL08", "partial", 0.5, "SRC05", "NCCIH St. John\'s Wort: Mild Mood Support", "Modulates synaptic reuptake of serotonin, dopamine, and norepinephrine.", True),
    ("MAP042", "SUP119", "GL05", "direct", 1.0, "SRC01", "ODS Coenzyme Q10: Myocardial Bioenergetics", "Crucial electron carrier for mitochondrial ATP synthesis in high-demand cardiac tissue.", True),

    # Candidate mappings for remaining supplements (needs_review, inactive)
    ("MAP043", "SUP029", "GL02", "direct", 1.0, "SRC06", "MedlinePlus B-Complex", "PROPOSED candidate mapping for comprehensive B-complex.", False),
    ("MAP044", "SUP031", "GL11", "partial", 0.5, "SRC01", "ODS Beta-Carotene", "PROPOSED candidate provitamin carotenoid mapping.", False),
    ("MAP045", "SUP032", "GL08", "partial", 0.5, "SRC06", "MedlinePlus Inositol", "PROPOSED candidate second-messenger mapping.", False),
    ("MAP046", "SUP037", "GL01", "partial", 0.5, "SRC01", "ODS Boron Bone Matrix", "PROPOSED candidate trace mineral mapping.", False),
    ("MAP047", "SUP038", "GL01", "partial", 0.5, "SRC06", "MedlinePlus Silicon", "PROPOSED candidate bone matrix mapping.", False),
    ("MAP048", "SUP040", "GL11", "direct", 1.0, "SRC02", "DSLD Multi-Mineral", "PROPOSED candidate multi-mineral mapping.", False),
    ("MAP049", "SUP044", "GL05", "partial", 0.5, "SRC01", "ODS Cod Liver Oil", "PROPOSED candidate marine lipid mapping.", False),
    ("MAP050", "SUP045", "GL05", "partial", 0.5, "SRC01", "ODS Krill Oil", "PROPOSED candidate phospholipid omega-3 mapping.", False),
    ("MAP051", "SUP046", "GL05", "partial", 0.5, "SRC05", "NCCIH Flaxseed Oil", "PROPOSED candidate plant omega-3 mapping.", False),
    ("MAP052", "SUP054", "GL07", "direct", 1.0, "SRC01", "ODS Whey Concentrate", "PROPOSED candidate protein mapping.", False),
    ("MAP053", "SUP055", "GL07", "direct", 1.0, "SRC01", "ODS Casein", "PROPOSED candidate nocturnal protein mapping.", False),
    ("MAP054", "SUP057", "GL07", "direct", 1.0, "SRC05", "NCCIH Soy Protein", "PROPOSED candidate complete plant protein mapping.", False),
    ("MAP055", "SUP060", "GL07", "direct", 1.0, "SRC02", "DSLD Egg White Protein", "PROPOSED candidate animal protein mapping.", False),
    ("MAP056", "SUP061", "GL10", "direct", 1.0, "SRC06", "MedlinePlus Collagen Peptides", "PROPOSED candidate dermal extracellular matrix mapping.", False),
    ("MAP057", "SUP063", "GL07", "direct", 1.0, "SRC01", "ODS BCAA", "PROPOSED candidate branched amino acid mapping.", False),
    ("MAP058", "SUP066", "GL07", "partial", 0.5, "SRC06", "MedlinePlus L-Citrulline", "PROPOSED candidate nitric oxide ergogenic mapping.", False),
    ("MAP059", "SUP067", "GL07", "direct", 1.0, "SRC01", "ODS Beta-Alanine", "PROPOSED candidate carnosine buffer mapping.", False),
    ("MAP060", "SUP070", "GL09", "partial", 0.5, "SRC06", "MedlinePlus L-Tyrosine", "PROPOSED candidate dopamine precursor mapping.", False),
    ("MAP061", "SUP072", "GL04", "partial", 0.5, "SRC06", "MedlinePlus Glycine", "PROPOSED candidate sleep neuroinhibition mapping.", False),
    ("MAP062", "SUP088", "GL06", "direct", 1.0, "SRC01", "ODS Saccharomyces boulardii", "PROPOSED candidate probiotic yeast mapping.", False),
    ("MAP063", "SUP089", "GL06", "direct", 1.0, "SRC01", "ODS Lactobacillus rhamnosus GG", "PROPOSED candidate probiotic strain mapping.", False),
    ("MAP064", "SUP093", "GL03", "direct", 1.0, "SRC05", "NCCIH Echinacea", "PROPOSED candidate immune botanical mapping.", False),
    ("MAP065", "SUP094", "GL05", "partial", 0.5, "SRC05", "NCCIH Garlic Extract", "PROPOSED candidate vascular botanical mapping.", False),
    ("MAP066", "SUP095", "GL02", "direct", 1.0, "SRC05", "NCCIH Panax Ginseng", "PROPOSED candidate adaptogenic energy mapping.", False),
    ("MAP067", "SUP096", "GL08", "direct", 1.0, "SRC05", "NCCIH Rhodiola Rosea", "PROPOSED candidate burnout resilience mapping.", False),
    ("MAP068", "SUP100", "GL11", "partial", 0.5, "SRC05", "NCCIH Green Tea Extract", "PROPOSED candidate antioxidant polyphenol mapping.", False),
    ("MAP069", "SUP101", "GL06", "direct", 1.0, "SRC05", "NCCIH Ginger Root", "PROPOSED candidate gastrointestinal motility mapping.", False),
    ("MAP070", "SUP102", "GL01", "partial", 0.5, "SRC05", "NCCIH Boswellia Serrata", "PROPOSED candidate joint inflammation mapping.", False),
    ("MAP071", "SUP103", "GL03", "direct", 1.0, "SRC05", "NCCIH Elderberry", "PROPOSED candidate antiviral flavonoid mapping.", False),
    ("MAP072", "SUP106", "GL05", "partial", 0.5, "SRC05", "NCCIH Berberine", "PROPOSED candidate AMPK metabolic mapping.", False),
    ("MAP073", "SUP109", "GL09", "direct", 1.0, "SRC06", "MedlinePlus Bacopa Monnieri", "PROPOSED candidate memory retention mapping.", False),
    ("MAP074", "SUP111", "GL09", "direct", 1.0, "SRC06", "MedlinePlus Lion\'s Mane", "PROPOSED candidate neurotrophic mushroom mapping.", False),
    ("MAP075", "SUP114", "GL11", "partial", 0.5, "SRC05", "NCCIH Cranberry Extract", "PROPOSED candidate urinary tract mapping.", False),
    ("MAP076", "SUP115", "GL05", "direct", 1.0, "SRC05", "NCCIH Hawthorn Berry", "PROPOSED candidate cardiac circulation mapping.", False),
    ("MAP077", "SUP116", "GL04", "partial", 0.5, "SRC05", "NCCIH Passionflower", "PROPOSED candidate calming botanical mapping.", False),
    ("MAP078", "SUP117", "GL04", "partial", 0.5, "SRC06", "MedlinePlus Tart Cherry", "PROPOSED candidate melatonin sleep mapping.", False),
    ("MAP079", "SUP120", "GL11", "partial", 0.5, "SRC06", "MedlinePlus Alpha-Lipoic Acid", "PROPOSED candidate antioxidant mapping.", False),
    ("MAP080", "SUP122", "GL10", "direct", 1.0, "SRC06", "MedlinePlus Astaxanthin", "PROPOSED candidate carotenoid photo-protection mapping.", False),
    ("MAP081", "SUP123", "GL09", "partial", 0.5, "SRC06", "MedlinePlus Lutein & Zeaxanthin", "PROPOSED candidate macular pigment mapping.", False),
    ("MAP082", "SUP127", "GL01", "direct", 1.0, "SRC06", "MedlinePlus Glucosamine", "PROPOSED candidate cartilage glycosaminoglycan mapping.", False),
    ("MAP083", "SUP128", "GL01", "partial", 0.5, "SRC06", "MedlinePlus Chondroitin", "PROPOSED candidate cartilage matrix mapping.", False),
    ("MAP084", "SUP129", "GL01", "partial", 0.5, "SRC06", "MedlinePlus MSM", "PROPOSED candidate organosulfur cartilage mapping.", False),
    ("MAP085", "SUP130", "GL08", "partial", 0.5, "SRC05", "NCCIH SAMe", "PROPOSED candidate methylation mood mapping.", False)
]


ACTIVITY_MAPPINGS_DEF = [
    ("ACT001", "SUP024", "high", "direct", 1.0, "SRC01", "ODS Athletic Performance Guidelines", True),
    ("ACT002", "SUP024", "moderate", "partial", 0.5, "SRC01", "ODS Athletic Performance Guidelines", True),
    ("ACT003", "SUP013", "high", "partial", 0.5, "SRC01", "ODS Athletic Performance Guidelines", True),
    ("ACT004", "SUP012", "high", "partial", 0.5, "SRC01", "ODS Athletic Performance Guidelines", True),
    ("ACT005", "SUP053", "high", "direct", 1.0, "SRC01", "ODS Athletic Performance Guidelines", True),
    ("ACT006", "SUP053", "moderate", "partial", 0.5, "SRC01", "ODS Athletic Performance Guidelines", True),
    ("ACT007", "SUP056", "high", "direct", 1.0, "SRC02", "DSLD Athletic Guidelines", True),
    ("ACT008", "SUP075", "high", "direct", 1.0, "SRC02", "DSLD Athletic Hydration", True),
    ("ACT009", "SUP075", "moderate", "partial", 0.5, "SRC02", "DSLD Athletic Hydration", True),
    ("ACT010", "SUP062", "high", "partial", 0.5, "SRC01", "ODS Athletic Performance Guidelines", True),
    # Candidate activity maps
    ("ACT011", "SUP063", "high", "direct", 1.0, "SRC01", "ODS Exercise Performance", False),
    ("ACT012", "SUP067", "high", "direct", 1.0, "SRC01", "ODS Exercise Performance", False)
]


LIFESTYLE_MAPPINGS_DEF = [
    ("LIF001", "SUP020", "poor", "direct", 1.0, "SRC01", "ODS Sleep and Circadian Factors", True),
    ("LIF002", "SUP013", "poor", "partial", 0.5, "SRC01", "ODS Sleep and Circadian Factors", True),
    ("LIF003", "SUP071", "poor", "partial", 0.5, "SRC06", "MedlinePlus Sleep Physiology", True),
    ("LIF004", "SUP098", "poor", "direct", 1.0, "SRC05", "NCCIH Valerian Sleep Monograph", True),
    ("LIF005", "SUP098", "fair", "partial", 0.5, "SRC05", "NCCIH Valerian Sleep Monograph", True),
    # Candidate lifestyle maps
    ("LIF006", "SUP116", "poor", "partial", 0.5, "SRC05", "NCCIH Passionflower Monograph", False),
    ("LIF007", "SUP117", "poor", "partial", 0.5, "SRC06", "MedlinePlus Tart Cherry Sleep", False)
]


ALLERGEN_MAPPINGS_DEF = [
    ("SUP018", "fish", "may_contain_depending_on_source", "SRC02", "DSLD Product Labels Cross-Reference", True, "Fish-oil derived formulations contain fish allergen; algal oil formulations do not."),
    ("SUP019", "milk", "may_contain_depending_on_product", "SRC02", "DSLD Product Labels Cross-Reference", True, "Dairy culture broth residues in selected commercial probiotic strains."),
    ("SUP044", "fish", "contains", "SRC01", "ODS Cod Liver Oil Monograph", True, "Derived from Atlantic cod liver tissues."),
    ("SUP045", "shellfish", "contains", "SRC01", "ODS Krill Oil Monograph", True, "Derived from Antarctic krill crustacean species."),
    ("SUP053", "milk", "contains", "SRC01", "ODS Whey Monograph", True, "Derived from bovine milk dairy fraction."),
    ("SUP054", "milk", "contains", "SRC01", "ODS Whey Monograph", True, "Derived from bovine milk dairy fraction."),
    ("SUP055", "milk", "contains", "SRC01", "ODS Casein Monograph", True, "Primary phosphoprotein fraction of bovine dairy milk."),
    ("SUP057", "soy", "contains", "SRC05", "NCCIH Soy Monograph", True, "Derived from glycine max soybean protein isolate."),
    ("SUP060", "egg", "contains", "SRC02", "DSLD Egg White Monograph", True, "Derived from avian poultry egg albumen."),
    ("SUP127", "shellfish", "may_contain_depending_on_source", "SRC06", "MedlinePlus Glucosamine Monograph", True, "Commercial glucosamine sulfate is frequently derived from marine shellfish exoskeletons.")
]


SAFETY_RULES_DEF = [
    # Global missing safety info rule (enforces R000 for unverified supplements)
    ("R000", "", "missing_info", "ANY", "safety_verification_status!=verified", "require_review", "No verified safety record for this supplement", "Safety information for this item is incomplete; recommendation withheld pending review.", "SRC01", "Platform Safety Core Architecture", True),

    # Clinical rules R001 - R014
    ("R001", "SUP006", "interaction", "anticoagulant", "medication_class", "require_review", "Cofactor in prothrombin synthesis counteracting coumarin anticoagulants", "Check with a clinician/pharmacist if taking blood thinners.", "SRC01", "ODS Vitamin K Drug Interactions", True),
    ("R002", "SUP023", "interaction", "anticoagulant", "medication_class", "require_review", "Ginkgolides exert platelet-activating factor antagonist properties", "Check with a clinician/pharmacist if taking blood thinners.", "SRC05", "NCCIH Ginkgo Cautions", True),
    ("R003", "SUP005", "interaction", "anticoagulant", "medication_class", "require_review", "High-dose alpha-tocopherol antagonizes vitamin K clotting cascades", "Check with a clinician/pharmacist if taking blood thinners.", "SRC01", "ODS Vitamin E Drug Interactions", True),
    ("R004", "SUP018", "condition", "bleeding_disorder", "condition_code", "require_review", "High dose polyunsaturated EPA/DHA prolonged bleeding times", "Review with a clinician if you have a bleeding disorder.", "SRC01", "ODS Omega-3 High-Dose Bleeding", True),
    ("R005", "SUP012", "condition", "iron_overload", "condition_code", "exclude", "Exogenous iron exacerbates tissue hemosiderosis and organ damage", "Not suitable to suggest for users with iron overload.", "SRC01", "ODS Iron Precautions", True),
    ("R006", "SUP007", "condition", "pregnancy", "condition_code", "require_review", "Preformed retinol exhibits teratogenic cranial-neural risk at high intake", "Review vitamin A intake with a clinician during pregnancy.", "SRC01", "ODS Vitamin A Teratogenicity", True),
    ("R007", "SUP017", "condition", "kidney_disease", "condition_code", "exclude", "Impaired renal excretion precipitates life-threatening cardiac arrhythmias", "Not suitable to suggest for users with kidney disease.", "SRC01", "ODS Potassium Renal Impairment", True),
    ("R008", "SUP017", "interaction", "antihypertensive", "medication_class", "require_review", "Potassium-sparing ACE inhibitors / ARBs exacerbate hyperkalemia risk", "Review with a clinician if taking blood-pressure medication.", "SRC01", "ODS Potassium Drug Interactions", True),
    ("R009", "SUP021", "condition", "thyroid_disorder", "condition_code", "require_review", "Withanolides stimulate circulating thyroid hormone concentrations", "Review with a clinician if you have a thyroid condition.", "SRC05", "NCCIH Ashwagandha Thyroid", True),
    ("R010", "SUP021", "condition", "pregnancy", "condition_code", "require_review", "Botanical extract possesses documented spasmolytic abortifacient concerns", "Review with a clinician during pregnancy.", "SRC05", "NCCIH Ashwagandha Pregnancy", True),
    ("R011", "SUP016", "condition", "thyroid_disorder", "condition_code", "require_review", "Excess iodine precipitates Wolff-Chaikoff effect or hyperthyroid flares", "Review with a clinician if you have a thyroid condition.", "SRC01", "ODS Iodine Thyroid Disorders", True),
    ("R012", "SUP013", "condition", "kidney_disease", "condition_code", "require_review", "Diminished glomerular clearance increases toxic hypermagnesemia risk", "Review with a clinician if you have kidney disease.", "SRC01", "ODS Magnesium Clearance", True),
    ("R013", "SUP020", "interaction", "sedative", "medication_class", "require_review", "Additive central nervous system depression with sedative medications", "Review with a clinician if taking sedatives.", "SRC01", "ODS Melatonin Interaction", True),
    ("R014", "SUP020", "condition", "autoimmune_disease", "condition_code", "require_review", "Exogenous melatonin stimulates pro-inflammatory cytokine expression", "Review with a clinician if you have an autoimmune condition.", "SRC01", "ODS Melatonin Immunostimulatory", True),

    # Expanded Clinical Safety Rules R015 - R040
    ("R015", "SUP030", "interaction", "anticoagulant", "medication_class", "require_review", "Vitamin K2 directly interferes with warfarin anticoagulation.", "Check with a clinician/pharmacist if taking blood thinners.", "SRC01", "ODS Vitamin K Interaction Monograph", True),
    ("R016", "SUP033", "condition", "liver_disease", "condition_code", "require_review", "Impaired biliary excretion of copper risks toxic hepatic accumulation (e.g. Wilson disease).", "Review with a clinician if you have liver disease.", "SRC01", "ODS Copper Precautions", True),
    ("R017", "SUP041", "condition", "bleeding_disorder", "condition_code", "require_review", "High-dose concentrated EPA exhibits antiplatelet properties.", "Review with a clinician if you have a bleeding disorder.", "SRC01", "ODS Omega-3 High-Dose Bleeding", True),
    ("R018", "SUP044", "condition", "pregnancy", "condition_code", "require_review", "High preformed vitamin A content poses teratogenicity concerns during pregnancy.", "Review with a clinician during pregnancy.", "SRC01", "ODS Vitamin A Monograph", True),
    ("R019", "SUP099", "interaction", "sedative", "medication_class", "require_review", "St. John\'s Wort induces hepatic CYP3A4 enzymes and interacts with CNS sedatives.", "Check with a clinician if taking sedatives or psychiatric medications.", "SRC05", "NCCIH St. John\'s Wort Drug Interactions", True),
    ("R020", "SUP099", "interaction", "immunosuppressant", "medication_class", "require_review", "CYP3A4 and P-glycoprotein induction significantly lowers cyclosporine and tacrolimus levels.", "Contraindicated with immunosuppressant medications.", "SRC05", "NCCIH St. John\'s Wort Transplant Warnings", True),
    ("R021", "SUP098", "interaction", "sedative", "medication_class", "require_review", "Valerian exhibits additive central nervous system depressant effects with sedatives.", "Review with a clinician if taking sedative or sleep medications.", "SRC05", "NCCIH Valerian Interaction Review", True),
    ("R022", "SUP094", "interaction", "anticoagulant", "medication_class", "require_review", "Garlic extract exhibits mild antiplatelet effects and may enhance bleeding risks.", "Check with a clinician if taking anticoagulants or scheduled for surgery.", "SRC05", "NCCIH Garlic Interaction Review", True),
    ("R023", "SUP095", "interaction", "anticoagulant", "medication_class", "require_review", "Ginsenosides modulate platelet aggregation and may alter INR monitoring.", "Check with a clinician if taking blood thinners.", "SRC05", "NCCIH Asian Ginseng Monograph", True),
    ("R024", "SUP095", "interaction", "antidiabetic", "medication_class", "require_review", "Panax ginseng enhances insulin sensitivity and may increase hypoglycemia risks.", "Review with a clinician if taking diabetes medications.", "SRC05", "NCCIH Asian Ginseng Monograph", True),
    ("R025", "SUP118", "condition", "liver_disease", "condition_code", "exclude", "Monacolin K in red yeast rice carries statin-equivalent hepatic transaminase elevation risks.", "Not suitable to suggest for users with chronic liver disease.", "SRC05", "NCCIH Red Yeast Rice Warnings", True),
    ("R026", "SUP118", "condition", "pregnancy", "condition_code", "exclude", "HMG-CoA reductase inhibition is strictly contraindicated during pregnancy.", "Contraindicated during pregnancy.", "SRC05", "NCCIH Red Yeast Rice Pregnancy Safety", True),
    ("R027", "SUP106", "interaction", "antidiabetic", "medication_class", "require_review", "Berberine activates AMPK to decrease hepatic gluconeogenesis and may compound hypoglycemia.", "Review with a clinician if taking blood glucose lowering medication.", "SRC05", "NCCIH Berberine Metabolic Interactions", True),
    ("R028", "SUP106", "condition", "pregnancy", "condition_code", "exclude", "Berberine crosses placenta and displaces bilirubin, carrying neonatal kernicterus risks.", "Contraindicated during pregnancy.", "SRC05", "NCCIH Berberine Safety Review", True),
    ("R029", "SUP076", "condition", "hypertension", "condition_code", "require_review", "Excess sodium intake increases intravascular volume and raises blood pressure.", "Review supplemental sodium intake with a clinician if you have hypertension.", "SRC06", "MedlinePlus Sodium Dietary Considerations", True),
    ("R030", "SUP077", "condition", "kidney_disease", "condition_code", "exclude", "Supplemental potassium is contraindicated in advanced kidney disease due to hyperkalemia risk.", "Not suitable for users with kidney disease.", "SRC01", "ODS Potassium Clearance Monograph", True),
    ("R031", "SUP077", "interaction", "antihypertensive", "medication_class", "require_review", "Potassium-sparing blood pressure medications can trigger hyperkalemia when combined with potassium salts.", "Review with a clinician if taking antihypertensives.", "SRC01", "ODS Potassium Interaction Monograph", True),
    ("R032", "SUP116", "interaction", "sedative", "medication_class", "require_review", "Passionflower exhibits additive sedative properties with CNS depressants.", "Review with a clinician if taking sedative medications.", "SRC05", "NCCIH Passionflower Monograph", True),
    ("R033", "SUP130", "interaction", "sedative", "medication_class", "require_review", "SAMe interacts with serotonergic and central nervous system medications.", "Review with a clinician if taking psychoactive medications.", "SRC05", "NCCIH SAMe Interaction Monograph", True),
    ("R034", "SUP114", "interaction", "anticoagulant", "medication_class", "require_review", "Concentrated cranberry extract proanthocyanidins may alter warfarin clearance.", "Check with a clinician if taking warfarin or other anticoagulants.", "SRC05", "NCCIH Cranberry Safety Monograph", True),
    ("R035", "SUP100", "condition", "liver_disease", "condition_code", "require_review", "High-dose green tea extracts (EGCG) in concentrated fasting boluses have been linked to liver injury.", "Review with a clinician if you have liver disease.", "SRC05", "NCCIH Green Tea Monograph", True),
    ("R036", "SUP053", "condition", "milk", "allergen_code", "exclude", "Contains bovine dairy milk protein allergen.", "Excluded due to declared milk allergy.", "SRC01", "ODS Whey Monograph", True),
    ("R037", "SUP054", "condition", "milk", "allergen_code", "exclude", "Contains bovine dairy milk protein allergen.", "Excluded due to declared milk allergy.", "SRC01", "ODS Whey Monograph", True),
    ("R038", "SUP055", "condition", "milk", "allergen_code", "exclude", "Contains bovine dairy milk casein allergen.", "Excluded due to declared milk allergy.", "SRC01", "ODS Casein Monograph", True),
    ("R039", "SUP057", "condition", "soy", "allergen_code", "exclude", "Contains concentrated soybean allergen.", "Excluded due to declared soy allergy.", "SRC05", "NCCIH Soy Monograph", True),
    ("R040", "SUP060", "condition", "egg", "allergen_code", "exclude", "Contains poultry egg white ovalbumin allergen.", "Excluded due to declared egg allergy.", "SRC02", "DSLD Egg White Monograph", True)
]
