# PCOS Dataset Profile

Generated from the second worksheet of `(Main_Dataset)_PCOS_data_without_infertility.xlsx`.

## Row Counts

- Labeled rows: 541
- PCOS positive: 177
- PCOS negative: 364

## Cycle Coding Audit

Raw `Cycle(R/I)` values are preserved in `cycle_raw`; model input maps `2 -> regular/0` and `4 -> irregular/1`. Any other value is treated as missing.

| Raw value | Count |
|---|---:|
| 2 | 390 |
| 4 | 150 |
| 5 | 1 |

## Excluded Columns

`blood_group`, `i_beta_hcg`, `ii_beta_hcg`, `marraige_status`, `no_of_abortions`, `patient_file_no`, `pregnant`, `sl_no`

## Feature Sets

### History

`age`, `weight_kg`, `height_cm`, `bmi`, `cycle`, `cycle_length`, `weight_gain`, `hair_growth`, `skin_darkening`, `hair_loss`, `pimples`

### Basic

`age`, `weight_kg`, `height_cm`, `bmi`, `cycle`, `cycle_length`, `weight_gain`, `hair_growth`, `skin_darkening`, `hair_loss`, `pimples`, `bp_systolic`, `bp_diastolic`, `rbs`, `tsh`, `prl`, `fsh`, `lh`, `hemoglobin`, `waist`, `hip`, `waist_hip_ratio`

### Full

`age`, `weight_kg`, `height_cm`, `bmi`, `cycle`, `cycle_length`, `weight_gain`, `hair_growth`, `skin_darkening`, `hair_loss`, `pimples`, `bp_systolic`, `bp_diastolic`, `rbs`, `tsh`, `prl`, `fsh`, `lh`, `hemoglobin`, `waist`, `hip`, `waist_hip_ratio`, `amh`, `follicle_no_l`, `follicle_no_r`, `avg_f_size_l`, `avg_f_size_r`, `endometrium`

## Missing Values In Model Features

| Feature | Missing |
|---|---:|
| `age` | 0 |
| `amh` | 1 |
| `avg_f_size_l` | 0 |
| `avg_f_size_r` | 0 |
| `bmi` | 0 |
| `bp_diastolic` | 0 |
| `bp_systolic` | 0 |
| `cycle` | 1 |
| `cycle_length` | 0 |
| `endometrium` | 0 |
| `follicle_no_l` | 0 |
| `follicle_no_r` | 0 |
| `fsh` | 0 |
| `hair_growth` | 0 |
| `hair_loss` | 0 |
| `height_cm` | 0 |
| `hemoglobin` | 0 |
| `hip` | 0 |
| `lh` | 0 |
| `pimples` | 0 |
| `prl` | 0 |
| `rbs` | 0 |
| `skin_darkening` | 0 |
| `tsh` | 0 |
| `waist` | 0 |
| `waist_hip_ratio` | 0 |
| `weight_gain` | 0 |
| `weight_kg` | 0 |

## Derived Value Checks

| Check | Median absolute mismatch | Max absolute mismatch |
|---|---:|---:|
| BMI mismatch | 0.0000 | 0.0000 |
| FSH/LH ratio mismatch | 0.0000 | 0.0000 |
| Waist:hip mismatch | 0.0000 | 0.0000 |
