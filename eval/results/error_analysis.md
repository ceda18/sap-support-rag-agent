# Retrieval error analysis

7 misses: no gold page in the hybrid top 5 pages, or no gold page in the deployed context.

Rank of the first gold page per ranking (1 = best, - = not in the top 100 chunks).

| id | type | gold pages | BM25 | vector | hybrid | reranked | in deployed context | miss |
|---|---|---|---|---|---|---|---|---|
| syn-07 | synthetic | [54] | 74 | 1 | 14 | 1 | yes | MISS |
| syn-09 | synthetic | [70] | 57 | 2 | 6 | 1 | yes | MISS |
| syn-10 | synthetic | [89] | - | 1 | 14 | 6 | yes | MISS |
| syn-28 | synthetic | [243] | - | 54 | 73 | - | NO | MISS |
| man-04 | manual | [105] | - | 5 | 25 | 1 | yes | MISS |
| man-08 | manual | [14] | 34 | 26 | 34 | - | NO | MISS |
| man-10 | manual | [3] | 5 | 42 | 7 | 7 | yes | MISS |
| syn-01 | synthetic | [4] | 1 | 1 | 1 | 1 | yes |  |
| syn-02 | synthetic | [12] | 1 | 1 | 1 | 1 | yes |  |
| syn-03 | synthetic | [22] | 2 | 1 | 1 | 1 | yes |  |
| syn-04 | synthetic | [30] | 2 | 13 | 5 | 1 | yes |  |
| syn-05 | synthetic | [39] | 2 | 3 | 1 | 1 | yes |  |
| syn-06 | synthetic | [46] | 2 | 2 | 2 | 2 | yes |  |
| syn-08 | synthetic | [69] | 1 | 1 | 1 | 1 | yes |  |
| syn-11 | synthetic | [94] | 1 | 10 | 4 | 3 | yes |  |
| syn-12 | synthetic | [98] | 1 | 2 | 1 | 1 | yes |  |
| syn-13 | synthetic | [107] | 8 | 1 | 2 | 4 | yes |  |
| syn-14 | synthetic | [115] | 1 | 2 | 1 | 2 | yes |  |
| syn-15 | synthetic | [126] | 7 | 4 | 5 | 2 | yes |  |
| syn-16 | synthetic | [134] | 7 | 1 | 2 | 2 | yes |  |
| syn-17 | synthetic | [147] | 1 | 1 | 1 | 1 | yes |  |
| syn-18 | synthetic | [148] | 8 | 2 | 1 | 3 | yes |  |
| syn-19 | synthetic | [162] | 3 | 3 | 2 | 1 | yes |  |
| syn-20 | synthetic | [166] | 38 | 2 | 5 | 1 | yes |  |
| syn-21 | synthetic | [181] | 7 | 4 | 4 | 7 | yes |  |
| syn-22 | synthetic | [190] | 8 | 1 | 2 | 2 | yes |  |
| syn-23 | synthetic | [196] | 1 | 1 | 1 | 1 | yes |  |
| syn-24 | synthetic | [206] | 22 | 1 | 2 | 1 | yes |  |
| syn-25 | synthetic | [219] | 2 | 1 | 1 | 1 | yes |  |
| syn-26 | synthetic | [224] | 4 | 1 | 2 | 1 | yes |  |
| syn-27 | synthetic | [230] | 3 | 1 | 1 | 2 | yes |  |
| syn-29 | synthetic | [259] | 1 | 4 | 2 | 1 | yes |  |
| syn-30 | synthetic | [267] | 1 | 2 | 1 | 2 | yes |  |
| man-01 | manual | [30] | 14 | 2 | 1 | 2 | yes |  |
| man-02 | manual | [35] | 1 | 2 | 1 | 1 | yes |  |
| man-03 | manual | [42, 43] | 50 | 1 | 4 | 1 | yes |  |
| man-05 | manual | [265] | 6 | 3 | 3 | 1 | yes |  |
| man-06 | manual | [72] | 1 | 2 | 2 | 1 | yes |  |
| man-07 | manual | [21] | 2 | 14 | 3 | 1 | yes |  |
| man-09 | manual | [396, 397] | 1 | 1 | 1 | 1 | yes |  |

---

## syn-07 (synthetic) - gold pages [54]

**Question:** In PaPM, how can I find out which functions are using a particular environment field, and can I jump straight to one of those functions from the result?

**Reference answer:** Select the field and choose the Where Used button. A dialog box lists all the functions that use that field, and clicking a function in this overview opens the function directly.

**Rank of first gold page** (pages, 1 = best, - = not in top 100 chunks): BM25 74 | vector 1 | hybrid 14 | reranked 1 | in deployed context: yes

