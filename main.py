import sys
import pandas as pd
import numpy as np
from scipy import stats
import xlrd
#from ordereddict import OrderedDict
import collections
import math
import urllib, json
stdout = sys.stdout
reload(sys)
sys.setdefaultencoding('utf-8')
sys.stdout = stdout

## COMMON FUNCTIONS
def dcAddErrorToList(error_column, row, error_to_add,df):
	df.ix[int(row), 'row'] = str(row)
	if error_column in df.columns:
		# check if cell value is empty (nan)
		if(pd.isnull(df.ix[int(row), error_column])):
			# no data exists in cell so add error
	      		df.ix[int(row), error_column] = error_to_add
			print("Row: %s, Error To Add: %s" % (int(row),error_to_add))
		else:
			# a previous error was recorded so append to it
			# even though there may be data lets check to make sure it is not empty
			if str(df.ix[int(row), error_column]):
				#print("There is already a previous error recorded: %s" % str(df.ix[int(row), error_column]))
				df.ix[int(row), error_column] = str(df.ix[int(row), error_column]) + "," + error_to_add
				print("Row: %s, Error To Add: %s" % (int(row),error_to_add))
			else:
				#print("No error is recorded: %s" % str(df.ix[int(row), error_column]))
	      			df.ix[int(row), error_column] = error_to_add
				print("Row: %s, Error To Add: %s" % (int(row),error_to_add))
	else:
		df.ix[int(row), error_column] = error_to_add
		print("Row: %s, Error To Add: %s" % (int(row),error_to_add))
	return df

## WORKSPACE START ###
# place the bight13 toxicity data in a location that the application can access
df = pd.ExcelFile('./errors.xlsx')
# df = pd.read_excel('./station_occupation_test-drop-occupationtime.xls')

# get sheet names
df_tab_names = df.sheet_names

# create dictionary to hold dataframes
all_dataframes = collections.OrderedDict()

# loop through each sheet
count = 0
for tab in df_tab_names:
	tab_name = tab
    	### extract individual dataframes
    	tab = df.parse(tab)
        # if the sheet is blank skip to the next sheet
	if tab.empty:
		print('The application is skipping sheet "%s" because it is empty' % tab)
		continue
	# lowercase all column names
	tab.columns = [x.lower() for x in tab.columns]
    	### and put into dictionary object
    	all_dataframes[count] = tab
	### create tmp_row for tracking row numbers
	all_dataframes[count]['tmp_row'] = all_dataframes[count].index
	count = count + 1

### WORKSPACE END ###

### SUMMARY TABLE START ###
station_occ = all_dataframes[0]
trawl = all_dataframes[1]

### SUMMARY TABLE END ###
# Here are the checks:
#
# 1. Check Trawl/StartDepth is no more 10% off of StationOccupation/OccupationDepth - warning only
# merging the StationID
merge_trawl_sta = pd.merge(station_occ, trawl, on=['stationid'], how='inner')
# print(merge_Trawl_Sta)
# print(merge_Trawl_Sta.columns)
trawlStart_depth = merge_trawl_sta['startdepth']
occupation_depth = merge_trawl_sta['occupationdepth']
occEnd_depth = merge_trawl_sta['enddepth']
def calculatedPercentDepth(c1, c2, c3):
	perc_result_start = abs(c1 - c2)/c2*100
	merge_trawl_sta['start_percentagedepth'] = perc_result_start
	# print(df1['start_percentagedepth'])
	perc_result_end = abs(c3 - c2)/c2*100
	merge_trawl_sta['end_percentagedepth'] = perc_result_end
	return
calculatedPercentDepth(trawlStart_depth, occupation_depth, occEnd_depth )
# NaN is used as a placeholder for missing data consistently in pandas, consistency is good. I usually read/translate NaN as "missing". Also see the 'working with missing data' section in the docs.
merge_trawl_sta['start_percentagedepth'] = np.where(merge_trawl_sta['start_percentagedepth'] <= 10, merge_trawl_sta['start_percentagedepth'], np.NaN)
merge_trawl_sta['end_percentagedepth'] = np.where(merge_trawl_sta['end_percentagedepth'] <= 10, merge_trawl_sta['end_percentagedepth'], np.NaN)
print(merge_trawl_sta)
print('=================================')
# print(merge_trawl_sta.columns)
# merge_trawl_sta.groupby(columns)
merge_trawl_sta.to_csv('output.csv', sep='\t', encoding='utf-8')

# 	perc_result = abs(static_depth - occupation_depth)/occupation_depth*100
# 	merge_stID['PercentageDepth'] = perc_result
# 	#NaN is used as a placeholder for missing data consistently in pandas, consistency is good. I usually read/translate NaN as "missing". Also see the 'working with missing data' section in the docs.
# 	merge_stID['PercentageDepth'] = np.where(merge_stID['PercentageDepth'] <= 10, merge_stID['PercentageDepth'], np.NaN)
# 	print(merge_stID)
# 	print("======================")
# 	print("======================")
# 	# 2. Check Trawl/EndDepth is no more than 10% off of StationOccupation/OccupationDepth - warning only
# 	perc_result = abs(static_depth - occupation_depth)/occupation_depth*100
# 	merge_stID['PercentageDepth'] = perc_result
# 	merge_stID['PercentageDepth'] = np.where(merge_stID['PercentageDepth'] <= 10, merge_stID['PercentageDepth'], np.NaN)
# 	print(merge_stID)
# percentDepth(df1,df2)
