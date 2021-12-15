import streamlit as st
import pandas as pd
from pyxlsb import open_workbook as open_xlsb
import matplotlib.pyplot as plt

#modification taille de la page
st.set_page_config(layout="wide")

st.title('EDF taux d\'utilisation/occupation de trottinettes ...')
st.write("\n\n")

filename = 'data/comptage-multimodal-comptages_trottinettes_binary.xlsb'

@st.cache(allow_output_mutation=True)
def load_data(nrows):
	df = []

	with open_xlsb(filename) as wb:
	    with wb.get_sheet(1) as sheet:
	        for row in sheet.rows():
	            df.append([item.v for item in row])

	df = pd.DataFrame(df[1:], columns=df[0])
	data = df	
	return data.head(nrows) 	

data = load_data(1000)

def move_mode(df):
	data = df.loc[:, ['Mode déplacement', 'Nombre de véhicules']]
	data['Mode déplacement'] = data['Mode déplacement'].map({
														'2 roues motorisées':'2 roues motorisées',
	                            						'Autobus et autocars':'autobus/autocars',
	                            						'Trottinettes':'Trottinettes',
	                            						'Trottinettes + vélos':'Trottinettes',
	                            						'Véhicule lourds > 3.5t':'Véhicule lourds > 3.5t',
	                            						'Véhicule légers < 3.5t':'Véhicule légers < 3.5t',
	                            						'Vélos':'Vélos'},
	                            						na_action=None)
	d = data.groupby('Mode déplacement')['Mode déplacement'].value_counts()
	return d

dt = move_mode(data)
labels = ['2 roues motorisées', 'Trottinettes', 'Vélos', 'autobus/autocars']

def plotly_charts(df, labels):
	fig, ax = plt.subplots()

	box = ax.get_position()
	ax.set_position([box.x0, box.y0, box.width * 1.3, box.height])

	ax.pie(df, labels=labels, explode=(0, 0.02, 0, 0), autopct = "%0.2f%%")

	total = sum(df)
	plt.legend(
	    loc='upper left',
	    labels=['%s, %1.1f%%' % (
	        l, (float(s) / total) * 100) for l, s in zip(labels, df)],
	    prop={'size': 12},
	    bbox_to_anchor=(0.0, 1),
	    bbox_transform=fig.transFigure
	)

	return fig

def new_data(df):
	data = df.loc[:, ['Mode déplacement', 'Nombre de véhicules']]
	data['Mode déplacement'] = data['Mode déplacement'].map({
														'2 roues motorisées':'2 roues motorisées',
	                            						'Autobus et autocars':'autobus/autocars',
	                            						'Trottinettes':'Trottinettes',
	                            						'Trottinettes + vélos':'Trottinettes',
	                            						'Véhicule lourds > 3.5t':'Véhicule lourds > 3.5t',
	                            						'Véhicule légers < 3.5t':'Véhicule légers < 3.5t',
	                            						'Vélos':'Vélos'},
	                            						na_action=None)
	d = data['Mode déplacement'].value_counts()
	return d


def load_map_data(df):
	df['lat'], df['lon'] = df['Coordonnées Géo'].split(',', expand=True)
	return df
		

st.write(load_map_data(data)) # 
st.write("\n\n")
col1, col2 = st.columns(2)

with col1:
    st.header(" ")
    st.bar_chart(new_data(data))

with col2:
    st.header(" ")
    st.write(plotly_charts(dt, labels))