**BM25 token match with the gold page:** exact: ['can', 'out', 'functions', 'are', 'a', 'field,', 'and', 'can', 'to', 'of', 'functions', 'the'] | only after lowercasing / stripping punctuation: ['In', 'environment']

**Chunks on the gold page(s):**

- p.54 chunk 143: BM25 rank 90, vector rank - - `Button Description Procedure Open Master Data If you need to define the master data To create the master data, follow the for a field, select it to enable the Open steps below: Master Data button. 1. Choose Open Master D`

- p.54 chunk 144: BM25 rank -, vector rank 1 - `On the Environment Fields tab this lected field. button is displayed as Open Master 3. Choose Create Hierarchy and fill & Hierarchy Data. out all the necessary information. 4. Once you have completed your en- try, choose`

**Top 5 pages the hybrid ranking returned instead:**

- p.352 (chunk 893): `Related Information • For more information about common aspects of SAP Profitability and Performance Management functions, see Concepts for Key Users [page 7]. • For more information on how to add and remove functions in`

- p.61 (chunk 162): `Where used To find out where a field was used within a function, follow the Where used procedure in the Buttons [page 52] section. 1.3.2.2.1.1.1.1.6 BW Fields These are similar to BW InfoObjects but no master data or hie`

- p.48 (chunk 131): `Merge You can use the Merge button to merge the configuration of one environment with the configuration of another environment (never a node). The merge function not only adds or merges functions from one environment to `

- p.106 (chunk 278): `specific function. Key Features The following table explains the key features available. Key Feature Use Environment List All current and historic environments are listed on the initial page. If an environment is deleted`

- p.111 (chunk 293): `Field Description Function The ID of the function relevant for execution. Choose F4 to display all functions configured in the specified environment and version entered above. Run ID The ID of the run relevant for execut`

**Category** (chunk boundary | terminology / synonyms | table | answer spans several pages | ambiguous question | wrong label | other): 

**Note:** 

---

## syn-09 (synthetic) - gold pages [70]

**Question:** I created a function in the PaPM modeling environment and now want to change its technical ID to something different. Is that possible, and what format can the ID take?

**Reference answer:** The function ID starts out numeric, and you can change it to alphanumeric form when you create it. Once the function has been created, the ID is permanently assigned and cannot be edited.

**Rank of first gold page** (pages, 1 = best, - = not in top 100 chunks): BM25 57 | vector 2 | hybrid 6 | reranked 1 | in deployed context: yes

**BM25 token match with the gold page:** exact: ['created', 'a', 'function', 'in', 'the', 'and', 'to', 'change', 'ID', 'to', 'that', 'and', 'can', 'the', 'ID'] | only after lowercasing / stripping punctuation: ['modeling', 'environment', 'Is', 'possible,']

**Chunks on the gold page(s):**

- p.70 chunk 186: BM25 rank -, vector rank - - `If you choose the Where Used button, the system shows you where the selected function is used as input.`

- p.70 chunk 187: BM25 rank -, vector rank - - `1.3.2.2.1.2.1 Add Function You can use the Add Function button to create a new function: 1. Choose an entry from the list of functions as the starting point of the description or function that you are creating.  Note By`

- p.70 chunk 188: BM25 rank 69, vector rank 2 - `If you have selected a function before choosing Add (+), you can only add a function on the same level and the system will not allow you to add a function one level below. • General Tab 1. Function This is an ID that is `

- p.70 chunk 189: BM25 rank -, vector rank - - `• “Management”: This allows all unprocessed records to be further processed using the My Events application.  Example If the allocation function has an unassigned item, set Event Handling to “Management”. 5. Processing `

**Top 5 pages the hybrid ranking returned instead:**

- p.326 (chunk 829): `1. Go to transaction /n/nxi/p1_mf. 2. From here, go to Rule Types Remote Function Adapter Mapping . 3. The system gives you the option to select an RFA type (for example, “Finance General Ledger”). 4. This provides you w`

- p.47 (chunk 130): `In SAP Profitability and Performance Management, do not use an environment ID that starts with the letter “S” (for example “SEN”). This letter is reserved explicitly for use in the default template environment and for sa`

- p.72 (chunk 193): `1.3.2.2.1.2.4 Copy When you copy a function, all the configuration settings made in this function are automatically copied to the new one. By default, the copied function has the same function ID and description as the o`

- p.110 (chunk 291): `1.3.5.2 Run Function This tool allows you to run functions without having to access the modeling environment. The following fields are available: Field Description Environment This is a 3-digit alphanumeric ID that is pe`

