# -*- coding: utf-8 -*-
'''
Wenesday July 17, 2019
Stacy Bridges

a bearing decoder
- this script uses Manufacturer and ManufacturerID to decode ball bearing type
- first run uses only 4- and 5- digit SKF codes
'''

# GLOBALS  ---------------------------------------------------------
bearing_codes = [
	'0', '1', '2', '3', '4', '5', '6', '7', '8', 'C', 'N', 'QJ', 'T'
]
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
	manuf = ['FAF', 'SKF']
	mMat = ['3207', '3206']

	i = 0
	for item in manuf:
		lastTwo = ''
		bearing_attr = ''
		bearing_code = ''
		bearing_type = ''
		d = ''  # diameter

		if item == 'SKF':
			# get bearing type
			if mMat[i][0] == '3' and len(item) == 4:
				# get the bearing code
				bearing_code = '0'

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
			lastTwo = mMat[i]
			if lastTwo == '00': d = '10'
			elif lastTwo == '01': d = '12'
			elif lastTwo == '02': d = '15'
			elif lastTwo == '03': d = '17'
			else:
				d = lastTwo
				print(d)
				d = int(d)
				d = d * 5

			bearing_attr = str(d) + ' mm'
	i += 1

	# end program
	print('Done.')

if __name__ == '__main__': main()
