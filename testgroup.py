from itertools import groupby
import pandas as pd
import datetime as dt

#gets today's date so that it is included in the file name
today = dt.datetime.today().strftime('%m%d%Y')  
output_file = 'maximums_{}.csv'.format(today)

today = pd.Timestamp('today')

#pulls in the appropriate dataframe, will have to change the file name as need
#again, there likely is a more elegant way to do this but I'm not sure of it
df = pd.read_csv('detection-2021_11_01-14_41_01.csv')

#this adds column names so that we can group later
df.columns = ['Date', 'Time', 'Persons Detected']

#groups the column by the time (by minute) and pulls out the maximum values and then resets the index
groupdf = df.groupby('Time')
maximums = groupdf.max()
maximums = maximums.reset_index()

#saves this as a new csv file
maximums.to_csv(output_file)