- p.50 (chunk 137): `If you are using SAP Profitability and Performance Management 3.0 SP07 or below, select Meta Function Table Info. 3. The Function Table Info overview screen appears. The listed table names are included once a transport i`

**Category** (chunk boundary | terminology / synonyms | table | answer spans several pages | ambiguous question | wrong label | other): 

**Note:** 

---

## syn-10 (synthetic) - gold pages [89]

**Question:** I'm setting up a new field in PaPM Modeling and need to decide on its type. What kinds of fields can I pick from, and what is each one meant for?

**Reference answer:** When creating a field you can choose Characteristic, Key Figure or Unit. A Characteristic identifies key figures and holds texts, codes, dates or numerical characteristic values. A Key Figure is used for calculations and can hold natural numbers, integers, decimals or floating points. A Unit is needed to give meaning to the values of a key figure.

**Rank of first gold page** (pages, 1 = best, - = not in top 100 chunks): BM25 - | vector 1 | hybrid 14 | reranked 6 | in deployed context: yes

**BM25 token match with the gold page:** exact: ['a', 'field', 'in', 'and', 'to', 'of', 'can', 'and', 'is'] | only after lowercasing / stripping punctuation: ['Modeling', 'fields', 'from,', 'for?']

**Chunks on the gold page(s):**

- p.89 chunk 234: BM25 rank -, vector rank - - `3. Choose Studio. 4. Select an environment from the environment list. 5. In the Go to menu in the top right-hand corner of the screen, choose Modeling.`

- p.89 chunk 235: BM25 rank -, vector rank 1 - `1.3.3.5.1.2.1 General Entities The following general entities are available in SAP Profitability and Performance Management: Entity Icon Description Fields A field is a unique technical name that initially has a predefin`

**Top 5 pages the hybrid ranking returned instead:**

- p.19 (chunk 50): `1.2.3 Information Models for Master Data and Lookup The term “Master Data” is used in the following two ways: 1. Master Data of a Field Field master data defines the values permitted for a field like InfoObjects and data`

- p.356 (chunk 902): `For more information, see SAP Note 2935308 – PaPM 3.0 Bank Analyzer/Insurance Analyzer Result Data Layer integration . 1.4.4 Structuring Functions SAP Profitability and Performance Management offers the following functio`

- p.59 (chunk 158): `1.3.2.2.1.1.1.1.5 Environment Fields Fields are visible only in the environment in which the field is defined. Once the environment is transported, these fields will also be available in the target system. Refer to the F`

- p.203 (chunk 536): `1.4.2.6 Flow Modeling The Flow Modeling function offers a set of rule types that provide different calculation logic to process different kinds of business requirements. Each rule type represents an independent and reusa`

- p.398 (chunk 1008): `• Order by Fields: Specifies the fields according to that the segmented datasets are to be sorted. Rule Output Fields You can use the following output fields for configuration: • Predicted Value: Specifies a field that s`

**Category** (chunk boundary | terminology / synonyms | table | answer spans several pages | ambiguous question | wrong label | other): 

**Note:** 

---

## syn-28 (synthetic) - gold pages [243]

**Question:** In the Flow Modeling configuration for the Acknowledgement of Actuals (Same Period) rule, which fields do I need to assign for actuarial granularity, the business date, and the life cycle step, and what period type is used?

**Reference answer:** The actuarial granularity fields are Contract, Cost Category, and Coverage. The business date field is Key Date, and the life cycle step field is Cf Indicator. The period type is Monthly.

**Rank of first gold page** (pages, 1 = best, - = not in top 100 chunks): BM25 - | vector 54 | hybrid 73 | reranked - | in deployed context: NO

**BM25 token match with the gold page:** exact: ['Flow', 'Modeling', 'of', 'Actuals', 'and', 'and'] | only after lowercasing / stripping punctuation: ['In', 'configuration', '(Same', 'Period)', 'rule,', 'fields', 'actuarial', 'granularity,', 'business', 'date,', 'life', 'cycle', 'step,', 'period', 'type']

**Chunks on the gold page(s):**

- p.243 chunk 622: BM25 rank -, vector rank - - `Input Data Pr Pr Cost Cf In- Re- In- Re- Set- Cov- Cat- Indi- cur- port cur- port Set- tled Cur- Hold Cf Con- erag egor ca- red ed red ed Due tled Amo renc BT Back RA Key Re- Calc tract e y tor Date Date Date Date Date D`

