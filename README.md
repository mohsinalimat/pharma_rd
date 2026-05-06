# Pharma R&D — Frappe v15+ Application
## Complete Technical Documentation

---

## Table of Contents

1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Installation & Setup](#installation--setup)
4. [Module Structure](#module-structure)
5. [DocTypes Reference](#doctypes-reference)
6. [Reports](#reports)
7. [Workspace](#workspace)
8. [Notifications](#notifications)
9. [Scheduled Tasks](#scheduled-tasks)
10. [Roles & Permissions](#roles--permissions)
11. [Client Scripts](#client-scripts)
12. [Git Structure](#git-structure)
13. [Customisation Guide](#customisation-guide)
14. [Troubleshooting](#troubleshooting)

---

## Overview

**pharma_rd** is a production-ready Frappe v15+ custom application for Research & Pharmaceutical Development organisations. It provides end-to-end lifecycle management from early drug discovery through regulatory approval.

### Core Capabilities

| Domain | Features |
|---|---|
| Research | Project management, milestones, team tracking, budget |
| Drug Discovery | Compound tracking, Lipinski analysis, target biology |
| Clinical Operations | Trial management, site tracking, enrollment, SAEs |
| Manufacturing | Batch manufacturing records, formula, process steps |
| Quality Control | Test management, OOS alerts, pass/fail tracking |
| Stability | ICH-compliant stability study and timepoint management |
| Regulatory Affairs | Multi-agency submission tracking, correspondence log |
| Lab Operations | Equipment calibration tracking, qualification status |

---

## Architecture

```
frappe-bench/
└── apps/
    └── pharma_rd/                        ← App root
        ├── setup.py
        ├── requirements.txt
        ├── MANIFEST.in
        ├── .gitignore
        └── pharma_rd/                    ← Python package
            ├── __init__.py
            ├── hooks.py                  ← App hooks & scheduler config
            ├── tasks.py                  ← Scheduled task functions
            ├── boot.py                   ← Boot session injection
            ├── doctype/                  ← DocType definitions
            │   ├── research_project/
            │   ├── drug_candidate/
            │   ├── clinical_trial/
            │   ├── batch_manufacturing_record/
            │   ├── qc_test/
            │   ├── stability_study/
            │   ├── regulatory_submission/
            │   ├── lab_equipment/
            │   ├── biological_target/
            │   ├── therapeutic_area/
            │   └── [child doctypes]/
            ├── report/                   ← Script reports
            │   ├── research_project_summary/
            │   ├── clinical_trial_status/
            │   └── qc_test_results_summary/
            ├── workspace/                ← Module workspace
            │   └── pharma_rd_workspace/
            ├── notification/             ← Email notifications
            │   ├── calibration_due_alert/
            │   ├── clinical_trial_milestone_alert/
            │   ├── qc_test_fail_alert/
            │   └── regulatory_submission_approved/
            ├── print_format/             ← Print templates
            │   └── research_project_summary_print/
            ├── fixtures/                 ← Seed data
            │   ├── roles.json
            │   └── therapeutic_areas.json
            └── public/                   ← Frontend assets
                ├── css/pharma_rd.css
                └── js/pharma_rd.js
```

---

## Installation & Setup

### Prerequisites

| Requirement | Version |
|---|---|
| Frappe Framework | v15.x |
| Python | 3.10+ |
| Node.js | 18+ |
| MariaDB | 10.6+ |

### Step 1 — Get the App

```bash
cd ~/frappe-bench
bench get-app https://github.com/balaji-001-gif/research_pharma.git
# OR for local development:
bench get-app pharma_rd /path/to/pharma_rd
```

### Step 2 — Install on Site

```bash
bench --site your-site.local install-app pharma_rd
```

### Step 3 — Run Migrations

```bash
bench --site your-site.local migrate
```

### Step 4 — Build Assets

```bash
bench build --app pharma_rd
bench --site your-site.local clear-cache
```

### Step 5 — Import Fixtures (Roles + Seed Data)

```bash
bench --site your-site.local import-fixtures --app pharma_rd
```

### Step 7 — Import Demo Data (Optional)

```bash
bench --site your-site.local execute pharma_rd.setup_demo_data.create_demo_data
```

### Step 8 — Restart

```bash
bench restart
```

### Development Setup

```bash
# Clone for development
cd ~/frappe-bench/apps
git clone https://github.com/balaji-001-gif/research_pharma.git
pip install -e pharma_rd

# Watch mode for assets
bench watch

# Run tests
bench --site your-site.local run-tests --app pharma_rd
```

---

## Module Structure

### hooks.py — Key Registrations

```python
# Document Events
doc_events = {
    "Research Project": {
        "on_submit": "pharma_rd.pharma_rd.doctype.research_project...",
        "on_cancel": "pharma_rd.pharma_rd.doctype.research_project...",
    },
    "Clinical Trial":             {"on_submit": "..."},
    "Batch Manufacturing Record": {"on_submit": "..."},
}

# Scheduled Tasks
scheduler_events = {
    "daily":  ["check_expiry_alerts", "check_trial_milestones"],
    "weekly": ["generate_stability_alerts"],
}
```

---

## DocTypes Reference

### 1. Research Project

**Purpose:** Central hub for managing R&D projects from inception to completion.

**Key Fields:**

| Field | Type | Description |
|---|---|---|
| project_code | Data (unique) | Auto-generated project identifier |
| project_title | Data | Full project name |
| therapeutic_area | Link → Therapeutic Area | Disease/therapy category |
| drug_modality | Select | Small Molecule, Biologic, Cell Therapy, etc. |
| research_phase | Select | Target ID → Phase III → Registration |
| status | Select | Draft / Active / On Hold / Completed / Cancelled |
| principal_investigator | Link → User | Lead scientist |
| start_date / end_date | Date | Project timeline |
| budget / spent_budget | Currency | Financial tracking |
| team_members | Table | Linked researchers with FTE% |
| milestones | Table | Milestone tracking with status |

**Workflow:** Draft → Active → Completed (submitted)

**Server-side logic:**
- Auto-generates project_code if not provided
- Validates start_date < end_date
- On submit: flags in-progress milestones as "In Progress"

**Linked DocTypes:** Drug Candidate, Clinical Trial, Stability Study, Regulatory Submission

---

### 2. Drug Candidate

**Purpose:** Tracks compounds from hit identification through development candidate selection.

**Key Fields:**

| Field | Type | Description |
|---|---|---|
| compound_id | Data (unique) | Auto-generated (e.g. PROJ-0001) |
| compound_name | Data | Common/lab name |
| research_project | Link → Research Project | Parent project |
| development_stage | Select | Hit → Lead → Optimized → DC → Preclinical → Clinical |
| iupac_name | Small Text | IUPAC systematic name |
| molecular_formula | Data | Empirical formula |
| molecular_weight | Float | MW in Daltons |
| cas_number | Data | CAS registry number |
| smiles | Small Text | SMILES string |
| logp | Float | Lipophilicity |
| psa | Float | Polar surface area (Å²) |
| hbd / hba | Int | H-bond donors/acceptors |
| target | Link → Biological Target | Primary molecular target |
| ic50 / ec50 | Float | Potency (nM) |
| bioavailability | Percent | Oral bioavailability |
| half_life | Float | Elimination half-life (h) |
| patent_status | Select | IP filing status |
| ip_expiry_date | Date | Patent expiry |

**Server-side logic:**
- Lipinski Rule-of-5 validation with warning on violations
- Auto-generates compound_id based on project prefix

---

### 3. Clinical Trial

**Purpose:** Full lifecycle management of clinical studies from design to completion.

**Key Fields:**

| Field | Type | Description |
|---|---|---|
| trial_id | Data (unique) | Auto-generated (e.g. PhaseII-0001) |
| trial_phase | Select | Phase I through Phase IV |
| status | Select | Draft → Planning → Active → Completed |
| drug_candidate | Link → Drug Candidate | Investigational drug |
| study_design | Select | RCT, Open Label, Crossover, etc. |
| primary_endpoint | Small Text | Primary efficacy endpoint |
| planned_enrollment | Int | Target sample size |
| actual_enrollment | Int | Enrolled to date |
| irb_approval | Check | Ethics board approval |
| irb_number | Data | Protocol reference |
| sites | Table | Clinical site breakdown |
| saes | Int | Serious adverse event count |
| nct_number | Data | ClinicalTrials.gov identifier |

**Server-side logic:**
- Blocks status "Active" without IRB approval
- On submit: notifies Regulatory Affairs Officers via email
- Auto-generates trial_id from phase abbreviation + sequence

**Child DocType — Clinical Trial Site:**

| Field | Description |
|---|---|
| site_name / site_code | Site identifier |
| country | Link → Country |
| pi_name | Site principal investigator |
| target_patients / enrolled | Enrollment tracking |
| site_status | Not Initiated → Initiated → Enrolling → Closed |

---

### 4. Batch Manufacturing Record (BMR)

**Purpose:** GMP-compliant batch records for R&D and clinical manufacturing.

**Key Fields:**

| Field | Type | Description |
|---|---|---|
| batch_no | Data (unique) | Auto-generated (BMR-000001) |
| drug_candidate | Link → Drug Candidate | Product |
| batch_type | Select | R&D / Pilot / Scale-Up / Validation / Clinical |
| batch_size + unit | Float + Select | Quantity (g, mg, kg, mL, L) |
| manufacture_date | Date | Date of manufacture |
| expiry_date | Date | Shelf-life date |
| batch_status | Select | Draft → In Process → Pending QC → Passed/Failed → Released |
| qc_status | Select | Auto-updated by QC Tests |
| batch_formula | Table | Ingredient list with actuals |
| process_steps | Table | Step-by-step manufacturing log |

**Child: BMR Formula Line** — Ingredients, grade, quantity planned vs actual, lot numbers

**Child: BMR Process Step** — Step number, operation, performer, start/end time, parameters, observations

---

### 5. QC Test

**Purpose:** Individual quality control test records linked to batches.

**Key Fields:**

| Field | Type | Description |
|---|---|---|
| test_id | Data (unique) | Auto-generated (QCT-000001) |
| test_type | Select | Identity, Assay, Purity, Sterility, Dissolution, etc. |
| batch_no | Link → BMR | Tested batch |
| test_method | Data | SOP reference |
| instrument | Link → Lab Equipment | Instrument used |
| analyst | Link → User | Testing analyst |
| specification | Small Text | Acceptance criteria |
| result_value | Data | Test result |
| pass_fail | Select | Pass / Fail |
| oos_reference | Data | OOS investigation reference |

**Server-side logic:**
- Sets batch QC status when test is submitted
- Triggers OOS alert message on fail
- Status auto-set from pass_fail field

---

### 6. Stability Study

**Purpose:** ICH Q1A(R2) compliant stability program management.

**Key Fields:**

| Field | Type | Description |
|---|---|---|
| study_id | Data (unique) | Auto-generated (STB-00001) |
| study_type | Select | Long-Term / Intermediate / Accelerated / Stress / Photo |
| ich_guideline | Select | Q1A(R2), Q1B, Q1C, Q1D, Q1E, Q1F |
| temperature | Data | Storage temperature (°C) |
| humidity | Data | Relative humidity (%RH) |
| timepoints | Table | Stability timepoint records |
| shelf_life_months | Int | Proposed shelf life |
| storage_statement | Small Text | e.g. "Store at 25°C/60%RH" |

**Child: Stability Timepoint** — target date, actual date, assay %, impurities %, appearance, pH, pass/fail

---

### 7. Regulatory Submission

**Purpose:** Track all regulatory interactions from IND through post-market.

**Key Fields:**

| Field | Type | Description |
|---|---|---|
| submission_id | Data (unique) | Auto-generated (FDA-IND-0001) |
| submission_type | Select | IND, NDA, BLA, ANDA, MAA, CTA, IMPD, DMF |
| regulatory_agency | Select | FDA, EMA, HPRA, PMDA, Health Canada, TGA, etc. |
| status | Select | Draft → Internal Review → Submitted → Under Review → Approved |
| nct_number | Data | Trial registry number |
| pdufa_date | Date | Target action date (FDA) |
| decision_date | Date | Agency decision |
| approval_number | Data | Granted approval number |
| correspondence | Table | Full agency correspondence log |

---

### 8. Lab Equipment

**Purpose:** Track laboratory instruments with calibration and qualification status.

**Key Fields:**

| Field | Type | Description |
|---|---|---|
| equipment_id | Data (unique) | Instrument identifier |
| equipment_type | Select | Analytical, Synthesis, Biological, Safety, Storage |
| make / model / serial_number | Data | Instrument details |
| status | Select | Operational / Under Maintenance / Calibration Due / Out of Service |
| last_calibration | Date | Most recent calibration |
| calibration_due | Date | Next calibration required by |
| calibration_frequency | Select | Monthly → Annual |
| qualification_status | Select | IQ / OQ / PQ complete |

---

### Master DocTypes

**Therapeutic Area** — Disease/therapy category master list (seeded with 10 areas)

**Biological Target** — Molecular target registry with UniProt ID, gene name, target class (GPCR, Kinase, etc.)

---

## Reports

### 1. Research Project Summary

**Type:** Script Report | **Ref DocType:** Research Project

**Filters:** Status, Therapeutic Area, From Date, To Date

**Columns:** Project Code, Title, Therapeutic Area, Phase, Status, Priority, Start Date, End Date, Budget, Spent, PI, Milestones, Completed Milestones

**Visuals:** Donut chart by status | Summary row: Total Projects, Active, Total Budget, Total Spent

**Usage:** Management dashboard, portfolio review

---

### 2. Clinical Trial Status

**Type:** Script Report | **Ref DocType:** Clinical Trial

**Filters:** Status, Trial Phase

**Columns:** Trial ID, Title, Phase, Status, Drug, Planned N, Enrolled N, Enrollment %, Start, Primary Completion, NCT Number, IRB, SAEs

**Visuals:** Bar chart by phase | Summary: Total, Active, Total SAEs

---

### 3. QC Test Results Summary

**Type:** Script Report | **Ref DocType:** QC Test

**Filters:** Batch No, Pass/Fail, From Date, To Date

**Columns:** Test ID, Name, Type, Batch, Analyst, Date, Result, Specification, Pass/Fail, Status

---

## Workspace

**Name:** Pharma R&D  
**Icon:** lab | **Public:** Yes

### Quick-access Shortcuts (top bar)

Research Project, Drug Candidate, Clinical Trial, Batch Mfg Record, QC Test, Stability Study, Regulatory Submission, Lab Equipment, Project Summary Report, Clinical Trial Status Report

### Card Layout

| Card | Links |
|---|---|
| Research | Research Project, Drug Candidate, Biological Target, Therapeutic Area |
| Clinical | Clinical Trial |
| Quality | QC Test, Stability Study |
| Manufacturing | Batch Manufacturing Record, Lab Equipment |
| Regulatory | Regulatory Submission |
| Masters | Therapeutic Area, Biological Target |
| Analytics | All 3 Reports |

---

## Notifications

### 1. Calibration Due Alert

| Setting | Value |
|---|---|
| DocType | Lab Equipment |
| Event | Days Before calibration_due |
| Days in Advance | 14 |
| Condition | `doc.status == 'Operational'` |
| Recipients | Role: Lab Manager |

### 2. Clinical Trial Status Change

| Setting | Value |
|---|---|
| DocType | Clinical Trial |
| Event | Change (status field) |
| Recipients | Clinical Trial Manager + Regulatory Affairs Officer |

### 3. QC Test Failure Alert

| Setting | Value |
|---|---|
| DocType | QC Test |
| Event | Change (pass_fail field) |
| Condition | `doc.pass_fail == 'Fail'` |
| Recipients | QC Analyst + Lab Manager + Pharma Admin |

### 4. Regulatory Submission Approved

| Setting | Value |
|---|---|
| DocType | Regulatory Submission |
| Event | Change (status field) |
| Condition | `doc.status == 'Approved'` |
| Recipients | Regulatory Affairs Officer + Pharma Admin |

---

## Scheduled Tasks

| Task | Frequency | Action |
|---|---|---|
| check_expiry_alerts | Daily | Email Lab Managers about batches expiring within 30 days |
| check_trial_milestones | Daily | Auto-update trials past primary completion to "Data Collection" |
| generate_stability_alerts | Weekly | Email QC Analysts about stability timepoints due within 7 days |

---

## Roles & Permissions

| Role | Research Project | Drug Candidate | Clinical Trial | BMR | QC Test | Stability | Regulatory | Lab Equipment |
|---|---|---|---|---|---|---|---|---|
| Pharma Admin | Full | Full | Full | Full | Full | Full | Full | Full |
| Pharma Researcher | Read/Write/Submit | Read/Write/Submit | Read | — | — | — | Read | — |
| Clinical Trial Manager | Read | Read | Read/Write/Submit | — | — | — | Read/Write | — |
| QC Analyst | — | Read | — | Read/Write | Read/Write/Submit | Read/Write/Submit | — | Read |
| Regulatory Affairs Officer | Read | Read | Read/Write | — | — | — | Read/Write/Submit | — |
| Lab Manager | Read/Write | Read | — | Read/Write/Submit | Read/Write/Submit | Read/Write | — | Read/Write/Create |

---

## Client Scripts

### pharma_rd.js (global)

```javascript
pharma_rd.colour_status_badge(frm)   // Colour-code status indicator
pharma_rd.format_compact_currency(v) // "1.5M", "250K"
pharma_rd.check_lipinski(frm)        // Lipinski Rule-of-5 dashboard alert
```

### Research Project JS

- Progress bar for milestone completion percentage
- Budget utilisation percentage with colour coding (red >90%, orange >70%)
- Quick-action buttons: View Drug Candidates, View Clinical Trials, Add Compound

### Drug Candidate JS

- Triggers Lipinski check on molecular property field changes
- "Lipinski Check" button on form
- "Create Stability Study" quick action

### Clinical Trial JS

- Enrollment progress bar (actual / planned)
- Blocks status "Active" without IRB approval (client-side warning)
- "View Regulatory Submissions" navigation button

### QC Test JS

- Colour-codes pass/fail indicator instantly
- Shows OOS investigation alert message on Fail

---

## Git Structure

```
pharma_rd/
├── .github/
│   └── workflows/
│       └── ci.yml          ← GitHub Actions CI (flake8 lint)
├── .gitignore
├── setup.py
├── requirements.txt
├── MANIFEST.in
└── pharma_rd/
    ├── __init__.py
    ├── hooks.py
    ├── tasks.py
    ├── boot.py
    ├── doctype/            ← Each doctype: __init__.py + .json + .py + .js
    ├── report/             ← Each report: __init__.py + .json + .py + .js
    ├── workspace/
    ├── notification/       ← Each notification: __init__.py + .json
    ├── print_format/
    ├── fixtures/
    └── public/
        ├── css/pharma_rd.css
        └── js/pharma_rd.js
```

### Deploying Updates

```bash
cd ~/frappe-bench
bench get-app --branch main pharma_rd   # pull latest
bench --site your-site migrate
bench build --app pharma_rd
bench --site your-site clear-cache
bench restart
```

---

## Customisation Guide

### Adding a New DocType

1. Create folder: `pharma_rd/doctype/my_new_doctype/`
2. Add `__init__.py` (empty)
3. Add `my_new_doctype.json` — DocType schema
4. Add `my_new_doctype.py` — Controller class
5. Add `my_new_doctype.js` — Client script
6. Run `bench --site your-site migrate`

### Adding a New Report

1. Create folder: `pharma_rd/report/my_report/`
2. Add `__init__.py`, `my_report.json`, `my_report.py`, `my_report.js`
3. In `.json` set `"report_type": "Script Report"` and `"ref_doctype"`
4. Run `bench --site your-site clear-cache`

### Adding a Notification

1. Create folder: `pharma_rd/notification/my_alert/`
2. Add `__init__.py` and `my_alert.json`
3. Set `document_type`, `event`, `condition`, `recipients`, `message`
4. Run `bench --site your-site migrate`

### Extending with Custom Fields

Add to `pharma_rd/fixtures/` a JSON file and add it to the `fixtures` list in `hooks.py`:

```python
fixtures = [
    {"dt": "Custom Field", "filters": [["module", "=", "Pharma R&D"]]}
]
```

Then create custom fields in the UI and export:

```bash
bench --site your-site export-fixtures --app pharma_rd
```

---

## Troubleshooting

| Issue | Solution |
|---|---|
| DocType not appearing | Run `bench --site your-site migrate` |
| Assets not loading | Run `bench build --app pharma_rd && bench --site your-site clear-cache` |
| Notifications not firing | Check Notification log in ERPNext; verify Email Account is configured |
| Scheduled tasks not running | Check `bench doctor`; verify `background_workers` are running |
| Permission denied on DocType | Verify role is assigned in DocType permissions tab; run `bench --site your-site clear-cache` |
| Fixture import fails | Check JSON syntax; verify `fixtures` list in hooks.py |
| Workspace not visible | Re-run `bench --site your-site migrate`; check module name in workspace JSON |
| `bench get-app` fails | Ensure SSH key is set up for GitHub; or use HTTPS URL |

### Useful Debug Commands

```bash
bench --site your-site console                 # Python REPL
bench --site your-site mariadb                 # DB access
bench --site your-site list-apps               # Verify app is installed
bench --site your-site show-config             # Site config
bench --site your-site execute frappe.get_all "\"Research Project\""  # Quick DocType check
tail -f ~/frappe-bench/logs/web.log            # Web server logs
tail -f ~/frappe-bench/logs/worker.log         # Background worker logs
```

---

*pharma_rd v0.0.1 — Built for Frappe Framework v15+*
*License: MIT | Module: Pharma R&D*
