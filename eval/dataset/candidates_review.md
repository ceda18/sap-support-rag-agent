## syn-01 | page 4 | lexical overlap 0.52

**Q:** When PaPM needs to push results out to other systems like BW/4HANA, BPC or the Results Data component, which interfaces does it use, and what does it fall back on if a redundancy-free approach isn't possible?

**A:** For write access, PaPM uses official application interfaces such as SAP HANA-based write interfaces like HAP to BW or BW/4HANA, SAP HANA-based PAK functions to BPC, and AMDP interfaces to the Results Data component. If that redundancy-free approach isn't feasible, it uses other official interfaces such as SAP BAPIs and Web services, or classic file exports in various formats.

```
imports of various formats.
SAP Profitability and Performance Management uses the official application interfaces from the SAP or non-
SAP application for data write access, for example SAP HANA-based write interfaces like HAP to BW or BW/
4HANA, SAP HANA-based PAK functions to BPC and AMDP interfaces to the Results Data component. If this
redundancy-free approach is not feasible, SAP Profitability and Performance Management uses other official
application interfaces, such as SAP BAPIs and Web services, or classic file exports of various formats.
Features
The simulation application capabilities of SAP Profitability and Performance Management enable the execution
of what-if scenarios for business users and the management of assumptions and drivers. Based on the
granularity of the financial model, it allows drill-down from high-level to very detailed results and provides
transparency by offering traceability and auditability information. In addition, it allows non-SAP and SAP BI
```

## syn-02 | page 12 | lexical overlap 0.14

**Q:** In a PaPM function, what happens when the Result Handling is configured to abort on records where no rule could be applied? How does it differ from just raising an error for those records?

**A:** With the abort option, the system writes an abort message to the log and terminates the function, rather than writing an error message. Otherwise it works the same way as the error handling for non-enriched data.

```
log and a business event is registered so that the
business user can deal with the exceptional situa-
tion and fix it.
• “Abort on non-enriched data”: This setting works in the
same way as errors in non-enriched data, but instead of
an error message the system writes an abort message
to the log, and the function is terminated.
Procedure
As each function has different header fields, you can find more information about the specific header
procedures in the Functions section (see Functions [page 118]).
```

## syn-03 | page 22 | lexical overlap 0.18

**Q:** When I set up the run mode for a partitioning in PaPM, what does the last position of the run mode code control, and what is the difference between choosing the partitioned option and leaving it blank?

**A:** The last position determines whether the environment-managed Model Table or Model BW is activated with the partitioning range information applied on the database (Partitioned, P), which is especially helpful in scale-out environments. Leaving it blank (Not Partitioned) means no partitioning is applied on the database.

```
2. “Unpackaged” means that one instance of the function run is initiated without restriction to a
range field value.
3. “Batch-Process” (B), “Dialog-Process” (D) or “Process like Caller” (X):
1. “Batch-Process” means that a new background job is opened, the run of the function is
submitted to this background job and the job definition is closed afterwards.
2. “Dialog-Process” means that a new task is opened in dialog mode, where the function run is
initiated.
3. “Process like Caller” means that the run of the function is initiated directly in the process of
the caller, which can be either in dialog or background mode.
4. “Partitioned” (P) or “Not Partitioned” (“ ”):
1. “Partitioned” means that the environment-managed Model Table or Model BW is activated
in such a way that the partitioning range information is applied on the database. This is
especially helpful in scale-out environments.
2. “Not Partitioned” means that no partitioning is applied on the database.
```

## syn-04 | page 30 | lexical overlap 0.39

**Q:** We run PaPM on a separate NetWeaver instance from our ERP system and want to post accounting documents to it. Which interface does PaPM use for the posting, and where do I enter the remote RFC destination?

**A:** Posting in the remote scenario uses the official BAPI. You specify the remote RFC destination on the Advanced tab of the environment.

```
the corresponding fields to local InfoObjects in the SAP Profitability and Performance Management
instance has to be set up on the remote instance. For more information, see the SAP ERP and SAP
S/4HANA documentation. Once this replication is set up, from an SAP Profitability and Performance
Management perspective the master data and hierarchy data behaves as it does in the local scenario.
2. Reading of Accounting and Controlling Data
Accounting and controlling data available as SAP HANA-based CDS view interfaces from the remote
SAP ERP and SAP S/4HANA instance can be reused.
3. Posting of Accounting and Controlling Data
For posting, the official BAPI is used. You need to specify the remote RFC destination on the Advanced
tab for the environment.
4. Other use cases
Further read or write access use cases can be customized using the SAP Profitability and Performance
Management functions Model View, Model Table and Remote Function Adapter.
Related Information
```

## syn-05 | page 39 | lexical overlap 0.35

**Q:** When I create a new connection in PaPM Manage Connections, which kinds of data sources can I choose for the connection, and what is the difference between the Default and Custom connection classes?

**A:** Connection sources allowed are DDIC Table, DDIC View, CDS View, HANA Table, HANA View, HANA SDA, BW InfoProvider, Model RDL, OData Service, and After Import. For the connection class, "Default" connections can be transported, while "Custom" connections cannot be transported.

```
that the connection name you create does not start with the letter “S”.
• Connection Description: Details about the connection
• Connection Class
• “Default”: This connection can be transported
• “Custom”: This connection cannot be transported
• Connection Source: Connections are allowed for DDIC Table, DDIC View, CDS View, HANA Table, HANA
View, HANA SDA, BW InfoProvider, Model RDL, OData Service, and After Import.
5. Choose OK to continue.
6. The system displays the Connection Details screen, where you can see the Connection Name, Connection
Details, Connection Source and Connection Description columns. On the left-hand side, these field columns
are read-only; they can be edited only on the right-hand side. You can add hidden columns by using the
Personalization button. Additional fields are available in the connection details on the right side.
7. In the Table / View Name field, you can choose a table name either by entering it manually or by using the
search help as follows:
```

## syn-06 | page 46 | lexical overlap 0.33

**Q:** I created an environment in SAP PaPM My Environments with the wrong 3-character ID. Can I change it afterwards, and are there any restrictions on which starting letter I should use for the ID?

**A:** No. The environment ID is a 3-digit alphanumeric ID that is permanently assigned, so it cannot be edited once the environment or node has been created. You should also not use an ID starting with the letter "S" (for example "SEN"), because that letter is reserved for the default template environment.

