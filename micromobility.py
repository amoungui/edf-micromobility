import streamlit as st
import pandas as pd
from pyxlsb import open_workbook as open_xlsb


#modification taille de la page
st.set_page_config(layout="wide")

st.title('EDF taux d\'utilisation/occupation de trottinettes ...')
st.write("\n\n")

filename = 'data/comptage-multimodal-comptages_trottinettes_binary.xlsb'

@st.cache
def load_data(nrows):
	df = []

	with open_xlsb(filename) as wb:
	    with wb.get_sheet(1) as sheet:
	        for row in sheet.rows():
	            df.append([item.v for item in row])

	df = pd.DataFrame(df[1:], columns=df[0])	
	return df.head(nrows) 	

st.write(load_data(1000))
st.write("\n\n")

#st.area_chart(load_data(1000))

