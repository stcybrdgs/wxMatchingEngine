# -*- coding: utf-8 -*-
'''
Wenesday July 17, 2019
Stacy Bridges

a bearing decoder
- this script uses Manufacturer and ManufacturerID to decode ball bearing type
- first run uses only 4- and 5- digit SKF codes
'''

# GLOBALS  ---------------------------------------------------------
bearing_code = [
	'0', '1', '2', '3', '4', '5', '6', '7', '8', 'C', 'N', 'QJ', 'T'
]
bearing_type = [
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
	mMat = ['6207', '6006']

	i = 0
	for item in manuf:
		if manuf = 'SKF':
			if len(mMat[i]) == 4:
				pass
			if len(mMat[i]) == 5:
		prod_str = ''
		att_str = ''

		# get product string  ----------------



		# get attribute string -----------------

		if len(mMat) = 4:
			lastTwo = right(mMat, 2)
			if lastTwo == '00': d = 10
			if lastTwo == '01': d = 12
			if lastTwo == '02': d = 15
			if lastTwo == '03': d = 17
			else
			    d = int(lastTwo) * 5
		att_str = str(lastTwo) + ' mm'


		if len(mMat) = 5:

	# end program
	print('Done.')

if __name__ == '__main__': main()
