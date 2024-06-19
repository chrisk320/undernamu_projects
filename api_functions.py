import requests

API_KEY = "PHv7rqvg9a4Uu9o7Y1nd42FflWDHQYuocFRcvgit"

def search_openFDA_registrationlisting(search_field, search_term, limit):
    '''
    Function Explination:
        This function connects to the openFDA regestration and listing API and searches their database for records containing the search_term in the search_field, returning as many as many matches as the limit parameter allows.
        The openFDA registration and listing API contains the location of medical device establishments and the devices manufactured at those establishments. Owners or operators of places of business (also called establishments or facilities) that are involved in the production and distribution of medical devices intended for use in the United States are required to register annually with the FDA. This process is known as establishment registration. Most foreign and domestic establishments that are required to register with the FDA are also required to list the devices that are made there for commercial distribution.
        Key facts of the registration and listing API:
            Source of the data: Registration and Listing
            changes to the source data: openFDA annotates the original records with special fields and converts the data into JSON, which is a widely used machine readable format.
            Time period covered in this API: 2007 to present
            Frequency of API updates: Monthly
        The API returns individual results as JSON by default. The JSON object has two sections:
            meta: Metadata about the query, including a disclaimer, link to data license, last-updated date, and total matching records, if applicable.
            results: An array of matching results, dependent on which endpoint was queried.
    
    search_term perameter explination:
        To search for records containing a word, search_term should be set to that word as a string
        Advanced syntax:
            Spaces: Queries use the plus sign + in place of the space character. Wherever you would use a space character, use a plus sign instead.
            Grouping: To group several terms together, use parentheses ( ) and +OR+ or +AND+.
            Wildcard search: Wildcard queries return data that contain terms matching a wildcard pattern. A wildcard operator is a placeholder that matches one or more characters. At this point, openFDA supports the * ("star") wildcard operator, which matches zero or more characters. You can combine wildcard operators with other characters to create a wildcard pattern.
                Example: search_term = "child*"   This example query looks in the endpoint for items whose search_field contains words that begin with child, case insensitive. This will include drugs with brand names that contain "Child", "Children", "Childrens" among others.

    search_field peramater explination:
        If you don't specify a field to search, the API will search in every field.
        Harmonization: 
            Different datasets use different unique identifiers, which can make it difficult to find the same drug in each dataset.
            openFDA features harmonization on specific identifiers to make it easier to both search for and understand the drug products returned by API queries. These additional fields are attached to records in all categories.
            Limits of openFDA harmonization: Not all records have harmonized fields. Because the harmonization process requires an exact match, some drug products cannot be harmonized in this fashion - for instance, if the drug name is misspelled. Some drug products will have openfda sections, while others will never, if there was no match during the harmonization process. Conversely, searching in these fields will only return a subset of records from a given endpoint.
            Exaustive list of harmonized fields for the registration and listing endpoint:
                regulation_number
                device_name
                device_class
                medical_specialty_description
                k_number
                pma_number
        Exaustive list of possible values of the search_field parameter: (orginized by section, search_field value, type, description)
            Section search_field    value   Type    Description
            Registration    registration.status_code	string	Registration status code.  Value is one of the following 1 = Active 5 = Active awaiting assignment of registration number
            Registration	registration.initial_importer_flag	string	Identifies whether facility is an initial importer.  Value is one of the following Y = Yes N = No
            Registration	registration.reg_expiry_date_year	string	Year that registration expires (expires 12/31 of that year).
            Registration	registration.address_line_1	string	Facility or US agent address line 1.
            Registration	registration.address_line_2	string	Facility or US agent address line 2.
            Registration	registration.city	string	Facility or US agent city.  This is an .exact field. It has been indexed both as its exact string content, and also tokenized.
            Registration	registration.state_code	string	Facility or US agent US state or foreign state or province.
            Registration	registration.zip_code	string	Number of devices noted in the adverse event report. Almost always 1. May be empty if report_source_code contains Voluntary report.  This is an .exact field. It has been indexed both as its exact string content, and also tokenized.
            Registration	registration.iso_country_code	string	Facility or US agent Zip code.  This is an .exact field. It has been indexed both as its exact string content, and also tokenized.
            Registration	registration.name	string	Name associated with the facility or US agent.  This is an .exact field. It has been indexed both as its exact string content, and also tokenized.
            Registration	registration.postal_code	string	Facility foreign postal code.  This is an .exact field. It has been indexed both as its exact string content, and also tokenized.
            Registration	registration.fei_number	string	Facility identifier assigned to facility by the FDA Office of Regulatory Affairs.
            Registration	registration.registration_number	string	Facility identifier assigned to facility by the FDA Office of Regulatory Affairs.
            Owner operator	registration.owner_operator.owner_operator_number	string	Number assigned to Owner Operator by CDRH.
            Owner operator	registration.owner_operator.firm_name	string	Firm name of owner operator.  This is an .exact field. It has been indexed both as its exact string content, and also tokenized.
            Owner operator	registration.owner_operator.official_correspondent.first_name	string	Official correspondent first name.  This is an .exact field. It has been indexed both as its exact string content, and also tokenized.
            Owner operator	registration.owner_operator.official_correspondent.last_name	string	Official correspondent last name.  This is an .exact field. It has been indexed both as its exact string content, and also tokenized.
            Owner operator	registration.owner_operator.official_correspondent.middle_initial	string	Official correspondent middle initial.  This is an .exact field. It has been indexed both as its exact string content, and also tokenized.
            Owner operator	registration.owner_operator.official_correspondent.phone_number	string	Official correspondent phone number.  This is an .exact field. It has been indexed both as its exact string content, and also tokenized.eprocessed and reused.
            Owner operator	registration.owner_operator.official_correspondent.subaccount_company_name	string	Official correspondent company name (if different from owner operator company name).  This is an .exact field. It has been indexed both as its exact string content, and also tokenized.
            Owner operator	registration.owner_operator.contact_address.address_1	string	First line of address for owner operator.
            Owner operator	registration.owner_operator.contact_address.address_2	string	Second line of address for owner operator.
            Owner operator	registration.owner_operator.contact_address.city	string	Owner operator city.  This is an .exact field. It has been indexed both as its exact string content, and also tokenized.
            Owner operator	registration.owner_operator.contact_address.state_code	string	Owner operator state code.  This is an .exact field. It has been indexed both as its exact string content, and also tokenized.
            Owner operator	registration.owner_operator.contact_address.state_province	string	Owner operator postal code.  This is an .exact field. It has been indexed both as its exact string content, and also tokenized.
            Owner operator	registration.owner_operator.contact_address.postal_code	string	Owner operator country code.
            Owner operator	registration.owner_operator.contact_address.iso_country_code	string	US agent individual name.  This is an .exact field. It has been indexed both as its exact string content, and also tokenized.
            US Agent	registration.us_agent.name	string	Business name of US agent.  This is an .exact field. It has been indexed both as its exact string content, and also tokenized.
            US Agent	registration.us_agent.business_name	string	US agent address line 1.
            US Agent	registration.us_agent.address_line_1	string	US agent address line 2.
            US Agent	registration.us_agent.address_line_2	string	US agent city.  This is an .exact field. It has been indexed both as its exact string content, and also tokenized.
            US Agent	registration.us_agent.city	string	US agent zip code.  This is an .exact field. It has been indexed both as its exact string content, and also tokenized.
            Identification	registration.us_agent.state_code	string	US agent US state or foreign state or province.
            Identification	registration.us_agent.zip_code	string	US agent zip code.  This is an .exact field. It has been indexed both as its exact string content, and also tokenized.
            Use of Device	registration.us_agent.postal_code	string	US agent country code.  This is an .exact field. It has been indexed both as its exact string content, and also tokenized.
            Use of Device	registration.us_agent.iso_country_code	string	Whether a device was implanted or not. May be either marked N or left empty if this was not applicable.  This is an .exact field. It has been indexed both as its exact string content, and also tokenized.
            Use of Device	registration.us_agent.bus_phone_area_code	string	US agent phone area code.
            Use of Device	registration.us_agent.bus_phone_extn	string	US agent phone extension.
            Use of Device	registration.us_agent.bus_phone_num	string	US agent phone number.  This is an .exact field. It has been indexed both as its exact string content, and also tokenized.
            Use of Device	registration.us_agent.fax_area_code	string	US agent fax area code.
            Use of Device	registration.us_agent.fax_num	string	US agent fax phone number.  This is an .exact field. It has been indexed both as its exact string content, and also tokenized.
            Use of Device	registration.us_agent.email_address	string	US agent email address.  This is an .exact field. It has been indexed both as its exact string content, and also tokenized.
            Proprietary names	proprietary_name	string	Proprietary or brand name or model number a product is marketed under.  This is an .exact field. It has been indexed both as its exact string content, and also tokenized.
            Establishment types	establishment_type	string	Facility operation or activity, e.g. "Manufacturer" (short version).  This is an .exact field. It has been indexed both as its exact string content, and also tokenized. search=establishment_type:"FOO+BAR"  Value is one of the following Manufacture Medical Device = Manufacture Medical Device Manufacture Medical Device for Another Party (Contract Manufacturer) = Manufacture Medical Device for Another Party (Contract Manufacturer) Repack or Relabel Medical Device = Repack or Relabel Medical Device Develop Specifications But Do Not Manufacture At This Facility = Develop Specifications But Do Not Manufacture At This Facility Sterilize Medical Device for Another Party (Contract Sterilizer) = Sterilize Medical Device for Another Party (Contract Sterilizer) Export Device to the United States But Perform No Other Operation on Device = Export Device to the United States But Perform No Other Operation on Device Complaint File Establishment per 21 CFR 820.198 = Complaint File Establishment per 21 CFR 820.198 Remanufacture Medical Device = Remanufacture Medical Device Manufacture Device in the United States for Export Only = Manufacture Device in the United States for Export Only Reprocess Single-Use Device = Reprocess Single-Use Device Foreign Private Label Distributor = Foreign Private Label Distributor
            Products	k_number	string	FDA-assigned premarket notification number, including leading letters. Leading letters "BK" indicates 510(k) clearance, or Premarket Notification, cleared by Center for Biologics Evaluation and Research. Leading letters "DEN" indicates De Novo, or Evaluation of Automatic Class III Designation. Leading letter "K" indicates 510(k) clearance, or Premarket Notification.
            Products	pma_number	string	FDA-assigned premarket application number, including leading letters. Leading letter "D" indicates Product Development Protocol type of Premarket Approval. Leading letters "BP" indicates Premarket Approval by Center for Biologics Evaluation and Research. Leading letter "H" indicates Humanitarian Device Exemption approval. Leading letter "N" indicates New Drug Application. Early PMAs were approved as NDAs. Leading letter "P" indicates Premarket Approval.
            Products	products.created_date	string	Date listing was created (may be unreliable).
            Products	products.exempt	string	Flag indicating whether a device is exempt or not.  Value is one of the following Y = Yes N = No
            Products	products.owner_operator_number	string	Number assigned to Owner Operator by CDRH.
            Products	products.product_code	string	A three-letter identifier assigned to a device category. Assignment is based upon the medical device classification designated under 21 CFR Parts 862-892, and the technology and intended use of the device. Occasionally these codes are changed over time.
            OpenFDA fields	device_class	string	A risk based classification system for all medical devices ((Federal Food, Drug, and Cosmetic Act, section 513)  Value is one of the following 1 = Class I (low to moderate risk): general controls 2 = Class II (moderate to high risk): general controls and special controls 3 = Class III (high risk): general controls and Premarket Approval (PMA) U = Unclassified N = Not classified F = HDE
            OpenFDA fields	device name	string	This is the proprietary name, or trade name, of the cleared device.  This is an .exact field. It has been indexed both as its exact string content, and also tokenized.
            OpenFDA fields	fei_number	array of strings	Facility identifier assigned to facility by the FDA Office of Regulatory Affairs.
            OpenFDA fields	medical_specialty_description	string	Regulation Medical Specialty is assigned based on the regulation (e.g. 21 CFR Part 888 is Orthopedic Devices) which is why Class 3 devices lack the "Regulation Medical Specialty" field.  This is an .exact field. It has been indexed both as its exact string content, and also tokenized.
            OpenFDA fields	regulation_number	array of strings	The classification regulation in the Code of Federal Regulations (CFR) under which the device is identified, described, and formally classified (Code of Federal regulations Title 21, 862.00 through 892.00). The classification regulation covers various aspects of design, clinical evaluation, manufacturing, packaging, labeling, and postmarket surveillance of the specific medical device.

    understanding the output: 
        For search queries, the results section includes matching SPL reports returned by the API.
        Each SPL report consists of these major sections:
            Standard SPL fields, including unique identifiers.
            Product-specific fields, the order and contents of which are unique to each product.
            An openfda section: An annotation with additional product identifiers, such as UPC and brand name, of the drug products listed in the labeling.
    
    Sample input and output:

    '''
    url = f"https://api.fda.gov/device/registrationlisting.json?api_key={API_KEY}&search={search_field}:{search_term}&limit={limit}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: Unable to fetch data (status code: {response.status_code})")
        print(url)
        return None

