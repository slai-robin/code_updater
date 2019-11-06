import csv
import os
import sys

if not os.path.exists('output'):
    os.makedirs('output')

old_official = sys.argv[1]
new_official = sys.argv[2]
old_robin = sys.argv[3]

official_clinician_descriptor = 'ClinicianDescriptor.csv'
robin_clinician_descriptor = 'RobinClinicianDescriptor.csv'

old_codes_dict = {}
new_codes_dict = {}
old_robin_dict = {}
deleted_dict = {}
new_internal_table = {}
clinician_descriptor_dict = {}
robin_clinician_descriptor_dict = {}

new = {}
changed = {}
unchanged = {}
deleted = {}

################ PROMPT FOR LABELS #######################

# prompt for old official code
proceed = ""
code_type_confirmed = False
cpt = 'CPT '
hcpcs = 'HCPCS '
icd10 = 'ICD10 '

while not code_type_confirmed:
	proceed = raw_input('\nWhat type of code are you updating?\n \
							\n[a] CPT \
							\n[b] HCPCS \
							\n[c] ICD10 \
							\nAnswer: '
							)
	if proceed == 'a':
		code_type = cpt
		code_type_confirmed = True
	elif proceed == 'b':
		code_type = hcpcs
		code_type_confirmed = True
	elif proceed == 'c':
		code_type = icd10
		code_type_confirmed = True
	else:
		continue


old_off_code = code_type + 'Code'
old_off_desc = code_type + 'Description'
new_off_code = code_type + 'Code'
new_off_desc = code_type + 'Description'
robin_code = code_type + 'Code'
robin_desc = 'Robin Descriptor'

print '\n=============='

labels_confirmed = False

while not labels_confirmed:
	proceed = raw_input('\n[!] Please confirm the input files have exactly the following labels:\n\n' + 
					'Old Official Codes: ' + old_off_code + '\n' + 
					'Old Official Descriptor: ' + old_off_desc + '\n' + 
					'New Official Codes: ' + new_off_code+ '\n' + 
					'New Official Descriptor: ' + new_off_desc + '\n' + 
					'Old Robin Codes: ' + robin_code + '\n' + 
					'Old Robin Descriptor: ' + robin_desc + '\n' + 
					'\n[yes/no] ')
	if proceed == 'yes':
		labels_confirmed = True
		break

	old_off_code = raw_input('\nProvide the label for OLD official codes: ')
	old_off_desc = raw_input('Provide the label for OLD official descriptors: ')

	new_off_code = raw_input('Provide the label for NEW official codes: ')
	new_off_desc = raw_input('Provide the label for NEW official descriptors: ')

	robin_code = raw_input('Provide the label for Robin codes: ')
	robin_desc = raw_input('Provide the label for Robin descriptors: ')

	print '\n=============='

current_date = raw_input('\n[!] In what quarter will these codes become active? (ex. Q1 2020) Answer: ')

print "\n\nCalculating . . ."

################ GENERATE DICTIONARIES #######################

with open(old_official) as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
     	old_codes_dict[str(row[old_off_code])] = row[old_off_desc]
     	deleted_dict[str(row[old_off_code])] = row[old_off_desc]

with open(new_official) as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
     	new_codes_dict[str(row[new_off_code])] = row[new_off_desc]

with open(old_robin) as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
    	if row[robin_code] in old_robin_dict.keys():
    		old_robin_dict[str(row[robin_code])].append(row[robin_desc])
     	else: 
     		old_robin_dict[str(row[robin_code])] = [row[robin_desc]]

with open(official_clinician_descriptor) as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
 		clinician_descriptor_dict[str(row['CPT Code'])] = {
 			'Concept Id': row['Concept Id'],
 			'Clinician Descriptor Id': row['Clinician Descriptor Id'],
 			'Clinician Descriptor': row['Clinician Descriptor']
 		}   

with open(robin_clinician_descriptor) as csvfile: 
    reader = csv.DictReader(csvfile)
    for row in reader:
 		robin_clinician_descriptor_dict[str(row['CPT Code'])] = {
 			'Concept Id': str(row['Concept Id']),
 			'Clinician Descriptor Id': str(row['Clinician Descriptor Id']),
 			'Robin Descriptor': row['Robin Descriptor'],
 			'Category': row['Category'],
 			'Date Added': row['Date Added'],
			'Date Changed': row['Date Changed']
 		}  

################ BIN #######################

for key in new_codes_dict.keys():
	if key not in old_codes_dict.keys(): 
		new[key] = new_codes_dict[key]
	else:
		if new_codes_dict[key] != old_codes_dict[key]: 
			changed[key] = new_codes_dict[key]
			deleted_dict.pop(key)
		else:
			unchanged[key] = new_codes_dict[key]
			deleted_dict.pop(key)
			#add to new internal

################ BUILD NEW INTERNAL TABLE #######################

for key in new.keys():
	CPT_code = key
	concept_id = ''
	clinician_descriptor_id = ''

	if key in clinician_descriptor_dict.keys():
		clinician_info = clinician_descriptor_dict[key] #OFFICIAL TABLE
		concept_id = clinician_info['Concept Id']
		clinician_descriptor_id =  clinician_info['Clinician Descriptor Id']

	new_internal_table[key] =  {
		'Concept Id':concept_id, 
		'CPT Code':CPT_code, 
		'Clinician Descriptor Id':clinician_descriptor_id, 
		'Robin Descriptor': '', 
		'Category': '', 
		'Date Added': current_date, 
		'Date Changed': '',
		'Status': 'New'
	}

