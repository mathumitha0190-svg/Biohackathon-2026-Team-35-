Table of Contents

[Problem Statement	2](#_Toc229270788)

[Datasets	4](#_Toc229270789)

[Main Dataset Guide	7](#_Toc229270790)

[Judging Criteria	11](#_Toc229270791)

# <a id="_37i74qdjb0pc"></a><a id="_Toc661743837"></a><a id="_Toc314088911"></a><a id="_Toc384316559"></a><a id="_Toc2114411574"></a><a id="_Toc2027347616"></a><a id="_Toc229270788"></a>__Problem Statement__

## <a id="_4x5njgy6i85x"></a><a id="_Toc720957983"></a><a id="_Toc1569199580"></a><a id="_Toc1100287440"></a><a id="_Toc1673232730"></a><a id="_Toc1200149885"></a>__Background__

Women's health faces a persistent and well\-documented crisis of misdiagnosis and diagnostic delay\. Research indicates that women are 66% more likely than men to experience medical misdiagnosis, reflecting systemic gender gaps in medical knowledge and practice\. This disparity stems from multiple factors: clinical trials have historically excluded women, disease presentations in women are often atypical compared to male\-dominated medical literature, and implicit bias frequently leads clinicians to attribute women's symptoms to emotional or psychological causes\.

Such diagnostic failures are not merely inconveniences for patients, they lead to disease progression, unnecessary suffering, infertility, and increased healthcare costs\. They erode trust in healthcare systems and leave women feeling dismissed and ignored\.

## <a id="_x2rsmbcjd9q7"></a><a id="_Toc682495853"></a><a id="_Toc459831587"></a><a id="_Toc665239894"></a><a id="_Toc925611358"></a><a id="_Toc15258388"></a>__Polycystic Ovary Syndrome \(PCOS\)__

Polycystic ovary syndrome \(PCOS\) exemplifies the broader crisis in women's health diagnostics\. PCOS is the most common endocrine disorder affecting reproductive\-age women with a global prevalence of 8\-13%\. The condition carries significant health burdens as a leading cause of infertility and is associated with a four\-fold increased risk of type 2 diabetes, along with elevated risks of metabolic syndrome, cardiovascular disease, depression, and anxiety\. 

Despite its prevalence, the World Health Organization estimates that up to 70% of women with PCOS remain undiagnosed\. Additionally, among those eventually diagnosed, one\-third experience delays exceeding two years, and nearly half consult at least three healthcare professionals before receiving the correct diagnosis\. This diagnostic challenge stems from the condition's heterogeneity \(patients present with varying symptom combinations for the same condition\), the absence of a single diagnostic test \(requiring clinicians to rule out overlapping conditions like endometriosis while synthesizing multiple clinical criteria\), and persistent misconceptions among clinicians about how PCOS presents itself\.

## <a id="_oz0ong8o07em"></a><a id="_Toc519566004"></a><a id="_Toc1753512293"></a><a id="_Toc1855652416"></a><a id="_Toc1981655832"></a><a id="_Toc632105984"></a>__The Challenge__

PCOS represents a microcosm of a larger problem in women's health\. Medical conditions that are common, heterogeneous, and poorly understood in medical practice, lead to delayed or missed diagnoses, with disproportionate impact on marginalized populations\. Yet early diagnosis matters\. Interventions for metabolic complications are most effective when implemented early, and patients deserve timely answers about their health\.

The challenge is to develop a feasible system or method that helps medical professionals improve diagnostic accuracy for women's health conditions\. The solution should:

- Address the diagnostic challenges outlined above such as helping clinicians synthesize complex symptom patterns, identify patients at highest risk of missed diagnosis, differentiate PCOS from conditions with overlapping presentations, or otherwise improve the diagnostic pathway\.
- Be grounded in available data \(such as the datasets provided or other women's health data\) and feasible for real\-world implementation\.
- Consider how the solution might address disparities in diagnosis across different populations\.
- Articulate both the potential impact on patient outcomes and the practical steps toward implementation\.

Interpretation is open\. The solution need not be limited to machine learning models or mobile apps\. It could be a clinical decision support tool, a screening algorithm, a reimagining of diagnostic criteria, a system for identifying at\-risk populations, a patient\-facing tool for better symptom communication, or any other approach that uses data to address the problem\. The key is to demonstrate how the method could reduce diagnostic delays and misdiagnosis, ultimately improving outcomes for women\.

# <a id="_bx1ded9k6rxr"></a><a id="_Toc1081260628"></a><a id="_Toc1811673098"></a><a id="_Toc288563702"></a><a id="_Toc538263796"></a><a id="_Toc1814481365"></a><a id="_Toc229270789"></a>__Datasets__

__Link to OneDrive folder with Datasets: __[__BioHackathon 2026 Datasets__](https://entuedu-my.sharepoint.com/:f:/g/personal/echia013_e_ntu_edu_sg/IgBzV0pH0cC3SaJXYAbofSl_AYFyPgCjaxK0x07e-znUyxY)__ __

<a id="_fyxx3gbdkeak"></a>

## <a id="_k4hdqg5ufhac"></a><a id="_Toc2138310461"></a><a id="_Toc1624452779"></a><a id="_Toc1876880917"></a><a id="_Toc722327802"></a><a id="_Toc824654469"></a>__Main Dataset__

__Participants are required to use this dataset as the foundation for their project to ensure a common basis for comparison\. While this dataset will form the core of the project, participants may also source and use additional datasets to supplement and support their work\.__

__Description__: PCOS physical and clinical parameters dataset

Source: [https://www\.kaggle\.com/datasets/prasoonkottarathil/polycystic\-ovary\-syndrome\-pcos/data](https://www.kaggle.com/datasets/prasoonkottarathil/polycystic-ovary-syndrome-pcos/data)

Link to Dataset \(Excel Sheet\): [PCOS\_Dataset](https://entuedu-my.sharepoint.com/:x:/r/personal/echia013_e_ntu_edu_sg/Documents/BioHackathon%202026%20Datasets/(Main_Dataset)_PCOS_data_without_infertility.xlsx?d=w76f2a27246644d93b37095afcbff889f&csf=1&web=1&e=VCrb3e)

- This dataset contains all physical and clinical parameters to determine PCOS\.
- Polycystic ovary syndrome is a disorder involving infrequent, irregular or prolonged menstrual periods, and often excess male hormone \(androgen\) levels\. The ovaries develop numerous small collections of fluid — called follicles — and may fail to regularly release eggs
- Data is collected from 10 different hospitals across Kerala, India\.

## <a id="_7hne0cvg5e1a"></a><a id="_Toc1325223537"></a><a id="_Toc35764303"></a><a id="_Toc708830791"></a><a id="_Toc78240756"></a><a id="_Toc1227785119"></a>__Supplementary Datasets__

__These datasets are optional for participants to use\. Participants may also source and use additional datasets to supplement and support their work, as they see fit\.__

### <a id="_knbwa0yiota1"></a><a id="_Toc1384790687"></a><a id="_Toc225821496"></a><a id="_Toc1811262120"></a><a id="_Toc829808443"></a><a id="_Toc1658446374"></a>__Endometriosis Dataset__

__Description__: Endometriosis common features and symptoms dataset

Source: [https://www\.kaggle\.com/datasets/michaelanietie/endometriosis\-dataset?resource=download](https://www.kaggle.com/datasets/michaelanietie/endometriosis-dataset?resource=download)

Link to Dataset: [Endometriosis\_Dataset](https://entuedu-my.sharepoint.com/:x:/r/personal/echia013_e_ntu_edu_sg/Documents/BioHackathon%202026%20Datasets/(Supplementary_Dataset)_structured_endometriosis_data.csv?d=w0a4bfc91075147b189c3c22135369f26&csf=1&web=1&e=ysHJMc)

- Dataset contains 10,000 instances of synthetic but realistic data
- Structured to reflect common features and symptoms associated with Endometriosis

Dataset Guide:

__Features:__

- Age: Age of the individual \(18–50 years\)\.
- Menstrual\_Irregularity: Indicates whether the individual experiences irregular menstruation \(0 = No, 1 = Yes\)\.
- Chronic\_Pain\_Level: Pain severity reported by the individual, on a scale of 0 to 10 \(higher indicates more severe pain\)\.
- Hormone\_Level\_Abnormality: Indicates abnormalities in hormone levels \(0 = Normal, 1 = Abnormal\)\.
- Infertility: Indicates if the individual experiences infertility \(0 = No, 1 = Yes\)\.
- BMI: Body Mass Index, ranging from 15 to 40\.
- Diagnosis: Target variable \(0 = No endometriosis, 1 = Endometriosis present\)\.

### <a id="_vluros4xk45b"></a><a id="_Toc1083801655"></a><a id="_Toc791823670"></a><a id="_Toc1492592829"></a><a id="_Toc955031777"></a><a id="_Toc1467184208"></a>__PCOS related Single Cell Dataset__

__Description__: PCOS related Single Cell Datasets

Source: https://pubmed\.ncbi\.nlm\.nih\.gov/41257877/

Link to Dataset \(tar files\): [PCOS\_Single\_Cell\_Dataset](https://entuedu-my.sharepoint.com/:u:/r/personal/echia013_e_ntu_edu_sg/Documents/BioHackathon%202026%20Datasets/(Supplementary_Dataset)_PCOS_single_cell_data.zip?csf=1&web=1&e=IexzAj)

- Single\-Cell RNA\-Seq Identifies Pathways and Genes Contributing to the Hyperandrogenemia Associated with Polycystic Ovary Syndrome
- scRNA\-seq data in the form of 10x Cell Ranger files are available for the following samples:
	- PCOS affected \- Mc03, Mc10, Mc16, Mc26, Mc27
	- Normal cycling women \- Mc02, Mc06, Mc31, Mc40, Mc50
	- A F in the sample name indicates forskolin treatment and a C indicates untreated control samples\.

### <a id="_faqxq7rlmdwh"></a><a id="_Toc621993270"></a><a id="_Toc511837794"></a><a id="_Toc1818811195"></a><a id="_Toc1050652980"></a><a id="_Toc675154084"></a>__Endometrium related Single Cell Dataset__

__Description__: Endometrium related Single Cell Datasets

Source: [https://www\.nature\.com/articles/s41588\-024\-01873\-w](https://www.nature.com/articles/s41588-024-01873-w)

Link to Dataset \(tar files\): [Endometriosis\_Single\_Cell\_Dataset](https://entuedu-my.sharepoint.com/:u:/r/personal/echia013_e_ntu_edu_sg/Documents/BioHackathon%202026%20Datasets/(Supplementary_Dataset)_Endometrium_single_cell_data.zip?csf=1&web=1&e=waVtV1)  \(Note: Only contains 2 single cell outputs out of 103\)

- Endometrial samples from donors in reproductive age with and without endometriosis collected either during natural cycles or under exogenous hormonal treatment\. Samples were profiled either with single\-cell RNA sequencing \(scRNA\-seq\) or single\-nuclei RNA sequencing \(snRNA\-seq\) using 10x technology\.

# <a id="_mqx4qjgod677"></a><a id="_Toc1142252835"></a><a id="_Toc725339284"></a><a id="_Toc251513590"></a><a id="_Toc741583393"></a><a id="_Toc1615064610"></a><a id="_Toc229270790"></a>__Main Dataset Guide__

Instructions for PCOS Dataset from the source:

- Units mentioned in the sheet\.\(ie, feet to cm\)
- Manipulated datas if any need to be highlighted using Orangish colour
- For every Yes/No questions \*\*\* , Indicate Yes = 1 ; No = 0
- Blood Group indications \*\*
	- A\+ = 11
	- A\- = 12
	- B\+ = 13
	- B\- = 14
	- O\+ =15
	- O\- = 16
	- AB\+ =17
	- AB\- = 18
- Blood pressure entered as systolic and diastolic separately
- RBS means Random glucose test
- Beta\-HCG cases are mentioned as Case I and II

A more detailed description can be found in the __metadata table below__

<a id="_1svr1r2t99s6"></a>__Metadata__

SI\. No

Serial Index number

Patient File No\. 

File number of patient

PCOS \(Y/N\)

Indicates if the patient has PCOS; Yes = 1 ; No= 0

Age \(yrs\)

Age in years of the patient

Weight \(kg\) 

Weight of the patient in kg

Height \(cm\)

Height of patient in cm

BMI 

BMI of the patient calculated from the patient’s weight and height

Formula: Weight\(kg\)/Height\(cm\)^2

Blood Group

Blood Group of the patient

Blood Group indications

A\+ = 11

A\- = 12

B\+ = 13

B\- = 14

O\+ =15

O\- = 16

AB\+ =17

AB\- = 18

Pulse rate\(bpm\)

Resting pulse rate in beats per minute

RR \(breaths/min\) 

Respiratory rate in breaths per minute 

Hb\(g/dl\) 

Hemoglobin concentration in grams per deciliter 

Cycle\(R/I\) 

Menstrual cycle regularity: R = Regular, I = Irregular\. \(Coding: Regular = 1, Irregular = 0 if needed\) 

Cycle length\(days\) 

Average length of the menstrual cycle in days \(from first day of one period to the next\) 

Marriage Status \(Yrs\) 

Number of years the patient has been married\.

Pregnant\(Y/N\) 

Whether the patient is currently pregnant; Yes = 1, No = 0 

No\. of abortions 

Total number of spontaneous or induced abortions the patient has experienced 

I beta\-HCG\(mIU/mL\) 

First measurement of beta\-human chorionic gonadotropin \(pregnancy hormone\) in mIU/mL 

II beta\-HCG\(mIU/mL\) 

Second measurement of beta\-hCG \(often taken 48 hours later\) in mIU/mL 

FSH\(mIU/mL\) 

Follicle Stimulating Hormone level in mIU/mL 

LH\(mIU/mL\) 

Luteinizing Hormone level in mIU/mL 

FSH/LH 

Ratio of FSH to LH \(calculated\) – a key indicator in PCOS \(often LH > FSH\) 

Hip\(inch\) 

Hip circumference in inches 

Waist\(inch\) 

Waist circumference in inches 

Waist:Hip Ratio 

Waist circumference divided by hip circumference – measure of fat distribution 

TSH \(mIU/L\) 

Thyroid Stimulating Hormone level in mIU/L 

AMH\(ng/mL\) 

Anti\-Müllerian Hormone level in ng/mL \(marker of ovarian reserve; often elevated in PCOS\) 

PRL\(ng/mL\) 

Prolactin level in ng/mL 

Vit D3 \(ng/mL\) 

Vitamin D3 level in ng/mL 

PRG\(ng/mL\) 

Vitamin D3 level in ng/mL 

RBS\(mg/dl\) 

Random Blood Sugar level in mg/dL 

Weight gain\(Y/N\) 

Presence of unexplained or rapid weight gain; Yes = 1, No = 0 

hair growth\(Y/N\) 

Presence of hirsutism \(excessive male\-pattern hair growth on face/body\); Yes = 1, No = 0 

Skin darkening \(Y/N\) 

Presence of acanthosis nigricans \(dark, velvety patches of skin, often on neck/groin\); Yes = 1, No = 0 

Hair loss\(Y/N\) 

Presence of female pattern hair loss \(thinning of scalp hair\); Yes = 1, No = 0 

Pimples\(Y/N\) 

Presence of persistent or severe acne; Yes = 1, No = 0 

Fast food \(Y/N\) 

Regular consumption of fast food \(typically ≥3 times/week\); Yes = 1, No = 0 

Reg\.Exercise\(Y/N\) 

Regular physical exercise \(typically ≥150 minutes/week of moderate activity\); Yes = 1, No = 0 

BP\_Systolic \(mmHg\) 

Systolic blood pressure in mm Hg \(top number\) 

BP\_Diastolic \(mmHg\) 

Diastolic blood pressure in mm Hg \(bottom number\) 

Follicle No\. \(L\) 

Number of antral follicles \(2–9 mm\) in the left ovary, counted via ultrasound 

Follicle No\. \(R\) 

Number of antral follicles in the right ovary 

Avg\. F size \(L\) \(mm\) 

Average diameter of follicles in the left ovary, in millimeters 

Avg\. F size \(R\) \(mm\) 

Average diameter of follicles in the right ovary, in millimeters 

Endometrium \(mm\) 

Endometrial thickness measured via ultrasound, in millimeters 

# <a id="_icrpd5i1pny7"></a><a id="_Toc242970742"></a><a id="_Toc1913883378"></a><a id="_Toc1868530517"></a><a id="_Toc500308659"></a><a id="_Toc1020516867"></a><a id="_Toc229270791"></a>__Judging Criteria__

__Clinical & Scientific Validity: 30%__

- How accurately the solution reflects current understanding of PCOS biology and pathophysiology \(e\.g\., hormonal, metabolic, reproductive, or ovarian mechanisms\) 
- Whether the approach meaningfully engages with existing diagnostic frameworks or classification approaches where relevant 
- How effectively the solution distinguishes PCOS from overlapping or related conditions
- The strength of scientific justification, including use of literature, clinical rationale, or mechanistic reasoning

__Diagnostic Accuracy: 20%__

- Its ability to improve differentiation between PCOS and other conditions with overlapping symptoms 
- Whether it supports clinical interpretation, decision\-making, or prioritization of investigations 
- Potential usefulness for early identification, risk prediction, or screening 
- Its ability to account for patient heterogeneity, including phenotypes, symptom patterns, or associated comorbidities

__Feasibility & Implementation: 20%__

- Applicability across different clinical environments \(e\.g\., primary care, specialist clinics, telehealth, community settings\) 
- Accessibility, affordability, scalability, and usability 
- Practicality of required data inputs, devices, infrastructure, or workflows 
- Adaptability to low\-resource or data\-limited settings

__Innovation & Creativity: 12%__

- __Novelty__: Does the solution introduce a new perspective, workflow, methodology, or application compared to existing approaches?
- __Creativity__:
	- __Problem reframing__: Does it challenge assumptions, e\.g\. redefining risk criteria?
	- How significantly does the solution vary from existing solutions, how creative is the solution\. 

__Impact & Public Health Value: 10%__

- Potential influence on long\-term health outcomes and quality of life 
- Relevance to diverse or underserved populations 
- Preventive, educational, or early intervention value 
- Scalability and potential public health reach

__Methodology and Scientific Rigor: 10%__

- Do the chosen methods align well with the stated objectives or problem being addressed 
- Clarity and justification of analytical, computational, or research approaches 
- Use of suitable validation, benchmarking, or evaluation strategies

__Code Quality & Technical Execution: 5%__

- Clarity of documentation, comments, and instructions 
- Robustness of data handling and preprocessing 
- Readability, maintainability, and reproducibility of the codebase

__Presentation & Clarity: 3%__

- Clarity in explaining the problem, solution, and methodology 
- Logical organization and ease of understanding 
- Use of demonstrations, visualizations, prototypes, or interactive elements where appropriate