- p.243 chunk 623: BM25 rank -, vector rank 77 - `Q101 _Q10 -05-1 -06- _01 -01-3 -01-3 -05-1 DT 1DT 4 25 1 1 5 01 RIC_ COV 1010 1 2018 2018 2018 2018 2018 2018 400 EUR 2018 2018 2018 Q101 _Q10 -01- -05- -04- -05- -06- -07- -01-3 -01-3 -05-1 DT 1DT 01 25 25 25 25 25 1 1 `

**Top 5 pages the hybrid ranking returned instead:**

- p.242 (chunk 620): `1.4.2.6.13 Example: Acknowledgment of Actuals Enriches actuals by applying matching logic to determine date information missing earlier in the life cycle, and also determines the regime for every cashflow item. The match`

- p.203 (chunk 536): `1.4.2.6 Flow Modeling The Flow Modeling function offers a set of rule types that provide different calculation logic to process different kinds of business requirements. Each rule type represents an independent and reusa`

- p.204 (chunk 540): `Calculates estimate values prior to the Reference Date for Redistribution (RDR) and redistributes them to the future periods after this date. 11. Scale Factor [page 239]: Ratio of two corresponding values with similar fi`

- p.244 (chunk 625): `incurred date has to be calculated as a factor of actuals to be accounted as estimates. Business Date Field Defines the key date for which the esti- mated cashflows are projected. Period Type Defines the periodicity used`

- p.206 (chunk 547): `For more information about the Input tab, see Input [page 12]. 3. Define the function to be used on the Lookup tab, if needed.  Note For more information about the Lookup tab, see Lookup [page 14]. 4. Define the fields `

**Category** (chunk boundary | terminology / synonyms | table | answer spans several pages | ambiguous question | wrong label | other): 

**Note:** 

---

## man-04 (manual) - gold pages [105]

**Question:** I'm a business user. What does modeling history tell me?

**Reference answer:** This application enables you to trace and inspect the configuration changes to a model within an environment. This helps you to trace and audit who did what and when. Depending on the user authorizations, even historic versions of environments and functions can be restored. You can choose the environment and version, and start the application to display objects for the selected configuration only.

**Rank of first gold page** (pages, 1 = best, - = not in top 100 chunks): BM25 - | vector 5 | hybrid 25 | reranked 1 | in deployed context: yes

**BM25 token match with the gold page:** exact: ['a'] | only after lowercasing / stripping punctuation: ['user.', 'What', 'modeling', 'history']

**Chunks on the gold page(s):**

- p.105 chunk 275: BM25 rank -, vector rank - - `1.3.4.2 Process Monitor The application enables you to examine all currently active and past processes. Search, filter and sorting of processes and activities is supported as well. Key Features The following table explai`

- p.105 chunk 276: BM25 rank -, vector rank 5 - `1.3.4.3 Modeling History This application enables you to trace and inspect the configuration changes to a model within an environment. This helps you to trace and audit who did what and when. Depending on the user author`

**Top 5 pages the hybrid ranking returned instead:**

- p.107 (chunk 281): `• Field: Allows you to retrieve a specific version of a field. 3. The following columns appear on the Function Details section of the History Versions screen: • Description: This is the same as the environment name • His`

- p.35 (chunk 95): `Section Application Description Modeling History [page 105] Displays the change history of all envi- ronments and allows users to retrieve historic versions. Tools Activate Function [page 108] Allows you to activate a fu`

- p.106 (chunk 279): `name. Function All the operations executed on the function within the envi- ronment are listed here together with the timestamp, user and name. Fields All the operations executed for fields on the environment are listed `

- p.51 (chunk 139): `Button Description Environment Details [page 51] Opens the details of the environment, where the system dis- plays six sections that contain settings that apply to specific functions in the environment. Historize Takes a`

- p.45 (chunk 122): `Related Information For more information about financial and business modeling, see Financial and Business Modeling Entities [page 8]. For more information about the modeling environment, see Modeling Environment [page 5`

**Category** (chunk boundary | terminology / synonyms | table | answer spans several pages | ambiguous question | wrong label | other): 

**Note:** 

---

## man-08 (manual) - gold pages [14]

**Question:** I'm actually totally new to this. How do signatures work?

**Reference answer:** All processing functions have a signature, which can produce a result for subsequent functions. The signature defines the minimum number of relevant fields of a function. There can also be further implicit fields from the input. These simply pass through the function without any change or any effect on the logic, and also appear in the output if no aggregation within the function is defined. 

**Rank of first gold page** (pages, 1 = best, - = not in top 100 chunks): BM25 34 | vector 26 | hybrid 34 | reranked - | in deployed context: NO

**BM25 token match with the gold page:** exact: ['to', 'do'] | only after lowercasing / stripping punctuation: ['this.']