for key in changed.keys():
	concept_id = ''
	CPT_code = key
	clinician_descriptor_id =  ''
	robin_descriptor = ''
	category = ''
	date_added = ''
	date_changed = current_date

	if key in robin_clinician_descriptor_dict.keys():
		clinician_info = robin_clinician_descriptor_dict[key] #INTERNAL TABLE
		concept_id = clinician_info['Concept Id']
		clinician_descriptor_id =  clinician_info['Clinician Descriptor Id']
		robin_descriptor = clinician_info['Robin Descriptor']
		category = clinician_info['Category']
		date_added = clinician_info['Date Added']
		date_changed = clinician_info['Date Changed']

	new_internal_table[key] =  {
		'Concept Id':concept_id, 
		'CPT Code':CPT_code, 
		'Clinician Descriptor Id':clinician_descriptor_id, 
		'Robin Descriptor': robin_descriptor, 
		'Category': category, 
		'Date Added': date_added, 
		'Date Changed': current_date,
		'Status': 'Changed'
		}

for key in unchanged.keys():
	concept_id = ''
	CPT_code = key
	clinician_descriptor_id =  ''
	robin_descriptor = ''
	category = ''
	date_added = ''
	date_changed = ''

	if key in robin_clinician_descriptor_dict.keys():
		clinician_info = robin_clinician_descriptor_dict[key] #INTERNAL TABLE
		concept_id = clinician_info['Concept Id']
		clinician_descriptor_id =  clinician_info['Clinician Descriptor Id']
		robin_descriptor = clinician_info['Robin Descriptor']
		category = clinician_info['Category']
		date_added = clinician_info['Date Added']
		date_changed = clinician_info['Date Changed']

	new_internal_table[key] =  {
		'Concept Id':concept_id, 
		'CPT Code':CPT_code, 
		'Clinician Descriptor Id':clinician_descriptor_id, 
		'Robin Descriptor': robin_descriptor, 
		'Category': category, 
		'Date Added': date_added, 
		'Date Changed': '',
		'Status': 'Unchanged'
		}

################ CREATE OUTPUT FILES #######################

with open('output/codes_added.csv', 'w') as csvfile:
	fieldnames = ['Concept Id', 'New Code', 'Clinician Descriptor Id', 'Clinician Descriptor', 'New Descriptor']
	writer = csv.DictWriter(csvfile, fieldnames)
	writer.writeheader()
	for key in sorted(new.keys()):
		if key in clinician_descriptor_dict.keys():
			clinician_info = clinician_descriptor_dict[key]
			writer.writerow({
				'Concept Id': clinician_info['Concept Id'],
				'New Code': key, 
				'Clinician Descriptor Id': clinician_info['Clinician Descriptor Id'],
				'Clinician Descriptor': clinician_info['Clinician Descriptor'],
				'New Descriptor': new[key]
				})
		else:
			writer.writerow({
				'Concept Id': '',
				'New Code': key, 
				'Clinician Descriptor Id': '',
				'Clinician Descriptor': '',
				'New Descriptor': new[key]
				})


with open('output/codes_changed.csv', 'w') as csvfile:
	fieldnames = ['Code', 'New Official Descriptor', 'Old Official Descriptor', 'Old Robin Descriptor']
	writer = csv.DictWriter(csvfile, fieldnames)
	writer.writeheader()
	for key in sorted(changed.keys()):
		old_robin_descriptor = ""
		if key in old_robin_dict.keys(): 
			old_robin_descriptor = old_robin_dict[key]
			for descriptor in old_robin_descriptor:
				writer.writerow({
					'Code': key, 
					'New Official Descriptor': changed[key], 
					'Old Official Descriptor': old_codes_dict[key], 
					'Old Robin Descriptor': descriptor
					})

		else:
			writer.writerow({
				'Code': key, 
				'New Official Descriptor': changed[key], 
				'Old Official Descriptor': old_codes_dict[key], 
				'Old Robin Descriptor': old_robin_descriptor
				})

with open('output/codes_deleted.csv', 'w') as csvfile:
	fieldnames = ['Deleted Code', 'Deleted Descriptor']
	writer = csv.DictWriter(csvfile, fieldnames)
	writer.writeheader()
	for key in sorted(deleted_dict.keys()):
		writer.writerow({
			'Deleted Code': key, 
			'Deleted Descriptor': deleted_dict[key]
			})

with open('output/codes_deleted_in_context.csv', 'w') as csvfile:
	fieldnames = ['Code', 'Descriptor', "Deleted?"]
	writer = csv.DictWriter(csvfile, fieldnames)
	writer.writeheader()
	for key in sorted(old_codes_dict.keys()):
		was_deleted = ''
		if key in deleted_dict.keys():
			was_deleted = 'DELETED'
		writer.writerow({
			'Code': key, 
			'Descriptor': old_codes_dict[key],
			'Deleted?': was_deleted
			})


with open('output/new_internal_table.csv', 'w') as csvfile:
	fieldnames = ['Concept Id', 'CPT Code', 'Clinician Descriptor Id', 'Robin Descriptor', 'Category', 'Date Added', 'Date Changed', 'Status'] 
	writer = csv.DictWriter(csvfile, fieldnames)
	writer.writeheader()

	for key in sorted(new_internal_table.keys()):
		code = new_internal_table[key]
		writer.writerow({ 
			'Concept Id': code['Concept Id'], 
			'CPT Code': key, 
			'Clinician Descriptor Id': code['Clinician Descriptor Id'], 
			'Robin Descriptor':code['Robin Descriptor'], 
			'Category':code['Category'], 
			'Date Added': code['Date Added'], 
			'Date Changed': code['Date Changed'],
			'Status': code['Status']
			})

################ TERMINAL OUTPUT #######################

print "\n==============================="
print "Number of codes added: ", len(new.keys())
print "Number of codes changed: ", len(changed.keys())
print "Number of codes deleted: ", len(deleted_dict.keys()) 
print "===============================\n"

