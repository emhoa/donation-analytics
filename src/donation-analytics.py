import sys, re, math, bisect

if len(sys.argv) != 4:
	print('Require: input-itcont-file input-percentile-file output-repeat-donors-file')
	quit()

with open(sys.argv[2], 'r') as fpt: # Read percentile
	percentile = int(fpt.read())

finput = open(sys.argv[1], 'r') # Read itcont file
foutput = open(sys.argv[3], 'w') # Open repeat-donors file

donor_dict = {}
rep_donor = 0
repdon_list = []
repdon_total = 0

while True:
	line = finput.readline()
	if not line: break
	entry = line.split("|") # Use data in 0,7,10,13,14,15
	if re.match(r'^C\d{8}$', entry[0]): CMTE_ID = entry[0]
	else: continue
	if re.match(r"^[A-Z][A-Za-z',. -]+$", entry[7]): NAME = entry[7]
	else: continue
	if re.match(r'^\d{5,}$', entry[10]): ZIP_CODE = entry[10][:5]
	else: continue
	if re.match(r'^((1[0-2])|(0?[1-9]))(([12][0-9])|(3[01])|(0?[1-9]))\d{4}', entry[13]): TRANSACTION_DT = int(entry[13][4:])
	else: continue
	if re.match(r'^(-?\d+)(\.\d+)?$', entry[14]): TRANSACTION_AMT = int(round(float(entry[14])))
	else: continue
	if entry[15]: continue # OTHER_ID
	
	id_string = NAME + ', ' + ZIP_CODE
	if id_string not in donor_dict:
		donor_dict[id_string] = TRANSACTION_DT
	elif donor_dict[id_string] < TRANSACTION_DT:
		rep_donor += 1
		repdon_total += TRANSACTION_AMT
		bisect.insort(repdon_list, TRANSACTION_AMT)
		pt_index = math.ceil(len(repdon_list) * percentile / 100) - 1
		print(CMTE_ID, '|', ZIP_CODE, '|', TRANSACTION_DT, '|', repdon_list[pt_index], '|', repdon_total, '|', rep_donor, sep='', file=foutput)

finput.close()
foutput.close()