def search_openFDA_druglabel(search_field, search_term, limit):
    '''
    Function Explination:
        This function connects to the openFDA drug label API and searches their database for records containing the search_term in the search_field, returning as many as many matches as the limit parameter allows.
        Drug manufacturers and distributors submit documentation about their products to FDA in the Structured Product Labeling (SPL) format. The openFDA drug product labeling API returns data from this dataset. The labeling is a 'living document' that changes over time to reflect increased knowledge about the safety and effectiveness of the drug. The openFDA drug product labels API returns data from these submissions for both prescription and over-the-counter (OTC) drugs. The labels are broken into sections, such as indications for use (prescription drugs) or purpose (OTC drugs), adverse reactions, and so forth. There is considerable variation between drug products in terms of these sections and their contents, since the information required for safe and effective use varies with the unique characteristics of each drug product.
        Key facts of the drug label API:
            Source of the data: FDA SPL files
            Changes to the source data: openFDA annotates the original records with special fields and converts the data into JSON, which is a widely used machine readable format.
            Time period covered in this API: The bulk of the data is from June 2009 (when labeling was first posted publicly in the SPL format) to the present. However, there are a small number of records from earlier than mid-2009.
            Frequency of API updates: Weekly
        The API returns individual results as JSON by default. The JSON object has two sections:
            meta: Metadata about the query, including a disclaimer, link to data license, last-updated date, and total matching records, if applicable.
            results: An array of matching results, dependent on which endpoint was queried.

    search_term perameter explination:
        To search for records containing a word, search_term should be set to that word as a string
        Advanced syntax:
            Spaces: Queries use the plus sign + in place of the space character. Wherever you would use a space character, use a plus sign instead.
            Grouping: To group several terms together, use parentheses ( ) and +OR+ or +AND+.
                Example: search_term = "(cetirizine+OR+loratadine+OR+diphenhydramine)"
            Wildcard search: Wildcard queries return data that contain terms matching a wildcard pattern. A wildcard operator is a placeholder that matches one or more characters. At this point, openFDA supports the * ("star") wildcard operator, which matches zero or more characters. You can combine wildcard operators with other characters to create a wildcard pattern.
                Example: search_term = "child*"   This example query looks in the endpoint for items whose search_field contains words that begin with child, case insensitive. This will include drugs with brand names that contain "Child", "Children", "Childrens" among others.

    search_field peramater explination:
        If you don't specify a field to search, the API will search in every field.
        Harmonization: 
            Different datasets use different unique identifiers, which can make it difficult to find the same drug in each dataset.
            openFDA features harmonization on specific identifiers to make it easier to both search for and understand the drug products returned by API queries. These additional fields are attached to records in all categories.
            Limits of openFDA harmonization: Not all records have harmonized fields. Because the harmonization process requires an exact match, some drug products cannot be harmonized in this fashion - for instance, if the drug name is misspelled. Some drug products will have openfda sections, while others will never, if there was no match during the harmonization process. Conversely, searching in these fields will only return a subset of records from a given endpoint.
            Exaustive list of harmonized fields for the data label endpoint:
                manufacturer_name
                unii
                Product Type
                spl_set_id
                route
                generic_name
                brand_name
                product_ndc
                substance_name
                spl_id
                package_ndc
                application_number
                rxcui
                pharm_class_moa
                pharm_class_epc
                pharm_class_cs
                nui
                pharm_class_pe
                is_original_packager
                upc
                original_packager_product_ndc      

        Exaustive list of possible values of the search_field parameter: (orginized by section, search_field value, type, description)
            Section	Field search_field value	Type	Description
            Abuse and overdosage	abuse	string	Information about the types of abuse that can occur with the drug and adverse reactions pertinent to those types of abuse, primarily based on human data. May include descriptions of particularly susceptible patient populations.
            Abuse and overdosage	abuse_table	string	Information about the types of abuse that can occur with the drug and adverse reactions pertinent to those types of abuse, primarily based on human data. May include descriptions of particularly susceptible patient populations.
            Abuse and overdosage	controlled_substance	string	Information about the schedule in which the drug is controlled by the Drug Enforcement Administration, if applicable.
            Abuse and overdosage	controlled_substance_table	string	Information about the schedule in which the drug is controlled by the Drug Enforcement Administration, if applicable.
            Abuse and overdosage	dependence	string	Information about characteristic effects resulting from both psychological and physical dependence that occur with the drug, the quantity of drug over a period of time that may lead to tolerance or dependence, details of adverse effects related to chronic abuse and the effects of abrupt withdrawl, procedures necessary to diagnose the dependent state, and principles of treating the effects of abrupt withdrawal.
            Abuse and overdosage	dependence_table	string	Information about characteristic effects resulting from both psychological and physical dependence that occur with the drug, the quantity of drug over a period of time that may lead to tolerance or dependence, details of adverse effects related to chronic abuse and the effects of abrupt withdrawl, procedures necessary to diagnose the dependent state, and principles of treating the effects of abrupt withdrawal.
            Abuse and overdosage	drug_abuse_and_dependence	string	Information about whether the drug is a controlled substance, the types of abuse that can occur with the drug, and adverse reactions pertinent to those types of abuse.
            Abuse and overdosage	drug_abuse_and_dependence_table	string	Information about whether the drug is a controlled substance, the types of abuse that can occur with the drug, and adverse reactions pertinent to those types of abuse.
            Abuse and overdosage	overdosage	string	Information about signs, symptoms, and laboratory findings of acute ovedosage and the general principles of overdose treatment.
            Abuse and overdosage	overdosage_table	string	Information about signs, symptoms, and laboratory findings of acute ovedosage and the general principles of overdose treatment.
            Adverse effects and interactions	adverse_reactions	string	Information about undesirable effects, reasonably associated with use of the drug, that may occur as part of the pharmacological action of the drug or may be unpredictable in its occurrence. Adverse reactions include those that occur with the drug, and if applicable, with drugs in the same pharmacologically active and chemically related class. There is considerable variation in the listing of adverse reactions. They may be categorized by organ system, by severity of reaction, by frequency, by toxicological mechanism, or by a combination of these.
            Adverse effects and interactions	adverse_reactions_table	string	Information about undesirable effects, reasonably associated with use of the drug, that may occur as part of the pharmacological action of the drug or may be unpredictable in its occurrence. Adverse reactions include those that occur with the drug, and if applicable, with drugs in the same pharmacologically active and chemically related class. There is considerable variation in the listing of adverse reactions. They may be categorized by organ system, by severity of reaction, by frequency, by toxicological mechanism, or by a combination of these.
            Adverse effects and interactions	drug_and_or_laboratory_test_interactions	string	Information about any known interference by the drug with laboratory tests.
            Adverse effects and interactions	drug_and_or_laboratory_test_interactions_table	string	Information about any known interference by the drug with laboratory tests.
            Adverse effects and interactions	drug_interactions	string	Information about and practical guidance on preventing clinically significant drug/drug and drug/food interactions that may occur in people taking the drug.
            Adverse effects and interactions	drug_interactions_table	string	Information about and practical guidance on preventing clinically significant drug/drug and drug/food interactions that may occur in people taking the drug.
            Clinical pharmacology	clinical_pharmacology	string	Information about the clinical pharmacology and actions of the drug in humans.
            Clinical pharmacology	clinical_pharmacology_table	string	Information about the clinical pharmacology and actions of the drug in humans.
            Clinical pharmacology	mechanism_of_action	string	Information about the established mechanism(s) of the drugus action in humans at various levels (for example receptor, membrane, tissue, organ, whole body). If the mechanism of action is not known, this field contains a statement about the lack of information.
            Clinical pharmacology	mechanism_of_action_table	string	Information about the established mechanism(s) of the drug's action in humans at various levels (for example receptor, membrane, tissue, organ, whole body). If the mechanism of action is not known, this field contains a statement about the lack of information.
            Clinical pharmacology	pharmacodynamics	string	Information about any biochemical or physiologic pharmacologic effects of the drug or active metabolites related to the drug's clinical effect in preventing, diagnosing, mitigating, curing, or treating disease, or those related to adverse effects or toxicity.
            Clinical pharmacology	pharmacodynamics_table	string	Information about any biochemical or physiologic pharmacologic effects of the drug or active metabolites related to the drug's clinical effect in preventing, diagnosing, mitigating, curing, or treating disease, or those related to adverse effects or toxicity.
            Clinical pharmacology	pharmacokinetics	string	Information about the clinically significant pharmacokinetics of a drug or active metabolites, for instance pertinent absorption, distribution, metabolism, and excretion parameters.
            Clinical pharmacology	pharmacokinetics_table	string	Information about the clinically significant pharmacokinetics of a drug or active metabolites, for instance pertinent absorption, distribution, metabolism, and excretion parameters.
            ID and version	effective_time	string	Date reference to the particular version of the labeling document.
            ID and version	id	string	The document ID, A globally unique identifier (GUID) for the particular revision of a labeling document.
            ID and version	set_id	string	The Set ID, A globally unique identifier (GUID) for the labeling, stable across all versions or revisions.
            ID and version	version	string	A sequentially increasing number identifying the particular version of a document, starting with 1.
            Indications, usage, and dosage	active_ingredient	string	A list of the active, medicinal ingredients in the drug product.
            Indications, usage, and dosage	active_ingredient_table	string	A list of the active, medicinal ingredients in the drug product.
            Indications, usage, and dosage	contraindications	string	Information about situations in which the drug product is contraindicated or should not be used because the risk of use clearly outweighs any possible benefit, including the type and nature of reactions that have been reported.
            Indications, usage, and dosage	contraindications_table	string	Information about situations in which the drug product is contraindicated or should not be used because the risk of use clearly outweighs any possible benefit, including the type and nature of reactions that have been reported.
            Indications, usage, and dosage	description	string	General information about the drug product, including the proprietary and established name of the drug, the type of dosage form and route of administration to which the label applies, qualitative and quantitative ingredient information, the pharmacologic or therapeutic class of the drug, and the chemical name and structural formula of the drug.
            Indications, usage, and dosage	description_table	string	General information about the drug product, including the proprietary and established name of the drug, the type of dosage form and route of administration to which the label applies, qualitative and quantitative ingredient information, the pharmacologic or therapeutic class of the drug, and the chemical name and structural formula of the drug.
            Indications, usage, and dosage	dosage_and_administration	string	Information about the drug product's dosage and administration recommendations, including starting dose, dose range, titration regimens, and any other clinically sigificant information that affects dosing recommendations.
            Indications, usage, and dosage	dosage_and_administration_table	string	Information about the drug product's dosage and administration recommendations, including starting dose, dose range, titration regimens, and any other clinically sigificant information that affects dosing recommendations.
            Indications, usage, and dosage	dosage_forms_and_strengths	string	Information about all available dosage forms and strengths for the drug product to which the labeling applies. This field may contain descriptions of product appearance.
            Indications, usage, and dosage	dosage_forms_and_strengths_table	string	Information about all available dosage forms and strengths for the drug product to which the labeling applies. This field may contain descriptions of product appearance.
            Indications, usage, and dosage	inactive_ingredient	string	A list of inactive, non-medicinal ingredients in a drug product.
            Indications, usage, and dosage	inactive_ingredient_table	string	A list of inactive, non-medicinal ingredients in a drug product.
            Indications, usage, and dosage	indications_and_usage	string	A statement of each of the drug product's indications for use, such as for the treatment, prevention, mitigation, cure, or diagnosis of a disease or condition, or of a manifestation of a recognized disease or condition, or for the relief of symptoms associated with a recognized disease or condition. This field may also describe any relevant limitations of use.
            Indications, usage, and dosage	indications_and_usage_table	string	A statement of each of the drug product's indications for use, such as for the treatment, prevention, mitigation, cure, or diagnosis of a disease or condition, or of a manifestation of a recognized disease or condition, or for the relief of symptoms associated with a recognized disease or condition. This field may also describe any relevant limitations of use.
            Indications, usage, and dosage	purpose	string	Information about the drug product's indications for use.
            Indications, usage, and dosage	purpose_table	string	Information about the drug product's indications for use.
            Indications, usage, and dosage	spl_product_data_elements	string	Usually a list of ingredients in a drug product.
            Indications, usage, and dosage	spl_product_data_elements_table	string	Usually a list of ingredients in a drug product.
            Nonclinical toxicology	animal_pharmacology_and_or_toxicology	string	Information from studies of the drug in animals, if the data were not relevant to nor included in other parts of the labeling. Most labels do not contain this field.
            Nonclinical toxicology	animal_pharmacology_and_or_toxicology_table	string	Information from studies of the drug in animals, if the data were not relevant to nor included in other parts of the labeling. Most labels do not contain this field.
            Nonclinical toxicology	carcinogenesis_and_mutagenesis_and_impairment_of_fertility	string	Information about carcinogenic, mutagenic, or fertility impairment potential revealed by studies in animals. Information from human data about such potential is part of the warnings field.
            Nonclinical toxicology	carcinogenesis_and_mutagenesis_and_impairment_of_fertility_table	string	Information about carcinogenic, mutagenic, or fertility impairment potential revealed by studies in animals. Information from human data about such potential is part of the warnings field.
            Nonclinical toxicology	nonclinical_toxicology	string	Information about toxicology in non-human subjects.
            Nonclinical toxicology	nonclinical_toxicology_table	string	Information about toxicology in non-human subjects.
            OpenFDA fields	application_number	array of strings	This corresponds to the NDA, ANDA, or BLA number reported by the labeler for products which have the corresponding Marketing Category designated. If the designated Marketing Category is OTC Monograph Final or OTC Monograph Not Final, then the application number will be the CFR citation corresponding to the appropriate Monograph (e.g. "part 341"). For unapproved drugs, this field will be null.  Values follow this pattern: ^[BLA|ANDA|NDA]{3,4}[0-9]{6}$
            OpenFDA fields	brand_name	array of strings	Brand or trade name of the drug product.
            OpenFDA fields	generic_name	array of strings	Generic name(s) of the drug product.
            OpenFDA fields	manufacturer_name	array of strings	Name of manufacturer or company that makes this drug product, corresponding to the labeler code segment of the NDC.
            OpenFDA fields	nui	array of strings	Unique identifier applied to a drug concept within the National Drug File Reference Terminology (NDF-RT).  Values follow this pattern: ^[N][0-9]{10}$
            OpenFDA fields	package_ndc	array of strings	This number, known as the NDC, identifies the labeler, product, and trade package size. The first segment, the labeler code, is assigned by the FDA. A labeler is any firm that manufactures (including repackers or relabelers), or distributes (under its own name) the drug.  Values follow this pattern: ^[0-9]{5,4}-[0-9]{4,3}-[0-9]{1,2}$
            OpenFDA fields	pharm_class_cs	array of strings	Chemical structure classification of the drug product's pharmacologic class. Takes the form of the classification, followed by [Chemical/Ingredient] (such as Thiazides [Chemical/Ingredient] or `Antibodies, Monoclonal [Chemical/Ingredient].
            OpenFDA fields	pharm_class_epc	array of strings	Established pharmacologic class associated with an approved indication of an active moiety (generic drug) that the FDA has determined to be scientifically valid and clinically meaningful. Takes the form of the pharmacologic class, followed by [EPC] (such as Thiazide Diuretic [EPC] or Tumor Necrosis Factor Blocker [EPC].
            OpenFDA fields	pharm_class_moa	array of strings	Mechanism of action of the drug-molecular, subcellular, or cellular functional activity-of the drug's established pharmacologic class. Takes the form of the mechanism of action, followed by [MoA] (such as Calcium Channel Antagonists [MoA] or Tumor Necrosis Factor Receptor Blocking Activity [MoA].
            OpenFDA fields	pharm_class_pe	array of strings	Physiologic effect or pharmacodynamic effect-tissue, organ, or organ system level functional activity-of the drug's established pharmacologic class. Takes the form of the effect, followed by [PE] (such as Increased Diuresis [PE] or Decreased Cytokine Activity [PE].
            OpenFDA fields	product_ndc	array of strings	The labeler manufacturer code and product code segments of the NDC number, separated by a hyphen.  Values follow this pattern: ^[0-9]{5,4}-[0-9]{4,3}$
            OpenFDA fields	product_type	array of strings	
            OpenFDA fields	route	array of strings	The route of administation of the drug product.
            OpenFDA fields	rxcui	array of strings	The RxNorm Concept Unique Identifier. RxCUI is a unique number that describes a semantic concept about the drug product, including its ingredients, strength, and dose forms.  Values follow this pattern: ^[0-9]{6}$
            OpenFDA fields	spl_id	array of strings	Unique identifier for a particular version of a Structured Product Label for a product. Also referred to as the document ID.  Values follow this pattern: ^[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}$
            OpenFDA fields	spl_set_id	array of strings	Unique identifier for the Structured Product Label for a product, which is stable across versions of the label. Also referred to as the set ID.  Values follow this pattern: ^[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}$
            OpenFDA fields	substance_name	array of strings	The list of active ingredients of a drug product.
            OpenFDA fields	unii	array of strings	Unique Ingredient Identifier, which is a non-proprietary, free, unique, unambiguous, non-semantic, alphanumeric identifier based on a substance's molecular structure and/or descriptive information.  Values follow this pattern: ^[A-Z0-9]{10}$
            OpenFDA fields	upc	array of strings	Universal Product Code
            Other fields	laboratory_tests	string	Information on laboratory tests helpful in following the patient's response to the drug or in identifying possible adverse reactions. If appropriate, information may be provided on such factors as the range of normal and abnormal values expected in the particular situation and the recommended frequency with which tests should be performed before, during, and after therapy.
            Other fields	laboratory_tests_table	string	Information on laboratory tests helpful in following the patient's response to the drug or in identifying possible adverse reactions. If appropriate, information may be provided on such factors as the range of normal and abnormal values expected in the particular situation and the recommended frequency with which tests should be performed before, during, and after therapy.
            Other fields	microbiology	string	Documentation forthcoming.
            Other fields	microbiology_table	string	Documentation forthcoming.
            Other fields	package_label_principal_display_panel	string	The content of the principal display panel of the product package, usually including the product's name, dosage forms, and other key information about the drug product.
            Other fields	package_label_principal_display_panel_table	string	The content of the principal display panel of the product package, usually including the product's name, dosage forms, and other key information about the drug product.
            Other fields	recent_major_changes	string	A list of the section(s) that contain substantive changes that have been approved by FDA in the product labeling. The headings and subheadings, if appropriate, affected by the change are listed together with each section's identifying number and the month and year on which the change was incorporated in the labeling.
            Other fields	recent_major_changes_table	string	A list of the section(s) that contain substantive changes that have been approved by FDA in the product labeling. The headings and subheadings, if appropriate, affected by the change are listed together with each section's identifying number and the month and year on which the change was incorporated in the labeling.
            Other fields	spl_unclassified_section	string	Information not classified as belonging to one of the other fields. Approximately 40% of labeling with effective_time between June 2009 and August 2014 have information in this field.
            Other fields	spl_unclassified_section_table	string	Information not classified as belonging to one of the other fields. Approximately 40% of labeling with effective_time between June 2009 and August 2014 have information in this field.
            Patient information	ask_doctor	string	Information about when a doctor should be consulted about existing conditions or sumptoms before using the drug product, including all warnings for persons with certain preexisting conditions (excluding pregnancy) and all warnings for persons experiencing certain symptoms. The warnings under this heading are those intended only for situations in which consumers should not use the product until a doctor is consulted.
            Patient information	ask_doctor_or_pharmacist	string	Information about when a doctor or pharmacist should be consulted about drug/drug or drug/food interactions before using a drug product.
            Patient information	ask_doctor_or_pharmacist_table	string	Information about when a doctor or pharmacist should be consulted about drug/drug or drug/food interactions before using a drug product.
            Patient information	ask_doctor_table	string	Information about when a doctor should be consulted about existing conditions or sumptoms before using the drug product, including all warnings for persons with certain preexisting conditions (excluding pregnancy) and all warnings for persons experiencing certain symptoms. The warnings under this heading are those intended only for situations in which consumers should not use the product until a doctor is consulted.
            Patient information	do_not_use	string	Information about all contraindications for use. These contraindications are absolute and are intended for situations in which consumers should not use the product unless a prior diagnosis has been established by a doctor or for situations in which certain consumers should not use the product under any circumstances regardless of whether a doctor or health professional is consulted.
            Patient information	do_not_use_table	string	Information about all contraindications for use. These contraindications are absolute and are intended for situations in which consumers should not use the product unless a prior diagnosis has been established by a doctor or for situations in which certain consumers should not use the product under any circumstances regardless of whether a doctor or health professional is consulted.
            Patient information	information_for_owners_or_caregivers	string	Documentation forthcoming.
            Patient information	information_for_owners_or_caregivers_table	string	Documentation forthcoming.
            Patient information	information_for_patients	string	Information necessary for patients to use the drug safely and effectively, such as precautions concerning driving or the concomitant use of other substances that may have harmful additive effects.
            Patient information	information_for_patients_table	string	Information necessary for patients to use the drug safely and effectively, such as precautions concerning driving or the concomitant use of other substances that may have harmful additive effects.
            Patient information	instructions_for_use	string	Information about safe handling and use of the drug product.
            Patient information	instructions_for_use_table	string	Information about safe handling and use of the drug product.
            Patient information	keep_out_of_reach_of_children	string	Information pertaining to whether the product should be kept out of the reach of children, and instructions about what to do in the case of accidental contact or ingestion, if appropriate.
            Patient information	keep_out_of_reach_of_children_table	string	Information pertaining to whether the product should be kept out of the reach of children, and instructions about what to do in the case of accidental contact or ingestion, if appropriate.
            Patient information	other_safety_information	string	Information about safe use and handling of the product that may not have been specified in another field.
            Patient information	other_safety_information_table	string	Information about safe use and handling of the product that may not have been specified in another field.
            Patient information	patient_medication_information	string	Information or instructions to patients about safe use of the drug product, sometimes including a reference to a patient medication guide or counseling materials.
            Patient information	patient_medication_information_table	string	Information or instructions to patients about safe use of the drug product, sometimes including a reference to a patient medication guide or counseling materials.
            Patient information	questions	string	A telephone number of a source to answer questions about a drug product. Sometimes available days and times are also noted.
            Patient information	questions_table	string	A telephone number of a source to answer questions about a drug product. Sometimes available days and times are also noted.
            Patient information	spl_medguide	string	Information about the patient medication guide that accompanies the drug product. Certain drugs must be dispensed with an accompanying medication guide. This field may contain information about when to consult the medication guide and the contents of the medication guide.
            Patient information	spl_medguide_table	string	Information about the patient medication guide that accompanies the drug product. Certain drugs must be dispensed with an accompanying medication guide. This field may contain information about when to consult the medication guide and the contents of the medication guide.
            Patient information	spl_patient_package_insert	string	Information necessary for patients to use the drug safely and effectively.
            Patient information	spl_patient_package_insert_table	string	Information necessary for patients to use the drug safely and effectively.
            Patient information	stop_use	string	Information about when use of the drug product should be discontinued immediately and a doctor consulted. Includes information about any signs of toxicity or other reactions that would necessitate immediately discontinuing use of the product.
            Patient information	stop_use_table	string	Information about when use of the drug product should be discontinued immediately and a doctor consulted. Includes information about any signs of toxicity or other reactions that would necessitate immediately discontinuing use of the product.
            Patient information	when_using	string	Information about side effects that people may experience, and the substances (e.g. alcohol) or activities (e.g. operating machinery, driving a car) to avoid while using the drug product.
            Patient information	when_using_table	string	Information about side effects that people may experience, and the substances (e.g. alcohol) or activities (e.g. operating machinery, driving a car) to avoid while using the drug product.
            References	clinical_studies	string	This field may contain references to clinical studies in place of detailed discussion in other sections of the labeling.
            References	clinical_studies_table	string	This field may contain references to clinical studies in place of detailed discussion in other sections of the labeling.
            References	references	string	This field may contain references when prescription drug labeling must summarize or otherwise relay on a recommendation by an authoritative scientific body, or on a standardized methodology, scale, or technique, because the information is important to prescribing decisions.
            References	references_table	string	This field may contain references when prescription drug labeling must summarize or otherwise relay on a recommendation by an authoritative scientific body, or on a standardized methodology, scale, or technique, because the information is important to prescribing decisions.
            Special populations	geriatric_use	string	Information about any limitations on any geriatric indications, needs for specific monitoring, hazards associated with use of the drug in the geriatric population.
            Special populations	geriatric_use_table	string	Information about any limitations on any geriatric indications, needs for specific monitoring, hazards associated with use of the drug in the geriatric population.
            Special populations	labor_and_delivery	string	Information about the drug's use during labor or delivery, whether or not the use is stated in the indications section of the labeling, including the effect of the drug on the mother and fetus, on the duration of labor or delivery, on the possibility of delivery-related interventions, and the effect of the drug on the later growth, development, and functional maturation of the child.
            Special populations	labor_and_delivery_table	string	Information about the drug's use during labor or delivery, whether or not the use is stated in the indications section of the labeling, including the effect of the drug on the mother and fetus, on the duration of labor or delivery, on the possibility of delivery-related interventions, and the effect of the drug on the later growth, development, and functional maturation of the child.
            Special populations	nursing_mothers	string	Information about excretion of the drug in human milk and effects on the nursing infant, including pertinent adverse effects observed in animal offspring.
            Special populations	nursing_mothers_table	string	Information about excretion of the drug in human milk and effects on the nursing infant, including pertinent adverse effects observed in animal offspring.
            Special populations	pediatric_use	string	Information about any limitations on any pediatric indications, needs for specific monitoring, hazards associated with use of the drug in any subsets of the pediatric population (such as neonates, infants, children, or adolescents), differences between pediatric and adult responses to the drug, and other information related to the safe and effective pediatric use of the drug.
            Special populations	pediatric_use_table	string	Information about any limitations on any pediatric indications, needs for specific monitoring, hazards associated with use of the drug in any subsets of the pediatric population (such as neonates, infants, children, or adolescents), differences between pediatric and adult responses to the drug, and other information related to the safe and effective pediatric use of the drug.
            Special populations	pregnancy	string	Information about effects the drug may have on pregnant women or on a fetus. This field may be ommitted if the drug is not absorbed systemically and the drug is not known to have a potential for indirect harm to the fetus. It may contain information about the established pregnancy category classification for the drug. (That information is nominally listed in the teratogenic_effects field, but may be listed here instead.)
            Special populations	pregnancy_or_breast_feeding	string	Documentation forthcoming.
            Special populations	pregnancy_or_breast_feeding_table	string	Documentation forthcoming.
            Special populations	pregnancy_table	string	Information about effects the drug may have on pregnant women or on a fetus. This field may be ommitted if the drug is not absorbed systemically and the drug is not known to have a potential for indirect harm to the fetus. It may contain information about the established pregnancy category classification for the drug. (That information is nominally listed in the teratogenic_effects field, but may be listed here instead.)
            Special populations	teratogenic_effects	string	Pregnancy category A: Adequate and well-controlled studies in pregnant women have failed to demonstrate a risk to the fetus in the first trimester of pregnancy, and there is no evidence of a risk in later trimesters. Pregnancy category B: Animal reproduction studies have failed to demonstrate a risk to the fetus and there are no adequate and well-controlled studies in pregnant women. Pregnancy category C: Animal reproduction studies have shown an adverse effect on the fetus, there are no adequate and well-controlled studies in humans, and the benefits from the use of the drug in pregnant women may be acceptable despite its potential risks. Pregnancy category D: There is positive evidence of human fetal risk based on adverse reaction data from investigational or marketing experience or studies in humans, but the potential benefits from the use of the drug in pregnant women may be acceptable despite its potential risks (for example, if the drug is needed in a life-threatening situation or serious disease for which safer drugs cannot be used or are ineffective). Pregnancy category X: Studies in animals or humans have demonstrated fetal abnormalities or there is positive evidence of fetal risk based on adverse reaction reports from investigational or marketing experience, or both, and the risk of the use of the drug in a pregnant woman clearly outweighs any possible benefit (for example, safer drugs or other forms of therapy are available).
            Special populations	teratogenic_effects_table	string	Pregnancy category A: Adequate and well-controlled studies in pregnant women have failed to demonstrate a risk to the fetus in the first trimester of pregnancy, and there is no evidence of a risk in later trimesters. Pregnancy category B: Animal reproduction studies have failed to demonstrate a risk to the fetus and there are no adequate and well-controlled studies in pregnant women. Pregnancy category C: Animal reproduction studies have shown an adverse effect on the fetus, there are no adequate and well-controlled studies in humans, and the benefits from the use of the drug in pregnant women may be acceptable despite its potential risks. Pregnancy category D: There is positive evidence of human fetal risk based on adverse reaction data from investigational or marketing experience or studies in humans, but the potential benefits from the use of the drug in pregnant women may be acceptable despite its potential risks (for example, if the drug is needed in a life-threatening situation or serious disease for which safer drugs cannot be used or are ineffective). Pregnancy category X: Studies in animals or humans have demonstrated fetal abnormalities or there is positive evidence of fetal risk based on adverse reaction reports from investigational or marketing experience, or both, and the risk of the use of the drug in a pregnant woman clearly outweighs any possible benefit (for example, safer drugs or other forms of therapy are available).
            Special populations	use_in_specific_populations	string	Information about use of the drug by patients in specific populations, including pregnant women and nursing mothers, pediatric patients, and geriatric patients.
            Special populations	use_in_specific_populations_table	string	Information about use of the drug by patients in specific populations, including pregnant women and nursing mothers, pediatric patients, and geriatric patients.
            Supply, storage, and handling	how_supplied	string	Information about the available dosage forms to which the labeling applies, and for which the manufacturer or distributor is responsible. This field ordinarily includes the strength of the dosage form (in metric units), the units in which the dosage form is available for prescribing, appropriate information to facilitate identification of the dosage forms (such as shape, color, coating, scoring, and National Drug Code), and special handling and storage condition information.
            Supply, storage, and handling	how_supplied_table	string	Information about the available dosage forms to which the labeling applies, and for which the manufacturer or distributor is responsible. This field ordinarily includes the strength of the dosage form (in metric units), the units in which the dosage form is available for prescribing, appropriate information to facilitate identification of the dosage forms (such as shape, color, coating, scoring, and National Drug Code), and special handling and storage condition information.
            Supply, storage, and handling	safe_handling_warning	string	Documentation forthcoming.
            Supply, storage, and handling	safe_handling_warning_table	string	Documentation forthcoming.
            Supply, storage, and handling	storage_and_handling	string	Information about safe storage and handling of the drug product.
            Supply, storage, and handling	storage_and_handling_table	string	Information about safe storage and handling of the drug product.
            Warnings and precautions	boxed_warning	string	Information about contraindications or serious warnings, particularly those that may lead to death or serious injury.
            Warnings and precautions	boxed_warning_table	string	Information about contraindications or serious warnings, particularly those that may lead to death or serious injury.
            Warnings and precautions	general_precautions	string	Information about any special care to be exercised for safe and effective use of the drug.
            Warnings and precautions	general_precautions_table	string	Information about any special care to be exercised for safe and effective use of the drug.
            Warnings and precautions	precautions	string	Information about any special care to be exercised for safe and effective use of the drug.
            Warnings and precautions	precautions_table	string	Information about any special care to be exercised for safe and effective use of the drug.
            Warnings and precautions	user_safety_warnings	string	When a drug can pose a hazard to human health by contact, inhalation, ingestion, injection, or by any exposure, this field contains information which can prevent or decrease the possibility of harm.
            Warnings and precautions	user_safety_warnings_table	string	When a drug can pose a hazard to human health by contact, inhalation, ingestion, injection, or by any exposure, this field contains information which can prevent or decrease the possibility of harm.
            Warnings and precautions	warnings	string	Information about serious adverse reactions and potential safety hazards, including limitations in use imposed by those hazards and steps that should be taken if they occur.
            Warnings and precautions	warnings_table	string	Information about serious adverse reactions and potential safety hazards, including limitations in use imposed by those hazards and steps that should be taken if they occur.
                
    
        Exaustive list of all possible values of the route search field: (orginized by SPL acceptable term, code)
            SPL Acceptable Term   Code
            AURICULAR (OTIC)	C38192
            BUCCAL	C38193
            CONJUNCTIVAL	C38194
            CUTANEOUS	C38675
            DENTAL	C38197
            ELECTRO-OSMOSIS	C38633
            ENDOCERVICAL	C38205
            ENDOSINUSIAL	C38206
            ENDOTRACHEAL	C38208
            ENTERAL	C38209
            EPIDURAL	C38210
            EXTRA-AMNIOTIC	C38211
            EXTRACORPOREAL	C38212
            HEMODIALYSIS	C38200
            INFILTRATION	C38215
            INTERSTITIAL	C38219
            INTRA-ABDOMINAL	C38220
            INTRA-AMNIOTIC	C38221
            INTRA-ARTERIAL	C38222
            INTRA-ARTICULAR	C38223
            INTRABILIARY	C38224
            INTRABRONCHIAL	C38225
            INTRABURSAL	C38226
            INTRACAMERAL	C64984
            INTRACANALICULAR	C132737
            INTRACARDIAC	C38227
            INTRACARTILAGINOUS	C38228
            INTRACAUDAL	C38229
            INTRACAVERNOUS	C38230
            INTRACAVITARY	C38231
            INTRACEREBRAL	C38232
            INTRACISTERNAL	C38233
            INTRACORNEAL	C38234
            INTRACORONAL, DENTAL	C38217
            INTRACORONARY	C38218
            INTRACORPORUS CAVERNOSUM	C38235
            INTRACRANIAL	C38236
            INTRADERMAL	C38238
            INTRADISCAL	C38239
            INTRADUCTAL	C38240
            INTRADUODENAL	C38241
            INTRADURAL	C38242
            INTRAEPICARDIAL	C79144
            INTRAEPIDERMAL	C38243
            INTRAESOPHAGEAL	C38245
            INTRAGASTRIC	C38246
            INTRAGINGIVAL	C38247
            INTRAHEPATIC	C38248
            INTRAILEAL	C38249
            INTRALESIONAL	C38250
            INTRALINGUAL	C79138
            INTRALUMINAL	C38251
            INTRALYMPHATIC	C38252
            INTRAMAMMARY	C79137
            INTRAMEDULLARY	C38253
            INTRAMENINGEAL	C38254
            INTRAMUSCULAR	C28161
            INTRANODAL	C79141
            INTRAOCULAR	C38255
            INTRAOMENTUM	C79142
            INTRAOVARIAN	C38256
            INTRAPERICARDIAL	C38257
            INTRAPERITONEAL	C38258
            INTRAPLEURAL	C38259
            INTRAPROSTATIC	C38260
            INTRAPULMONARY	C38261
            INTRARUMINAL	C79139
            INTRASINAL	C38262
            INTRASPINAL	C38263
            INTRASYNOVIAL	C38264
            INTRATENDINOUS	C38265
            INTRATESTICULAR	C38266
            INTRATHECAL	C38267
            INTRATHORACIC	C38207
            INTRATUBULAR	C38268
            INTRATUMOR	C38269
            INTRATYMPANIC	C38270
            INTRAUTERINE	C38272
            INTRAVASCULAR	C38273
            INTRAVENOUS	C38276
            INTRAVENTRICULAR	C38277
            INTRAVESICAL	C38278
            INTRAVITREAL	C38280
            IONTOPHORESIS	C38203
            IRRIGATION	C38281
            LARYNGEAL	C38282
            NASAL	C38284
            NASOGASTRIC	C38285
            NOT APPLICABLE	C48623
            OCCLUSIVE DRESSING TECHNIQUE	C38286
            OPHTHALMIC	C38287
            ORAL	C38288
            OROPHARYNGEAL	C38289
            PARENTERAL	C38291
            PERCUTANEOUS	C38676
            PERIARTICULAR	C38292
            PERIDURAL	C38677
            PERINEURAL	C38293
            PERIODONTAL	C38294
            RECTAL	C38295
            RESPIRATORY (INHALATION)	C38216
            RETROBULBAR	C38296
            SOFT TISSUE	C38198
            SUBARACHNOID	C38297
            SUBCONJUNCTIVAL	C38298
            SUBCUTANEOUS	C38299
            SUBGINGIVAL	C65103
            SUBLINGUAL	C38300
            SUBMUCOSAL	C38301
            SUBRETINAL	C79143
            SUPRACHOROIDAL	C128997
            TOPICAL	C38304
            TRANSDERMAL	C38305
            TRANSENDOCARDIAL	C79145
            TRANSMUCOSAL	C38283
            TRANSPLACENTAL	C38307
            TRANSTRACHEAL	C38308
            TRANSTYMPANIC	C38309
            URETERAL	C38312
            URETHRAL	C38271
            VAGINAL	C38313

    understanding the output: 
        For search queries, the results section includes matching SPL reports returned by the API.
        Each SPL report consists of these major sections:
            Standard SPL fields, including unique identifiers.
            Product-specific fields, the order and contents of which are unique to each product.
            An openfda section: An annotation with additional product identifiers, such as UPC and brand name, of the drug products listed in the labeling.
    
    Sample input and output:

    '''
    url = f"https://api.fda.gov/drug/label.json?api_key={API_KEY}&search={search_field}:{search_term}&limit={limit}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: Unable to fetch data (status code: {response.status_code})")
        print(url)
        return None

def main():
    search_field = "products.product_code"
    search_term = "HQY"
    limit = 1
    data = search_openFDA_registrationlisting(search_field, search_term, limit)
    if data:
        print(data)
    else:
        print("No data retrieved or an error occurred.")


if __name__ == "__main__":
    main()