```
• “Same Level”: This option means that the environment or node that you create is structured or
created at the same level as the selected entry. If you have not selected an entry before choosing
 (Add), the system automatically creates the environment or node at the highest level of the
structure .
• “One Level Below”: You can only use this option if you have selected a node before choosing
 (Add). You can only add nodes or environments to nodes or directories.
If you selected an environment before choosing  (Add), the system automatically sets the Add Level
field to “Same Level”.
2. Environment ID
This is a 3-digit alphanumeric ID that is permanently assigned to the node or environment. Once it has
been created, it is not possible to edit the environment ID.
 Note
In SAP Profitability and Performance Management, do not use an environment ID that starts with
the letter “S” (for example “SEN”). This letter is reserved exclusively for use in the default template
```

## syn-07 | page 54 | lexical overlap 0.23

**Q:** In PaPM, how can I find out which functions are using a particular environment field, and can I jump straight to one of those functions from the result?

**A:** Select the field and choose the Where Used button. A dialog box lists all the functions that use that field, and clicking a function in this overview opens the function directly.

```
On the Environment Fields tab this
lected field.
button is displayed as Open Master
3. Choose Create Hierarchy and fill
& Hierarchy Data.
out all the necessary information.
4. Once you have completed your en-
try, choose Save and activate.
Where Used
Lists all the functions that use a se- To check where the fields are used, fol-
lected field. low the steps below:
1. Select the field and choose the
Where Used button.
2. A dialog box appears, showing all
the functions that use this field.
 Note
When you click on a function in this
overview, you can directly open the
function itself.
SAP Profitability and Performance Management
54 PUBLIC SAP Profitability and Performance Management
```

## syn-08 | page 69 | lexical overlap 0.58

**Q:** In PaPM, where do I configure the RFC connection that lets the remote function adapter post documents to an S/4HANA system or pull master data such as an InfoObject back from a remote system, and what do I have to enter there?

**A:** In the Modeling Environment, go to the Environment button, Advanced tab, and choose RFC Destination (or Call Back RFC Destination). Enter the "RFC destination of PaPM client". Once defined, the remote function adapter can post documents to SAP S/4HANA or replicate master data from it.

```
Field Description
Call Back RFC Destination / RFC Destination
This allows you to connect an SAP ERP or SAP S/4HANA
system to SAP Finance and Controlling. If you define this, the
remote function adapter can post documents to an SAP S/4
HANA system or replicate master data from it (for example,
to replicate an InfoObject from a remote system back to SAP
Profitability and Performance Management).
To maintain this in the Modeling Environment,
select Environment Button Advanced Tab RFC
Destination or choose Call Back RFC Destination and enter
“RFC destination of PaPM client”.
```

## syn-09 | page 70 | lexical overlap 0.47

**Q:** I created a function in the PaPM modeling environment and now want to change its technical ID to something different. Is that possible, and what format can the ID take?

**A:** The function ID starts out numeric, and you can change it to alphanumeric form when you create it. Once the function has been created, the ID is permanently assigned and cannot be edited.

```
If you have selected a function before choosing Add (+), you can only add a function on the same level
and the system will not allow you to add a function one level below.
• General Tab
1. Function
This is an ID that is initially numeric, but that you can change to alphanumeric form if required.
It is permanently assigned to the function. Once it has been created, it is not possible to edit the
function ID.
2. Description
Enter a description here to name the function. You can adjust this description later, if necessary, by
choosing Edit in the Modeling Environment screen.
3. Function Type
You can choose one of the available functions used for modeling. For more information see the
Functions [page 118] section.
4. Event Handling
You can choose one of the following options:
• “Logging”: Registers function processing errors in the application log after processing.
• “Management”: This allows all unprocessed records to be further processed using the My
Events application.
 Example
```

## syn-10 | page 89 | lexical overlap 0.21

**Q:** I'm setting up a new field in PaPM Modeling and need to decide on its type. What kinds of fields can I pick from, and what is each one meant for?

**A:** When creating a field you can choose Characteristic, Key Figure or Unit. A Characteristic identifies key figures and holds texts, codes, dates or numerical characteristic values. A Key Figure is used for calculations and can hold natural numbers, integers, decimals or floating points. A Unit is needed to give meaning to the values of a key figure.

```
1.3.3.5.1.2.1 General Entities
The following general entities are available in SAP Profitability and Performance Management:
Entity Icon Description
Fields
A field is a unique technical name that
initially has a predefined characteristic
value which you can use as it is or
change to a different value.
When you create a field, you can choose
from the following field types:
• Characteristic: Used to identify key
figures, and contains texts, codes,
dates or numerical characteristic
values.
• Key Figure: Used for calculations
and can contain natural num-
bers, integers, decimals or floating
points.
• Unit: Required to give meaning to
the values of a key figure.
Parameters
Parameters are used to steer processes
and calculations. They are used in for-
mulas and calls of certain functions to
influence the logic and operations ap-
plied.
SAP Profitability and Performance Management
SAP Profitability and Performance Management PUBLIC 89
```

## syn-11 | page 94 | lexical overlap 0.43

**Q:** In the Report Management toolbar, which button takes me to the Process Management application, and what kind of view of the process instances will I see there?

**A:** The Process button navigates to the Process Management application, where process instances are visualized as a Gantt diagram.

```
images, tables and media, such as YouTube videos.
Modeling Allows navigation to the Modeling application, where process
environment versions are visualized in the form of a directed
graph.
Process Allows navigation to the Process Management application,
where process instances are visualized in the form of a Gantt
diagram.
Properties The Properties Panel on the right-hand side of the screen-
shows all process parameters and process selections of the
underlying process template or process instance.
Story filters comprise all fields, which are in use by the
embedded report elements and allow you to filter all re-
port elements at the same time. The client-side simulation
can contain a script, which can be executed via Tools
Simulate .
SAP Profitability and Performance Management
94 PUBLIC SAP Profitability and Performance Management
```

## syn-12 | page 98 | lexical overlap 0.38

**Q:** How do I animate how items move through the steps of a process diagram in a PaPM report, and which diagram types support this?

**A:** Flow Animation is available for process and relationship diagrams. Right-click the diagram to open the context menu, choose Flow Animation, and select one or more flow animation values. These values are offered only if a Flow field has been selected in the properties.

```
All filters, story filters, visualization field setting filters as well as the dimension values of the selected data point
or node are handed over to the target chart.
Flow Animation
The flow settings for Flow Animation are available for process and relationship diagrams. If a Flow field is
selected in the properties, its values are offered in the diagram for flow animation. It is especially helpful to
animate the flow through activities in Process Mining Analysis.
Procedure
Follow the steps below to trigger Flow Animation:
1. Open the context menu for a Process or Relationship diagram (right mouse click).
2. Choose Flow Animation and select one or more flow animation values.
```

