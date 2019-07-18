# -*- coding: utf-8 -*-
'''
Wenesday July 17, 2019
Stacy Bridges

bearing decoder
- this script uses Manufacturer and ManufacturerID to decode ball bearing type
- first run uses only 4- and 5- digit SKF codes
'''
# GLOBALS  ---------------------------------------------------------
bearing_codes = ['0', '1', '2', '3', '4', '5', '6', '7', '8', 'C', 'N', 'QJ', 'T']

bearing_types = [
	'Double row angular contact ball bearing',
	'Self-aligning ball bearing',
	'Spherical roller bearing',  # may also be thrust bearing
	'Tapered roller bearing',
	'Double row deep groove ball bearing',
	'Thrust ball bearing',
	'Single row deep groove ball bearing',
	'Single row angular contact ball bearing',
	'Cylindrical roller thrust bearing',
	'CARB toroidal roller bearing',
	'Cylindrical roller bearing',  # addtl letters identify no. rows & flange config
	'Four-point contact ball bearing',
	'Tapered roller bearing',  # in accordance with ISO 355'
]

# MAIN  ------------------------------------------------------------
def main():
	# 6207 FAF light deep groove ball bearing 85 mm
	# 6006 SKF extra light deep groove ball bearing 75mm
	manufs = ['FAF', 'SKF', 'NSK', 'SKF', 'SKF', 'SKF']
	mMats = ['3207', '3206', '303', '61704', 'NNF5005', 'QJ209' ]
	results = []

	i = 0
	for item in manufs:
		# local vars
		manuf = ''
		mMat = ''
		bearing_attr = ''
		bearing_type = ''
		bearing_code = ''
		lastTwo = ''
		d = ''  # diameter

		if item == 'SKF':
			# get manuf and mMat
			manuf = manufs[i]
			mMat = mMats[i]

			# get bearing code
			# Code 0
			if mMats[i][0] == '3' and len(item) == 4:
				bearing_code = '0'
			elif mMats[i][0] == '3' and len(item) == 5:
				bearing_code = '3'
			elif mMats[i][0] == 'N' and mMats[i][1] == 'N':
				bearing_code = 'NN'
			elif mMats[i][0] == 'Q' and mMats[i][1] == 'J':
				bearing_code = 'QJ'
			else:
				# if mMats starts with char in range 01 - 08, then code = char
				bearing_code = str(mMats[i][0])

			j = 0
			index = 0
			# use bearing code to get array index
			for code in bearing_codes:
				if code == bearing_code:
					index = j
				j += 1

			# use the array index to get the bearing type
			bearing_type = bearing_types[index]

			# get the bearing attribute
			#lastTwo = item[len(item)-2:len(item)]
			lastTwo = mMats[i][len(mMats[i])-2:len(mMats[i])]
			if lastTwo == '00': d = '10'
			elif lastTwo == '01': d = '12'
			elif lastTwo == '02': d = '15'
			elif lastTwo == '03': d = '17'
			else: d = int(lastTwo) * 5

			bearing_attr = 'd: ' + str(d) + ' mm'
			results.append([mMat, manuf, bearing_type, bearing_attr])

		i += 1

	# output to console
	print('OUTPUT FROM CODE RULES:  --------------------')
	for info in results:
		print(info)

	# end program
	print('Done.')

if __name__ == '__main__': main()