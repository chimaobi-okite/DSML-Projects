# -*- coding: utf-8 -*-
"""
Created on Thu Apr 28 11:07:52 2022

@author: Chimaobi Okite
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.header('st.write')
st.write('World *World!* :sunglasses:')

df = pd.DataFrame({
     'first column': [1, 2, 3, 4],
     'second column': [10, 20, 30, 40]
     })
st.write(df)

st.write('Below is a DataFrame:', df, 'Above is a dataframe.')

ax = plt.subplots()
ax.scatter(df['first column'], y=df['second column'])
st.pyplot(fig)