## syn-13 | page 107 | lexical overlap 0.38

**Q:** I deleted a field by mistake in one of my PaPM environments. How do I get an earlier version of it back using the modeling history report, and which screen and tabs do I use for that?

**A:** Open the Modeling History report via the SAP Menu (System Reports > Show Modeling History) or transaction /NXI/P1_MODEL_HIST. Choose the environment from the list as the starting point, then on the History Versions screen select the Field tab and use the Retrieve button to recover a specific version of the field. The Environment and Function tabs work the same way for environments and functions.

```
• The Historize button is manually executed in the environment.
Procedure
In the client where SAP Profitability and Performance Management is installed, choose SAP Menu
Profitability and Performance Management System Reports Show Modeling History or launch the
transaction code /NXI/P1_MODEL_HIST. The system opens the Modeling History window where you can
process the following activities in edit mode.
Retrieve Function
You can use the Retrieve button to recover the specific environment, function or field:
1. Choose an environment from the environment list to be the starting point of the retrieval.
2. On the History Versions screen, choose one of the following tabs:
• Environment: Allows you to retrieve a specific version of an environment.
• Function: Allows you to retrieve a specific version of a function.
• Field: Allows you to retrieve a specific version of a field.
3. The following columns appear on the Function Details section of the History Versions screen:
```

## syn-14 | page 115 | lexical overlap 0.62

**Q:** In the Display Run Function Statistics window, when I compare a main run against a reference run and tick the option to show only differences, which rows remain visible, and what do the extra comparison columns for entries and runtime show?

**A:** With Only Differences selected, only rows with a non-zero entries difference are displayed. The extra columns are Entries Difference (main run entries minus reference run entries) and Runtime Difference (the difference between the main run's and the reference run's runtime).

```
then all columns for the main run described above are available for the reference run as well. In addition, these
columns are also available:
Column Information displayed
Entries Difference The difference between the main run and reference run en-
tries. If the option Only Differences is selected in the Display
Run Function Statistics window, then only those lines (rows)
which show a non-zero difference are displayed.
Runtime Difference The difference between the main run and reference run run-
time.
SAP Profitability and Performance Management
SAP Profitability and Performance Management PUBLIC 115
```

## syn-15 | page 126 | lexical overlap 0.62

**Q:** I want to set up the Model BW function using the Business Warehouse source. What menu path do I follow in the SAP client to reach it, and what do I do once the environment opens?

**A:** In the client where SAP PaPM is installed, choose SAP Menu > Profitability and Performance Management > Modeling > Start My Environments. The Environment screen opens in a separate browser window, where you choose an existing environment and continue, then set up the newly added function within it.

```
and description of the new fields. However, you need to ensure that the name is unique. You can also exclude
certain fields from read access. If you want the changes to be reset to the initial state, choose Reset Proposal.
Parameters
If input parameters have been defined for the generated external SAP HANA view, the parameters appear here,
and a constant value or an environment parameter can be assigned.
Procedure
Function Access
Follow the steps below to access the Model BW function with source “Business Warehouse”:
1. In the client where SAP Profitability and Performance Management is installed, choose SAP Menu
Profitability and Performance Management Modeling Start My Environments .
2. The Environment screen appears in a separate browser window. Choose an existing environment and
continue. Within the environment, you can set up the newly added function.
SAP Profitability and Performance Management
126 PUBLIC SAP Profitability and Performance Management
```

## syn-16 | page 134 | lexical overlap 0.57

**Q:** In a Model Join, what does the auto filling option that goes from first to last do when a field has empty or initial values? And what is filled in if the following table has nothing but initial values for that field?

**A:** With the "If Null/Initial then First to Last" auto filling setting, the system replaces null and initial values (whitespace for a characteristic, zero for a key figure) with the next non-null value of the same field in the succeeding table. If that field contains only null or initial values, the system just sets an initial value.

```
1.4.1.3.1.2 Example: If Null/Initial Then First to Last
This scenario shows the enrichment capability of the Model Join function to highlight the effect of Auto Filling
set to “If Null/Initial then First to Last”.
That means, the system substitutes null and initial values (for Characteristic it is whitespace (' ') and for Key
Figure it is zero ('0')) by the next non-null value of the succeeding table having the same field. If this field only
has initial/null values, the system just sets an initial value.
Input Tables
Legend: " is considered as an initial or empty input
SAP Profitability and Performance Management
134 PUBLIC SAP Profitability and Performance Management
```

## syn-17 | page 147 | lexical overlap 0.61

**Q:** My Model Table reads from a DDIC table that has a client column. Why do I only get rows for my logon client, and what do I have to change on that field to pull in data from all clients?

**A:** When the DDIC source table has a client field (data type CLNT) and the Exclude option is not selected, the system filters the source data and selects only data for the current system client. If you select Exclude for the client field, the system reads all data from the source and does not filter by client.

```
option to change the field name and description of the new fields which should be unique. You can also exclude
certain fields from read access. If you want the changes to be reset to the initial state of the field, choose Reset
Proposal.
Further Details
If a DDIC table that is used as the source for a model table has a client field (field with DDIC data type CLNT),
the system selects data differently, depending on whether or not you have selected the Exclude option. If you
do not select Exclude, the system filters source data, and selects only data for the current system client. If you
select Exclude, the system selects all data from the source object, and does not filter by client.
If a model table that uses a DDIC table as a source is used as the target for a writer function, the system always
populates the client field with the value of the current client, irrespective of whether or not you have selected
the Exclude option for the client field.
```

## syn-18 | page 148 | lexical overlap 0.06

**Q:** I created a Model Table function in SAP PaPM with the Environment source and now want to fill it with records in the Data Editor. What are my options for getting the data in?

**A:** In the Data Editor, choose Edit, enter all the data and save. The data can be maintained either by writing directly in the fields (including copy and paste) or by importing it from an Excel file.

```
1. Choose Edit.
2. Input all the data and save.
 Note
The data can be maintained in two ways:
• Writing directly on the fields (Copy and Paste)
• Importing using an excel file.
Related Information
For more information about common aspects of SAP Profitability and Performance Management functions, see
Concepts for Key Users [page 7].
SAP Profitability and Performance Management
148 PUBLIC SAP Profitability and Performance Management
```

## syn-19 | page 162 | lexical overlap 0.67

**Q:** In a Receiver Rule with variable portions where the distribution driver is taken from the receiver, with periodic processing limited to periods 1 through 4, how do I get the portion percentages? Which fields do I group on, and what is the sender amount allocated on?

