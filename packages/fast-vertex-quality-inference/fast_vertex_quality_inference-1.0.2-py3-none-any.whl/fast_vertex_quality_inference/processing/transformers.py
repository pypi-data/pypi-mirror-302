import numpy as np
import pandas as pd
import numpy as np
from sklearn.preprocessing import PowerTransformer, QuantileTransformer
import uproot
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
import numpy as np
import pickle

_residualfrac_limit = 5.

def symlog(x, linthresh=1.0):
	sign = np.sign(x)
	abs_x = np.abs(x)
	return sign * np.log10(1 + abs_x / linthresh)

def invsymlog(y, linthresh=1.0):
	sign = np.sign(y)
	abs_y = np.abs(y)
	return sign * linthresh * (10**abs_y - 1)

class UpdatedTransformer:

	def __init__(self):
		
		self.qt_fit = False
		self.clip_value = 4.

	def fit(self, data_raw, column):

		self.column = column

		self.qt = QuantileTransformer(
			n_quantiles=500, output_distribution="normal"
		)

	def process(self, data_raw):
		
		try:
			data = data_raw.copy()
		except:
			# pass # value is likely a single element
			data = np.asarray(data_raw).astype('float64')

		if 'residualfrac' in self.column:
			limit = _residualfrac_limit
			data[np.where(data<(limit*-1.))] = -limit
			data[np.where(data>(limit))] = limit
			return symlog(data)/symlog(limit)

		if "TRUEORIGINVERTEX_X" in self.column or "TRUEORIGINVERTEX_Y" in self.column:
			return data

		if "DIRA" in self.column:
			where = np.where(np.isnan(data))
			where_not_nan = np.where(np.logical_not(np.isnan(data)))
			data[where] = np.amin(data[where_not_nan])

		# if self.column == "FD_B_plus_true_vertex":

		# 	plt.hist()

		if 'VTXISOBDTHARD' in self.column:
			data[np.where(data==-1)] = np.random.uniform(low=-1.1,high=-1.0,size=np.shape(data[np.where(data==-1)]))
		if 'FLIGHT' in self.column or 'FD' in self.column or 'IP' in self.column:
			data[np.where(data==0)] = np.random.uniform(low=-0.1,high=0.0,size=np.shape(data[np.where(data==0)]))

		if not self.qt_fit:
			self.qt.fit(data.reshape(-1, 1))
			self.qt_fit = True
		
		data = self.qt.transform(data.reshape(-1, 1))[:,0]
		data = np.clip(data, -self.clip_value, self.clip_value)
		data = data/self.clip_value

		return data

	def unprocess(self, data_raw):
			
		data = data_raw.copy()

		if 'residualfrac' in self.column:
			return invsymlog(data*symlog(_residualfrac_limit))

		if "TRUEORIGINVERTEX_X" in self.column or "TRUEORIGINVERTEX_Y" in self.column:
			return data

		data = data*self.clip_value

		data = self.qt.inverse_transform(data.reshape(-1, 1))[:,0]	

		if 'VTXISOBDTHARD' in self.column:
			data[np.where(data<-1)] = -1.
		if 'FLIGHT' in self.column or 'FD' in self.column or 'IP' in self.column:
			data[np.where(data<0)] = 0.

		return data


def transform_df(data, transformers):

    branches = list(data.keys())

    for branch in branches:	
        convert_units = False
        for P in ["P","PT","PX","PY","PZ"]:
            if f"_{P}_" in branch or branch[-(len(P)+1):] == f"_{P}":
                convert_units = True
        if "residualfrac" in branch: convert_units = False
        if convert_units:
            data[branch] = transformers[branch].process(np.asarray(data[branch])*1000.)
        else:
            data[branch] = transformers[branch].process(np.asarray(data[branch]))

    return data

def untransform_df(data, transformers):

    branches = list(data.keys())

    for branch in branches:	
        convert_units = False
        for P in ["P","PT","PX","PY","PZ"]:
            if f"_{P}_" in branch or branch[-(len(P)+1):] == f"_{P}":
                convert_units = True
        if "residualfrac" in branch: convert_units = False
        if convert_units:
            data[branch] = transformers[branch].unprocess(np.asarray(data[branch]))/1000.
        else:
            data[branch] = transformers[branch].unprocess(np.asarray(data[branch]))

    return data