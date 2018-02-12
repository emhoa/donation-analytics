import sys, re, math, bisect

if len(sys.argv) != 4:
	print('Error: Require paths input-itcont input-percentile output-repeat-donors')
	quit()

with open(sys.argv[2], 'r') as fpt:
	try: percentile = float(fpt.read())
	except:
		print('Error: Percentile is not a number')
		quit()
	if percentile < 0.0 or percentile > 100.0:
		print('Error: Percentile should between 0 and 100')
		quit()

with open(sys.argv[1], 'r') as finput, open(sys.argv[3], 'w') as foutput: # Read percentile
	donor_dict = {}
	rep_donor = {}
	repdon_list = []
	repdon_total = {}

	while True:
		line = finput.readline()
		if not line: break
		entry = line.split("|") # Use data in 0,7,10,13,14,15
		if not entry[0] or not entry[14] or entry[15]: continue # CMTE_ID and TRANSACTION_AMT and OTHER_ID
		if not re.search(r'[A-Za-z]', entry[7]): continue # NAME
		if not re.match(r'^\d{5,}$', entry[10]): continue # ZIP_CODE
		if not re.match(r'^((1[0-2])|(0?[1-9]))(([12][0-9])|(3[01])|(0?[1-9]))\d{4}$', entry[13]): continue # TRANSACTION_DT
		CMTE_ID = entry[0]
		NAME = entry[7]
		ZIP_CODE = entry[10][:5]
		TRANSACTION_DT = int(entry[13][4:])
		TRANSACTION_AMT = int(round(float(entry[14])))
		
		id_string = NAME + ', ' + ZIP_CODE
		if id_string not in donor_dict:
			donor_dict[id_string] = TRANSACTION_DT
		elif donor_dict[id_string] < TRANSACTION_DT:
			try: rep_donor[TRANSACTION_DT]
			except: rep_donor[TRANSACTION_DT] = 0
			rep_donor[TRANSACTION_DT] += 1
			try: repdon_total[TRANSACTION_DT]
			except: repdon_total[TRANSACTION_DT] = 0
			repdon_total[TRANSACTION_DT] += TRANSACTION_AMT
			bisect.insort(repdon_list, TRANSACTION_AMT)
			pt_index = math.ceil(len(repdon_list) * percentile / 100) - 1
			print(CMTE_ID, '|', ZIP_CODE, '|', TRANSACTION_DT, '|', repdon_list[pt_index], '|', repdon_total[TRANSACTION_DT], '|', rep_donor[TRANSACTION_DT], sep='', file=foutput)