**A:** The sender amount (ZE_AMT) is allocated proportionally, using the receiver's driver field (ZE_DRBRT) as the distribution percentage. To work out the portion, you first group by the fields that have the same characteristics in sender and receiver, which are ZE_CUST.ZE_CHNL and ZE_PROD.

```
Receiver Rule
Receiver Rule Variable Portions
Scale No Scaling
Distribution Rate Distribution Rate
Driver Result Portion
Advanced Tab / Periodic Processing Section
Periodic Counter
Fiscal Year
Total Periods 12
Period Financial Period
First 1
Last 4
Specific Period Processing none
Result
Distribution Financial Pe-
Channel Coverage Customer Rate riod Product Amount Portion
92H2 6989 AA 20 1 238 60 0.2
92H2 6990 AA 80 1 238 240 0.8
92H2 6982 DD 40 2 224 80 0.4
92H2 6981 DD 60 2 224 120 0.6
92H2 6989 AA 20 3 238 80 0.2
92H2 6990 AA 80 3 238 320 0.8
92H2 6982 DD 40 4 224 160 0.4
92H2 6981 DD 60 4 224 240 0.6
Procedure
1. ZE_AMT in the sender is allocated proportionally using ZE_DRBRT in the receiver as the distribution
percentage (for example, by color).
2. The following steps show hot to get the portion percentage:
1. Group ZE_CUST.ZE_CHNL and ZE_PROD. These are the fields that have the same characteristics from
our sender and receiver.
```

## syn-20 | page 166 | lexical overlap 0.5

**Q:** In the PaPM Calculation function, is there a worked example showing the "Absolute" calculation type applied with selection conditions on two rules, and which input data does it start from?

**A:** The example "Calculation Scenario with Condition" shows how the "Absolute" calculation type filters out values where the selection conditions are met for both rules and calculates a premium from the formula. It uses the "CA - Absolute and Relative Table" as input, with the columns Channel, Account, Customer, Product, Quantity and Amount.

```
1.4.2.2.1.1 Example: Calculation Scenario with Condition
This scenario shows how the “Absolute” calculation type filters out values where the selection conditions are
met for both rules and how it calculates the premium based on the formula used.
Input
This is the table that will be used as an input function:
CA - Absolute and Relative Table
Channel Account Customer Product Quantity Amount
90AH3 3 CN003 PROD03 15 62.5
90AH04 1 CN001 PROD02 89 250
90AH01 2 CN004 PROD03 99 206.25
90AH04 3 CN006 PROD01 112 132.5
90AH05 3 CN010 PROD03 55 20
90AH01 1 CN001 PROD01 76 125
90AH02 2 CN002 PROD01 80 143.75
90AH02 1 CN004 PROD01 103 175
90AH05 1 CN009 PROD02 126 70.63
90AH04 1 CN001 PROD02 17 100
90AH05 1 CN002 PROD02 13 75
90AH05 1 CN007 PROD01 40 44.75
90AH02 2 CN002 PROD01 20 57.5
90AH03 3 CN005 PROD01 108 153.13
90AH05 1 CN007 PROD01 117 111.88
90AH01 2 CN004 PROD03 15 82.5
90AH03 3 CN005 PROD01 10 61.25
90AH05 1 CN009 PROD02 75 28.25
90AH02 1 CN004 PROD01 13 70
90AH05 1 CN002 PROD02 94 187.5
```

## syn-21 | page 181 | lexical overlap 0.31

**Q:** I'm building an Excel-based calculation rule in PAPM and the Input and Result worksheets only show a zero row without my actual records. Should I type test values into those sheets, and will the system use them when the function actually runs?

**A:** The Excel tabs don't display the records from the input table, so it is recommended to add dummy data there to test the formula logic. This data is used only for modeling and is not considered in the calculation at system runtime, because the system still takes the data from the Input Model Table.

```
the Signature section.
Customer Product Quantity Amount Total Amount
0 0 0
Both the Input and the Result tab contains the table above.
 Note
The tabs do not show the data records from the input table. We recommend adding dummy data in the
Excel tabs to test the Excel formula logic. These data are only used for modeling purposes and are not
considered in the calculation during system runtime.
The Parameter tab shows the table below. You can manually enter dummy data as input in the Parameter field.
This helps you understand the calculation of the formula that is to be created on the Result tab.
Parameter Tab
Parameter Description Value
PKF_DISC Discount Parameter 0
The table below shows the dummy data for the tabs:
Input Tab
Total Discounted
Customer Product Quantity Amount Total Amount Amount
ARR21 SHOES 143 300 0 0
 Note
Even though dummy data is maintained on the Input tab, the system still captures the data from the Input
Model Table.
SAP Profitability and Performance Management
```

## syn-22 | page 190 | lexical overlap 0.57

**Q:** In the Formula function example that looks up a discount percentage from an imported file, how is the extra discount column in the output calculated, and why are all the input records processed even though there's only a single formula line?

**A:** The additional Total Discount field multiplies Quantity by Amount and applies the value looked up from the Discount Percentage table (the imported file data). All input records are processed because the fields are maintained in the Granularity fields of the Signature section, even though only one formula line exists.

```
Final Output
Final Output
Customer Product Quantity Amount Total Discount
CUST01 PROD05 15 62.50 243.75
CUST02 PROD04 89 250.00 6,007.50
CUST03 PROD03 99 206.25 5,717.25
CUST04 PROD02 112 132.50 4,303.60
CUST05 PROD01 55 20.00 330.00
The first four fields (Customer, Product, Quantity, and Amount) just capture the data from the Input Model
Table because the created formula has reference to the input. The additional field (Total Discount) multiplies
the product of Quantity and Amount with the value looked up from the Discount Percentage table (the data
from the imported file).
In this example, only one line of formula has been created. In any way, the function considers all records from
the input function for processing because the fields have been maintained in the Granularity fields from the
Signature section.
```

## syn-23 | page 196 | lexical overlap 0.53

**Q:** In PaPM's Unit Conversion function, which table does the Conversion Type field rely on to define how a quantity gets converted from one measurement unit to another?

**A:** The Conversion Type input field defines the unit conversion by using a predefined conversion table, which is table T006. The Value field holds the quantity that will be converted.

```
1.4.2.4.2 Unit Conversion
The Unit Conversion function can convert between different units of measurement for the same quantity based
on the conversion factors. Conversion factors are used to change the unit of a measured quantity without
changing its value.
Input Fields:
• Conversion Type: Defines the conversion of unit using a predefined conversion table (T006)
• Value: Value which will be converted
SAP Profitability and Performance Management
196 PUBLIC SAP Profitability and Performance Management
```

