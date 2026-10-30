-- PostgreSQL / Supabase schema (v0.1-draft). Import order = order below.
CREATE TABLE sources(source_id text PRIMARY KEY, source_name text NOT NULL, source_type text, url text, access_method text, reuse_note text, limitations text);
CREATE TABLE goals(goal_id text PRIMARY KEY, goal_code text UNIQUE NOT NULL, goal_name text NOT NULL, description text, is_active boolean NOT NULL DEFAULT true);
CREATE TABLE diets(diet_code text PRIMARY KEY, diet_name text, description text);
CREATE TABLE allergens(allergen_code text PRIMARY KEY, allergen_name text);
CREATE TABLE conditions(condition_code text PRIMARY KEY, condition_name text, in_scope_note text);
CREATE TABLE medication_classes(medclass_code text PRIMARY KEY, medclass_name text, note text);
CREATE TABLE activity_levels(activity_code text PRIMARY KEY, activity_name text, ordinal int);
CREATE TABLE sleep_categories(sleep_code text PRIMARY KEY, sleep_name text, ordinal int);
CREATE TABLE supplements(supplement_id text PRIMARY KEY, supplement_name text UNIQUE NOT NULL, supplement_category text NOT NULL, description text, active_ingredients text, ingredient_forms text,
  primary_source_id text REFERENCES sources, source_url text,
  verification_status text NOT NULL CHECK (verification_status IN ('verified','needs_review','unknown','not_applicable','rejected')),
  last_reviewed_at date, is_active boolean NOT NULL DEFAULT true, created_at date, updated_at date, notes text);
CREATE TABLE supplement_goal_map(mapping_id text PRIMARY KEY, supplement_id text NOT NULL REFERENCES supplements, goal_id text NOT NULL REFERENCES goals,
  match_type text NOT NULL CHECK (match_type IN ('direct','partial','none')), match_score numeric(3,2) NOT NULL CHECK (match_score IN (0,0.5,1)),
  source_id text REFERENCES sources, source_ref text, evidence_notes text, verification_status text NOT NULL, rule_version text NOT NULL, is_active boolean NOT NULL DEFAULT false,
  UNIQUE (supplement_id, goal_id, rule_version));
CREATE TABLE supplement_activity_map(map_id text PRIMARY KEY, supplement_id text NOT NULL REFERENCES supplements, activity_code text NOT NULL REFERENCES activity_levels,
  match_type text NOT NULL, match_score numeric(3,2) NOT NULL, source_id text REFERENCES sources, source_ref text, verification_status text NOT NULL, rule_version text, is_active boolean NOT NULL DEFAULT false);
CREATE TABLE supplement_lifestyle_map(map_id text PRIMARY KEY, supplement_id text NOT NULL REFERENCES supplements, sleep_code text NOT NULL REFERENCES sleep_categories,
  match_type text NOT NULL, match_score numeric(3,2) NOT NULL, source_id text REFERENCES sources, source_ref text, verification_status text NOT NULL, rule_version text, is_active boolean NOT NULL DEFAULT false);
CREATE TABLE supplement_diet_compat(supplement_id text REFERENCES supplements, diet_code text REFERENCES diets,
  compat_status text NOT NULL CHECK (compat_status IN ('compatible','incompatible','depends_on_product','unknown')),
  source_id text REFERENCES sources, source_ref text, verification_status text NOT NULL, last_reviewed_at date, notes text, PRIMARY KEY (supplement_id, diet_code));
CREATE TABLE supplement_allergen(supplement_id text REFERENCES supplements, allergen_code text REFERENCES allergens, relation text,
  source_id text REFERENCES sources, source_ref text, verification_status text NOT NULL, is_active boolean NOT NULL DEFAULT false, notes text, PRIMARY KEY (supplement_id, allergen_code));
CREATE TABLE safety_rules(rule_id text PRIMARY KEY, supplement_id text REFERENCES supplements, -- NULL = global rule
  rule_type text NOT NULL CHECK (rule_type IN ('allergy','dietary','condition','interaction','missing_info')), condition_code text NOT NULL, triggering_attribute text,
  action text NOT NULL CHECK (action IN ('exclude','require_review','warn')), reason text, safety_message text NOT NULL,
  source_id text REFERENCES sources, source_ref text, verification_status text NOT NULL, rule_version text NOT NULL, is_active boolean NOT NULL DEFAULT false);
CREATE TABLE scoring_config(criterion_id text PRIMARY KEY, criterion_code text UNIQUE NOT NULL, criterion_name text, weight numeric(4,3) NOT NULL CHECK (weight BETWEEN 0 AND 1),
  minimum_value numeric NOT NULL DEFAULT 0, maximum_value numeric NOT NULL DEFAULT 1, description text, rule_version text, is_active boolean NOT NULL DEFAULT true);
CREATE TABLE criterion_value_rules(rule_id text PRIMARY KEY, criterion_code text REFERENCES scoring_config(criterion_code), condition text, value numeric(3,2) CHECK (value BETWEEN 0 AND 1), note text, rule_version text);
CREATE TABLE system_config(config_key text PRIMARY KEY, config_value text NOT NULL, description text, rule_version text);
CREATE TABLE explanation_templates(template_id text PRIMARY KEY, criterion_code text NOT NULL, match_value text, template_text text NOT NULL, required_attribute text, rule_version text, is_active boolean DEFAULT true);

-- ---- Application tables (NOT populated from CSV) ----
CREATE TABLE user_profiles(profile_id uuid PRIMARY KEY DEFAULT gen_random_uuid(), user_id uuid NOT NULL, birth_year int, goals text[], dietary_preference text REFERENCES diets,
  allergies text[], existing_conditions text[], current_medication_classes text[],  -- needed for interaction checks
  activity_level text REFERENCES activity_levels, sleep_quality text REFERENCES sleep_categories, average_sleep_hours numeric(3,1),
  previous_supplement_usage jsonb, reported_reactions jsonb, profile_completed boolean DEFAULT false, created_at timestamptz DEFAULT now(), updated_at timestamptz DEFAULT now());
CREATE TABLE recommendation_runs(run_id uuid PRIMARY KEY DEFAULT gen_random_uuid(), user_id uuid NOT NULL, profile_id uuid NOT NULL REFERENCES user_profiles,
  profile_snapshot jsonb NOT NULL,   -- frozen copy => reproducible history
  threshold_value numeric NOT NULL, dataset_version text NOT NULL, rule_version text NOT NULL, scoring_version text NOT NULL,
  run_status text NOT NULL CHECK (run_status IN ('completed','withheld_incomplete_safety','no_eligible_results')), created_at timestamptz DEFAULT now());
CREATE TABLE recommendation_results(recommendation_id uuid PRIMARY KEY DEFAULT gen_random_uuid(), run_id uuid NOT NULL REFERENCES recommendation_runs, supplement_id text NOT NULL,
  eligibility_status text NOT NULL CHECK (eligibility_status IN ('eligible','below_threshold','excluded_safety','needs_review')),
  goal_match_score numeric, diet_match_score numeric, activity_match_score numeric, lifestyle_match_score numeric, history_match_score numeric,
  weighted_contributions jsonb, final_score numeric, rank_position int, explanation jsonb, safety_summary jsonb, created_at timestamptz DEFAULT now());
