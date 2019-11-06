# UpdateCodes

A script that aids in updating Robin Descriptors when official CPT, ICD10, and HCPCS codes are updated.

## Usage

Open the Terminal (Launchpad > Search "Terminal"). By default, you'll start in your home directory, called `~`.

Using the command `cd` (change directory), navigate to the folder where the script is kept. You can use `ls` to list out all the files in your current directory.  

	example: cd ~/Desktop/code_updater

Gather the following files in `.csv` format and place them all in the `code_updater` folder: 
- 'Old' Official Codes and Descriptors
- New Official Codes and Descriptors
- 'Old' Robin Codes and Robin Descriptors
- Official Clinician Descriptors (named ClinicianDesciptor.csv)
- Robin Clinician Descriptors (named RobinClinicianDescriptor.csv)

Make sure your directory structure is as follows:

	├── update_codes.py 				# Script 
	├── old_official.csv  				# Old Official Codes. Schema: Code, Descriptor
	├── new_official.csv          		# New Official Codes. Schema: Code, Descriptor
	├── robin_descriptor.csv           	# Robin Codes. Schema: Code, Descriptor
	├── ClinicianDesciptor.csv 		`	# Official Clinician Descriptors. Schema: Concept Id, Code, Clinician Descriptor Id, Clinician Descriptor
	├── RobinClinicianDescriptor.csv    # Robin Clinician Descriptors. Schema: Concept Id, Code, Clinician Descriptor Id, Robin Descriptor, Category, Date Added, Date Changed
	├── txt2csv.py 						# For converting .txt to .csv.               
	└── README.md 						# You are here

Copy and paste the following in the terminal to run the example: 

	python update_codes.py 


Exit the script at any time by hitting Ctrl + C.

### User-Specified Inputs

To make this script robust to different types of codes, this script prompts the user in the terminal to confirm the type of codes being updated, the labels of the columns of the input files, and the current quarter. 

The script does not prompt the user for the Clinician Descriptor labels -- we assume that these will stay the same. 

### Outputs

	codes_added.csv 						# Schema: Concept Id, New Code, Clinician Descriptor Id, Clinician Descriptor, New Descriptor
	codes_changed.csv 						# Schema: Code, New Official Descriptor, Old Official Descriptor, Old Robin Descriptor
	codes_deleted.csv 						# Schema: Deleted Code, Deleted Descriptor
	codes_deleted_in_context.csv 			# Schema: Code, Descriptor, Deleted? (lists all old codes and indicates which ones have been deleted)
	new_internal_table.csv 					# Schema: Concept Id, Code, Clinician Descriptor Id, Robin Descriptor, Category, Date Added, Date Changed, Status
	