## syn-24 | page 206 | lexical overlap 0.45

**Q:** I'm setting up a Flow Modeling function in SAP PaPM and want to create a calculation rule with its lines. What is the sequence of steps on the Rules tab, and what details do I have to enter when adding a new rule?

**A:** On the Rule tab of the Flow Modeling function, choose Add, then enter Add Level, Rule, Rule Type and Description in the Add Details screen and choose OK. Next, select the created rule, go to its Rule Lines tab, choose Add, and enter the required information in the Add Details screen.

```
For more information about the Input tab, see Input [page 12].
3. Define the function to be used on the Lookup tab, if needed.
 Note
For more information about the Lookup tab, see Lookup [page 14].
4. Define the fields to be used on the Signature tab.
 Note
For more information about the Signature tab, see Signature [page 14].
5. On the Rules tab, each rule type represents an encapsulated and reusable logic for the calculation of data.
For more information about the available rule types, see the Key Features section above.
Proceed as follows to configure the rules:
1. On the Rule tab of your Flow Modeling function, choose  (Add).
2. The Add Details screen is displayed. Enter the following information:
• Add Level
• Rule
• Rule Type
• Description
3. Choose OK.
4. Select the created rule.
5. On the Rule Lines tab of the created rule, choose  (Add).
6. The Add Details screen is displayed. Enter the required information.
SAP Profitability and Performance Management
```

## syn-25 | page 219 | lexical overlap 0.36

**Q:** In the PaPM function that builds cash flow period patterns from a start date and day count convention, which numeric code do I enter in Period Unit when my Period To values are in quarters, and which codes apply for months and years?

**A:** Period Unit depends on the Period Type that was defined. Use 6 if Period To is in months, 11 if Period To indicates quarters, and 7 if Period To indicates years.

```
value that has been defined under
Period Type.
The following values are possible:
• 6 if Period To is in months
• 11 if Period To indicates quarters
• 7 if Period To indicates years
Expected Output
Expected Output for Period Type = Monthly
Start Date Contract ID Pattern KF Type Period To Period Unit Period To Result
2019-01-01 A MOV (Delta) 30 6 1
2019-01-01 A MOV (Delta) 60 6 2
2019-01-01 A MOV (Delta) 90 6 3
2019-01-01 A MOV (Delta) 120 6 4
Start Date Contract ID Pattern KF Type Period To Period Unit Period To Result
2019-01-01 B MOV (Delta) 30 6 1
SAP Profitability and Performance Management
SAP Profitability and Performance Management PUBLIC 219
```

## syn-26 | page 224 | lexical overlap 0.59

**Q:** In SAP PaPM Flow Modeling, what does the Term To Date rule type do, and can it handle both cumulative and delta-style pattern items differently?

**A:** Term To Date converts a set of cash flow terms into dates based on a given start date. Its configuration lets you choose between a default approach and one that applies different logic to balance-type (cumulative) pattern items and movement-type (delta) pattern items.

```
1.4.2.6.7 Example: Term To Date
Converts a given set of terms of cash flows into dates referencing a given start date.
The configuration allows you to choose between a default approach and an approach that applies different
logic to distinguish between pattern items that are of either balance type (cumulative factor/amount values) or
movement type (delta factors/amounts).
The examples below are both for patterns of type MOV (delta) and of type BAL (cumulative).
Input Data with Pattern MOV (Delta) Values
Start Date Contract ID Pattern KF Type Period Unit Period To
2019-01-01 A MOV (Delta) 6 1
2019-01-01 A MOV (Delta) 6 2
Start Date Contract ID Pattern KF Type Period Unit Period To
2019-01-06 B MOV (Delta) 6 1
2019-01-06 B MOV (Delta) 6 2
Start Date Contract ID Pattern KF Type Period Unit Period To
2019-01-01 C MOV (Delta) 6 1
2019-01-01 C MOV (Delta) 6 2
2019-01-01 C MOV (Delta) 6 3
2019-01-01 C MOV (Delta) 6 4
Flow Modeling Configuration
Rules (Tab)
```

## syn-27 | page 230 | lexical overlap 0.45

**Q:** In a Flow Modeling example where the Conversion Type is set to "Bal to Mov" and the Value Type Target is "Balance", what values does the output show for contract A's two balance periods, given that contract A is the one with the 90 and 120 inputs?

**A:** With Conversion Type "Bal to Mov" and Value Type Target "Balance", contract A's output shows Period To Value 90 with Result Amount USD 90 for pattern BAL 1, and Period To Value 120 with Result Amount USD 30 for pattern BAL 2. The Result Amount for BAL 2 is thus the change from the previous balance (120 − 90).

```
Start Date Contract ID Pattern KF Type Period To Value
2019-01-01 C BAL 1 USD 0
2019-01-01 C BAL 2 USD 120
The Flow Modeling configuration is the same; however, the Conversion Type is now “Bal to Mov” and Value Type
Target is now “Balance”.
Output Data BAL
Start Date Contract ID Pattern KF Type Period To Value Result Amount
2019-01-01 A BAL 1 USD 90 USD 90
2019-01-01 A BAL 2 USD 120 USD 30
2019-01-01 B BAL 1 USD 90 USD 90
2019-01-01 C BAL 1 USD 0 USD 0
2019-01-01 C BAL 2 USD 120 USD 120
```

## syn-28 | page 243 | lexical overlap 0.73

**Q:** In the Flow Modeling configuration for the Acknowledgement of Actuals (Same Period) rule, which fields do I need to assign for actuarial granularity, the business date, and the life cycle step, and what period type is used?

**A:** The actuarial granularity fields are Contract, Cost Category, and Coverage. The business date field is Key Date, and the life cycle step field is Cf Indicator. The period type is Monthly.

```
Q101 _Q10 -05-1 -06- _01 -01-3 -01-3 -05-1
DT 1DT 4 25 1 1 5
01 RIC_ COV 1010 1 2018 2018 2018 2018 2018 2018 400 EUR 2018 2018 2018
Q101 _Q10 -01- -05- -04- -05- -06- -07- -01-3 -01-3 -05-1
DT 1DT 01 25 25 25 25 25 1 1 5
Flow Modeling Configuration
Rule Description Rule Type State Rule Grouping Rule Ordering Selection
AOA Acknowledge- Acknowledge of Active
ment of Actuals Actuals
Same Period
Input Fields
*Actuarial Granularity Fields Contract, Cost Category, Coverage
*BT Granularity Fields BT ID
*First Hold Back Date Field Hold Back Date
*Second Hold Back Date Field Ra HBD
*Business Date Field Key Date
*Period Type Monthly
*Life Cycle Step Field Cf Indicator
CF Calculation Field CF Calc
Match Basis Same Period Match
SAP Profitability and Performance Management
SAP Profitability and Performance Management PUBLIC 243
```