**Chunks on the gold page(s):**

- p.14 chunk 37: BM25 rank 40, vector rank - - `8. Choose Save. Removing Fields To remove a field from the Input tab, follow the steps below: 1. Select the field you want to remove.  2. Choose (Remove Field). 3. Choose Save. 1.2.2.3 Lookup In the Calculation, Funds T`

- p.14 chunk 38: BM25 rank -, vector rank 27 - `1.2.2.4 Signature All processing functions have a signature, which can produce a result for subsequent functions. The signature defines the minimum number of relevant fields of a function. There can also be further impli`

**Top 5 pages the hybrid ranking returned instead:**

- p.382 (chunk 972): `• Result Handling • Include Original Input Data • Suppress Initial Result • Result Model Table 2. Define the input function to be used on the Input tab.  Note For more information about the Input tab, see Input [page 12`

- p.351 (chunk 891): `1. In edit mode, configure the following required fields in the header. For more information about the header, see the Key Features section above. • Output Function = “Model BW” • BW Writer Type = “Planning” • Model Writ`

- p.344 (chunk 875): `Function Configuration Follow the steps below to configure the Writer function with output “Model Table”: 1. In edit mode, configure the following required fields in the header. For more information about the header, see`

- p.348 (chunk 885): `• BW Writer Type = “Loading” • Model Writer Type = “Insert” 2. Define the input function to be used on the Input tab.  Note For more information about the Input tab, see Input [page 12]. 3. Define the fields to be used `

- p.18 (chunk 47): `1.2.2.6 Rules Rules contain the individual part of most of the functions. They contain the following common fields: Field Description Rule ID The rule ID has to be unique in a function. If (interim) results of a function`

**Category** (chunk boundary | terminology / synonyms | table | answer spans several pages | ambiguous question | wrong label | other): 

**Note:** 

---

## man-10 (manual) - gold pages [3]

**Question:** What even is SAP PaPM?

**Reference answer:** SAP Profitability and Performance Management is a new generation of performance management applications that can use existing data and information models from other SAP and non-SAP applications. It is built on the SAP HANA platform and provides real-time insights, agile financial modeling capabilities, and integration with other SAP and non-SAP components.

**Rank of first gold page** (pages, 1 = best, - = not in top 100 chunks): BM25 5 | vector 42 | hybrid 7 | reranked 7 | in deployed context: yes

**BM25 token match with the gold page:** exact: ['even', 'is', 'SAP'] | only after lowercasing / stripping punctuation: []

**Chunks on the gold page(s):**

- p.3 chunk 7: BM25 rank 16, vector rank 49 - `1 SAP Profitability and Performance Management SAP Profitability and Performance Management is a new generation of performance management applications that can use existing data and information models from other SAP and `

- p.3 chunk 8: BM25 rank 46, vector rank 46 - `advanced potential of SAP HANA, SAP Profitability and Performance Management is designed for business and provides an instant insight by using a single source of truth, real-time processes, and agile financial and busine`

- p.3 chunk 9: BM25 rank 5, vector rank - - `data are already installed on SAP HANA, we recommend that you use SAP Profitability and Performance Management on the same SAP HANA platform or even on the same instance to ensure optimal performance and the maximum reus`

**Top 5 pages the hybrid ranking returned instead:**

- p.29 (chunk 80): `1.2.7 Integration 1.2.7.1 Integration with SAP ERP and SAP S/4HANA SAP Profitability and Performance Management allows integration with SAP ERP and SAP S/4HANA, including redundancy-free reuse of data, master data and hi`

- p.378 (chunk 962): `• “Yes”: Manual data input or planning is permitted. • “No”: Manual data input or planning is not permitted. • Display • Hide: Defines the display behavior of the key figure. • Always Show SAP Profitability and Performan`

- p.4 (chunk 12): `transparency by offering traceability and auditability information. In addition, it allows non-SAP and SAP BI tools, like SAP Analysis for Microsoft Office, to access the information or even trigger further calculations.`

- p.28 (chunk 78): `maintained. /NXI/P1FTY Defines the function type for which the authorization is maintained. /NXI/P1FID Defines the function ID for which the authorization is main- tained. SAP Profitability and Performance Management 28 `

- p.318 (chunk 810): `• accountt[2]-taxjurcode (Tax Jurisdiction) for Ac- counts Payable, and accountt[1]-taxjurcode for Accounts Receivable For FI-AP integration scenarios with SAP ERP or SAP S/4HANA, this feature enables the posting of vend`

**Category** (chunk boundary | terminology / synonyms | table | answer spans several pages | ambiguous question | wrong label | other): 

**Note:** 
