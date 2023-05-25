import streamlit as st
import sys
import csv
from datetime import datetime
import os
from io import BytesIO
import pandas as pd
from io import StringIO


class Ultra2Normal():
    def __init__(self, filename, user_name, patient_id, date=None):

        self.filename = filename
        self.user_name = user_name
        self.patient_id = patient_id

    def process(self):
        self.readfile()
        file = self.write_file()
        file = "%s\n#%s\n%s"%(user_name.split(' ')[0], str(patient_id), str(file))
        return file.encode('utf-8')

    def readfile(self):
        rows = []

        csvFile = csv.reader(self.filename)
        # displaying the contents of the CSV file
        for lines in csvFile:
            rows.append(lines)

        self.timestamps_raw = []
        self.timestamps_out = []
        self.values = []
        self.id = []
        self.type = []
        # converting proper timestamps and readings
        for ii, item in enumerate(rows[1:]):
            try:
                dt_raw = datetime.strptime(item[0], '%B %d %Y, %I:%M %p')
                dt_out = dt_raw.strftime('%Y/%m/%d %H:%M')
                self.timestamps_raw.append(dt_raw)
                self.timestamps_out.append(dt_out)
                self.values.append(int(item[1]))
                if ii == 0:
                    self.id.append(int(dt_raw.timestamp()) - 1680000000)
                else:
                    self.id.append(self.id[-1] + 1)
                self.type.append(0)
            except Exception as e:
                print("Failed parsing this row: %d" % ii)
                print(item)

    def write_file(self):
        print(len(self.id), len(self.timestamps_out), len(self.type), len(self.values))
        df = pd.DataFrame({'ID': self.id,
                           'Time': self.timestamps_out[1:],
                           'Record Type': self.type,
                           'Historic Glucose (mg/dL)': self.values})
        return df.to_csv(sep ='\t', index=False)



sys.path.append('/')

st.title("Ultra to Normal converter")

user_name = st.text_input("Enter your name (the one mentioned with Twin guys)", autocomplete='on')

patient_id = st.text_input("Enter your Twin id", autocomplete='on')

file = st.file_uploader("upload_file")

convert_clicked = st.button("Convert")

if convert_clicked:
    if file is not None:
        file = Ultra2Normal(StringIO(file.getvalue().decode("utf-8")), user_name, patient_id).process()
        date_today = datetime.now()
        filename = '%s-%s-%s.txt'%(patient_id, user_name.split(' ')[0], date_today.strftime('%d-%m-%Y'))
        st.download_button(
            label="Download file",
            data=file,
            file_name=filename,
            mime='text/csv',
        )