## syn-29 | page 259 | lexical overlap 0.47

**Q:** I'm setting up a Clear Actual Dates rule in a Key Figure Formula rule in PaPM. What do the different values of the life cycle step field do, and which dates does each one wipe out?

**A:** The Life Cycle Step Field is a mandatory input with four codes. Code 1 deletes no dates. Code 2 deletes all dates except Due Date and Settled Date. Code 3 deletes all dates except Settled Date. Code 4 deletes all dates.

```
Flow Modeling Configuration
Rules
Rule Description Rule Type State Rule Grouping Rule Ordering Selection
CAD Clear Actual Clear Actual Active
Dates Dates
Rule Line
*Sec. Risk *Sec. Risk
*Life Cycle *Pr. Risk In- Incurred *Pr. Risk Re- Reported *Settled
Line Step Field curred Date Date ported Date Date *Due Date Date
L1 CF Indicator Pr. Incurred Incurred Date Pr. Reported Reported Due Date Settled Date
Date Date Date
Key Configuration Description
Field Meaning Notes
Line Identifier of the line Must be unique. A single Key Figure For-
mula Rule can run multiple lines.
Life Cycle Step Field Defines the logic for cancellation of the Mandatory input.
dates
Four codes are possible:
• 1: The dates are not deleted
• 2: All the dates are deleted except
Due Date and Settled Date
• 3: All the dates are deleted but
Settled Date
• 4: All the dates are deleted.
Pr. Risk Incurred Date of the pattern Mandatory input and output
Sec. Risk Incurred Date Date of the pattern Mandatory input and output
```

## syn-30 | page 267 | lexical overlap 0.62

**Q:** In the flow generation rule lines, what does the Periodic Fixed Amount Flow line compute, and how does the total payment behave across periods?

**A:** It calculates principal payments that, combined with interest payments, make up a fixed periodic total that is equal in every period, although the individual principal and interest amounts change constantly. The principal calculation is done in two steps, beginning with finding the amortizing factor for the n-th principal payment.

```
where “CF” is the (absolute) amount of the i-th cash flow, “T” is the respective maturity of the i-th cash
i i
flow and “r” is the yield to maturity of this financial instrument.
• Modified Duration is a measure of price sensitivity, defined as the percentage derivative of price with
respect to yield to maturity and compounding method. Under the same assumption, modified duration is
given by
• Fisher-Weil Duration: If rates from a zero coupon yield curve are used instead of the yield to maturity, the
Fisher-Weil duration is calculated with the same formula instead of Macaulay duration.
Flow Generation
The following rule lines are available:
• Periodic Fixed Amount Flow
Calculates principal payments that, in combination with interest payments, would compose a fixed
periodic total of equal value in all periods (but with constantly changing principal and interest values).
Principal calculation is done in two steps:
First, the amortizing factor for n-th principal payment (A ) is found:
n
```

## syn-31 | page 272 | lexical overlap 0.5

**Q:** How do I get to the Funds Transfer Pricing function so I can set it up in SAP PaPM, and which header fields do I have to fill in when configuring it?

**A:** In the client where PaPM is installed, choose SAP Menu > Profitability and Performance Management > Modeling > Start My Environments, then pick an existing environment in the browser window that opens and set up the function there. In edit mode, the required header fields to configure are Result Handling and Suppress initial Result.

```
Procedure
Function Access
Follow the steps below to access the Funds Transfer Pricing function:
1. In the client where SAP Profitability and Performance Management is installed, choose SAP Menu
Profitability and Performance Management Modeling Start My Environments .
2. The Environment screen appears in a separate browser window. Choose an existing environment and
continue. Within the environment, you can set up the newly added function.
Function Configuration
Follow the steps below to configure the Funds Transfer Pricing function:
1. In edit mode, configure the following required fields in the header.
• Result Handling
• Suppress initial Result
SAP Profitability and Performance Management
272 PUBLIC SAP Profitability and Performance Management
```

## syn-32 | page 281 | lexical overlap 0.53

**Q:** In the PaPM Join function, what does the Lookup Auto Predicate option do, and which rule does it fill the looked-up fields into?

**A:** Lookup Auto Predicate looks up fields and fills them in the first non-lookup rule where all common fields match those of the input function set on the Rule tab (e.g., Field 1 of Rule 1 = Field 1 of Rule 2). At least one field must be defined as a lookup field.

```
8. Lookup Auto Predicate: Looks up fields and fills them in the first non-lookup rule where all common fields
match those of the input function which is set on the Rule tab (this means, Field 1 of Rule 1 = Field 1 of Rule
2). At least one field needs to be defined as a lookup field.
Sub View
You can define further selections, formulas, aggregations and sorting orders for each rule.
Complex Selections
If required, you can define complex selections using formulas and SQL functions.
Join Predicates
You can define the predicate conditions for the matching for join and lookup rules here.
Complex Predicates
If required, you can enter complex on-predicates for join and lookup rules here using formulas and SQL
functions.
 Note
Fields coming from inputs are automatically considered during the join procedure. If the field is visible
onThese settings are only relevant for multiple join rules in which either non-null or non-initial values of the
```

## syn-33 | page 293 | lexical overlap 0.59

**Q:** In a PaPM setup where I use a lower-level rule with a product table as "From" and a higher-level rule has already enriched the product-material data, how does the system combine the two, and do I need to set the product-material table as an input function in the second rule?

**A:** The product table in the first rule ("From") performs a Left Outer Join with the Level 1 result (the enhanced Product - Material table), matching on product code, because results from a higher level are treated as input for the lower level. You don't need to set the Product - Material table as an input function for the second rule, since the system automatically detects that the input comes from the enhanced table and the join result is unaffected.

```
Interim Result (Level 1)
Product Code Materials Code # Request Order Material
P0001 M1011 5 Leather
P0001 M1010 2 Lace
P0002 M1009 1 Glass
P0002 M1011 3 Leather
P0005 M1012 10 Thread
P0006 M1011 30 Leather
Level 0 Processing
Level 0 Processing
The product table declared in the first rule (“From”) will now perform a Left Outer Join (for every matched
product code (PROD_CODE) entry) with the Level 1 result (enhanced Product - Material Table) since result
processed from a higher level will be considered as an input for the lower level.
 Note
Setting the Product - Material Table as an input function for the second rule will not affect the results of
the join since the system automatically detects that the input will be coming from the enhanced Product -
Material Table.
Product Table (Level 0, From) Interim Result (Level 1)
Product Product Materials # Request
Code Product Price Unit Code Code Order Material
P0001 Shoe 75 EUR P0001 M1011 5 Leather
P0002 Watch 300 EUR P0001 M1010 2 Lace
```

## syn-34 | page 302 | lexical overlap 0.4

**Q:** In the Line Item Valuation rule type, which SAP HANA SQL function does the Lag line type use to fetch a previous row's value, and what offset does it default to?

**A:** The Lag line type uses the SAP HANA SQL LAG function to return the value of a previous row within the same granularity set. The position is given by the offset value, which should be positive and defaults to "1".

```
• Formula: Applies certain formulas and SQL functions to key figures and/or characteristics.
• Lag: Uses SAP HANA SQL LAG function to return the value of a previous row where the position is specified
by the offset value in the same granularity set. The offset value should be positive, the default is “1”. Its
SAP Profitability and Performance Management
302 PUBLIC SAP Profitability and Performance Management
```

## syn-35 | page 307 | lexical overlap 0.54

**Q:** In a View function that loops over an input Writer function writing to a Model Table, I want the old data deleted on every pass of the loop. Which iteration types should I choose, and which model writer type do I have to use for that to work?

**A:** Use the iteration types "Application Server For Loop" or "Application Server Reverse For Loop" so that deletion happens in every iteration. This only works when the model writer type "Delete and Insert" is used.

```
procedure, such as in a process chain. An example is the Writer function that writes data to BW. In this
case, you can use the following iteration types:
• “Application Server For Loop”
• “Application Reverse For Loop”
 Note
If you want the deletion to happen in every iteration when you write to model data, use “Application
Server for Loop” and “Application Server Reverse For Loop”. This is only possible when the model
writer type “Delete and Insert” is used.
• The system bases the number of loops it executes on the limits that you define in the following fields:
• Low: Minimum number of loops to be executed
• High: Maximum number of loops to be executed
• Iteration Parameter: In the Iteration Parameter field, you need to enter a parameter that contains the
current loop number and thus makes it available for the input function as well.
• Early Exit Check: You can register an early exit check from the environment checks. This is applied to the
```

## syn-36 | page 316 | lexical overlap 0.32

**Q:** I'm setting up a File Adapter function that writes data out to a file. After I fill in the header, what are the remaining steps to get it configured and live, and how do I get the column-to-field mapping created?

**A:** After the header is set (File IO Type Export, File Format, Number of Threads), define the input function on the Input tab and the fields on the Signature tab. Then choose Field Mapping Proposal on the Mapping tab to generate the column-to-field mapping with field attributes, optionally define checks on the Checks tab, and finally Save and Activate.

```
1. In edit mode, configure the following required fields in the header. For more information about the header,
see the Key Features section above.
• File IO Type = “Export”
• File Format: Choose the file format configured in Environment File Formats
• Number of Threads
2. Define the input function to be used on the Input tab.
 Note
For more information about the Input tab, see Input [page 12].
3. Define the fields to be used on the Signature tab.
 Note
For more information about the Signature tab, see Signature [page 14].
4. Choose Field Mapping Proposal on the Mapping tab to generate the mapping of columns to field names
with field attributes.
5. Define the checks to be used on the Checks tab, if needed.
 Note
For more information about the Checks tab, see Checks [page 18].
6. Choose Save and then choose Activate.
Related Information
• For more information about common aspects of SAP Profitability and Performance Management
functions, see Concepts for Key Users [page 7].
```

## syn-37 | page 329 | lexical overlap 0.27

**Q:** When I post data to Finance General Ledger through a Remote Function Adapter in PaPM, which validation rules are applied to the records I send, and what kinds of functions can I use as the source of those records?

**A:** The Finance General Ledger RFA type uses the standard accounting interface (BAPI), so input records are validated according to the standard SAP Financial Accounting rules. The input function can be a Model Table, a Model View, or the result of another function, as long as it contains the necessary fields.

```
 Note
RFA type “Finance General Ledger” uses the standard accounting interface (BAPI). This means that the
input records are validated according to the standard SAP Financial Accounting rules.
The input function can be a Model Table, Model View, or the result of another function, provided it contains
the necessary fields.
 Example
Trans-
Debit Credit action Distri-
Sender Amoun Cur- Amoun Amoun bution
Posting Com- GL Ac- Cost Cost Item t rency t t Rate Object
Date pany count Center Center Text (ZE_DE Key (ZE_CR (ZE_TR (ZE_DI Key
(ZE_PO (ZE_FC (ZE_FG (ZE_CO (ZE_SC (ZE_IT BITAMT (ZE_CU EDITAM ANSAMT STRATE (ZE_OB
DAT) MP) LC) SCENT) NTR) MTXT) ) KY) T) ) ) JKEY)
201901 0001 00004 00000 00000 Admin 95000 EUR -95000 49500 19
01 05200 09200 09400 Cost 0
 Note
The entries used (for example for Company, GL Account, Cost Center, and so on) are for the
purposes of this example only.
Configuration
Configure the RFA function as follows:
1. In edit mode, choose the Add button.
```

## syn-38 | page 333 | lexical overlap 0.65

**Q:** I need to create several group reporting journal entries from PaPM in one go. Is there a way for the Remote Function Adapter to post multiple documents in a single call, and how do the line items get assigned to the right document?

**A:** Yes. The RFA type "Post Journal Entries for Group Reporting" can post multiple documents in one call by using the component control-grouping, which lets you assign the line items to their corresponding documents.

```
1.4.3.2.3 RFA Type: Post Journal Entries for Group
Reporting
The Remote Function Adapter type “Post Journal Entries for Group Reporting” enables you to post and
simulate journal entries in group reporting in SAP S/4HANA using the synchronous inbound service
API_CNSLDTNGRPJRNLENTR.
The service allows you to manually post journal entries to adjust financial reports, standardize entries,
and consolidate entries according to group requirements. You can specify the relevant consolidation group,
consolidation unit or consolidation unit pair as well as the local currency or group currency amounts for the
journal entry line items according to the version, fiscal year, posting period, and document type.
The RFA type “Post Journal Entries for Group Reporting” can post multiple documents in one single call
using the component control-grouping. This allows you to assign the line items to their corresponding
documents.
```

## syn-39 | page 347 | lexical overlap 0.74

**Q:** I'm using a Model BW output function with the Loading writer type, and the Model BW source is Environment. After the run, will the target end up in loading mode or planning mode for real-time load behavior?

**A:** It depends on the Editable option. If Editable is "No", the real-time load behavior is set to Loading mode after the run. If Editable is "Yes", it is set to Planning mode.

```
1.4.3.3.2.1 BW Writer Type "Loading"
Data is written using the data transfer process (DTP), and users who are editing data cannot continue to work
during this time.
The model writer type “Insert” is available. For more information, see Example: Model Writer Type "Insert"
[page 349].
During activation, the following BW objects are generated (for more information, see Runtime Attributes):
• Data source
• Transformation
• Data transfer process
• Based on the type of Model BW, required process types are added to the process chain.
Real-Time Load Behavior
1. If the Model BW source is “Environment”, after the run the real-time load behavior is set either to:
• Loading mode if the Editable option is “No”
• Planning mode if the Editable option is “Yes”.
2. If the Model BW source is “Business Warehouse” and BW Infoprovider is “Planning ADSO”, the real-time
load behavior is always set to “Planning” mode after the run.
Activation of Data
```

## syn-40 | page 357 | lexical overlap 0.43

**Q:** In a PaPM process template, what is the difference between the performer and the reviewer set on an activity, and which principle governs the review step?

**A:** The performer is a team (a group of users) that works on the activity. The reviewer can also be a team; it reviews the activity in a workflow based on the Dual Control principle and can either approve or reject it.

```
Check” or “Excluding Check” to a process activity. The checks maintained here are used to validate the
activity result data during the run in the My Activities application. They also influence the Dual Control
activities Submit and Complete.
For more information about the impact of checks in My Activities, see Dual Control [page 362].
10.Start Date and End Date
In both fields, you need to define default values. These can be overwritten during process deployment.
11. Performer and Reviewer
The performer defines a team (group of users) that can work on an activity. The reviewer can also define a
team that has to review the activity in a workflow using the Dual Control [page 362] principle and can either
approve or reject it.
Parameters
Parameters are defined in the environment and can be registered here so that they are available for use in
process templates. They can influence the behavior of functions below the calculation unit at runtime.
 Example
```

## syn-41 | page 365 | lexical overlap 0.29

**Q:** In the activity approval workflow in SAP PaPM, which events trigger automatic email notifications, and who gets notified in each case?

**A:** Emails are sent when an activity is sent for approval (to the reviewer team), when it is approved (to both the performer and the reviewer team), and when it is rejected (to both the performer and the reviewer team).

```
As soon as activity A0002 has been approved, the status changes from “In Approval” to “Completed”:
Activity Status Previous Activity
A0001 Completed A0003
A0002 Completed A0003
A0003 Completed A0004
A0004 Completed
 Note
SAP Profitability and Performance Management sends email notifications in the following cases:
• Activity sent for approval, receiver is reviewer team
• Activity approved, receiver is both performer and reviewer team
• Activity rejected, receiver is both performer and reviewer team.
```

## syn-42 | page 371 | lexical overlap 0.43

**Q:** I'm building a query in SAP PaPM and want to add a calculated column that combines several key figures, like KF01 divided by the difference of KF02 and KF03. How should I write that expression, and which functions can I use?

**A:** Define it as a formula, with the operands and operators separated by spaces, for example KF01 / (KF02 – KF03). Only the functions available in the SAP BEx Query Designer are supported in formulas.

```
The following definitions are available:
• Characteristic: Can be added to a column or row definition.
• Key figure: Can be added to a column or row definition.
• Selection: You can define “restricted” columns or rows by choosing particular characteristic values. You
can also choose a key figure and restrict it to one or more characteristic values.
• Formula: Allows you to define any calculations that are executed during a report run. For example, the
summation of two or more fields or complex calculations using formula functions. Only the functions
available in the SAP BEx Query Designer are supported here.
 Note
When you define the formula, the operands and operators should be separated by spaces.
Example: KF01 / (KF02 – KF03)
 Note
Key figures, formulas and selections can only be included under a structure.
For each Characteristic the following settings are available:
• General
Displays the general properties of a field or characteristic when running a query:
```

## syn-43 | page 383 | lexical overlap 0.36

**Q:** My time-series forecast in the Machine Learning function is returning strange results and some repeated forecasted values. Which setting can I change on the Forecast rule to get more realistic output, and what should I change it to?

**A:** Change the Forecast Method field, which defaults to "Default", to either "Linear Regression" or "Exponential Smoothing". The default algorithm can sometimes generate unexpected results or duplicated forecasted values, and choosing one of these explicitly can give a more realistic result.

```
• End Date: Specifies the end date as a constant or parameter of the historical data
• Signal Field: Specifies the field from which the values are used for the forecast
• Excluded Fields: List of fields that are not relevant for the forecast, or those fields whose impact should be
excluded from the forecast
• Forecast Period: Period for which the forecast is executed
• Forecast Unit: Period unit for the number of periods (for example, year, quarter, or month)
• Forecast Method: Specifies the forecasting algorithm
 Note
The Forecast Method field, which is originally set to “Default”, may be explicitly changed to “Linear
Regression” or “Exponential Smoothing” to provide a more realistic result as it may happen at times
that the algorithm generates unexpected results or duplicated forecasted values.
• Positive Forecast: Defines whether only positive forecasted values are generated
• Segmented By: Defines which fields are segmented based on the input dataset in case of multiple
```

## syn-45 | page 396 | lexical overlap 0.41

**Q:** I want to group my records into segments in the Machine Learning function of PaPM. Which algorithm does the clustering rule type use, and what settings can I configure to limit how many groups it creates?

**A:** The Clustering rule type runs a k-means algorithm on the input data to partition it into clusters and assign each data point to a cluster. You can configure the Minimal Number of Cluster and Maximal Number of Cluster input fields, and you can also choose which fields (features) the algorithm considers.

```
1.4.6.1.2 Rule Type: Clustering
The Machine Learning function provides rule type Clustering to train a clustering model based on input data.
The goal of a clustering model is to find underlying structures in the input data, for example segmenting the
input data into multiple clusters, where each cluster contains data points that are similar to each other with
respect to observed features.
The clustering function runs a k-means algorithm on the input data to determine a partition into clusters.
This function then calculates which cluster each data point belongs to. You can choose explicitly which fields
(features) of the input data are to be considered by the algorithm. The model that is calculated is saved and
stored under a unique model ID for each segment.
Rule Input Fields
You can use the following input fields for configuration:
• Minimal Number of Cluster: Specifies the minimal number of clusters
• Maximal Number of Cluster: Specifies the maximum number of clusters
```

