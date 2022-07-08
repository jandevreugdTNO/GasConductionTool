# -*- coding: utf-8 -*-
"""
Created on Thu Jul  7 19:42:17 2022

Gas Conduction


@author: Jan de Vreugd
"""

import numpy as np
import pandas as pd
import streamlit as st
import plotly.graph_objects as go

def gasdata(gas,Tav):
    data = {
      'Molar Mass': [0.04401,0.01703,0.01604,0.03199,0.028013,0.002016,0.004,0.1313,0.039948,2.88E-02],
      'Gamma': [1.304,1.307,1.31,1.401,1.404,1.41,1.66,1.66,1.668,1.4034],
      'Cp': [832,2188,2206,909,1036,14150,5225,0,524,1010.6],
      'AA': [-7.2150E-03,3.8110E-04,-1.8690E-03,-3.2730E-04,3.9190E-04,8.0990E-03,3.7220E-02,5.6667E-04,2.7140E-03,2.4806E-04],
      'BB': [8.0150E-05,5.3890E-05,8.7270E-05,9.9660E-05,9.8160E-05,6.6890E-04,3.8960E-04,1.2431E-05,5.5400E-05,9.8460E-05],
      'CC': [5.4770E-09,1.2270E-07,1.1790E-07,-3.7430E-08,-5.0670E-08,-4.1580E-07,-7.4500E-08,1.9325E-08,-2.1780E-08,-4.8022E-08],
      'DD': [-1.0530E-11,-3.6350E-11,-3.6140E-11,9.7320E-12,1.5040E-11,1.5620E-10,1.2900E-11,2.1300E-11,5.5280E-12,1.3978E-11],
      'Lambda': [1.6434E-02,2.5732E-02,3.2840E-02,2.5864E-02,2.5145E-02,1.7209E-01,1.4513E-01,6.3892E-03,1.7193E-02,2.5289E-02],
      'Tmin': [185,273,273,115,115,115,115,100,115,115],
      'Tmax': [1670,1670,1270,1470,1470,1470,1070,600,1470,1470],
      'alpha':[0.92,0.8,0.8,0.85,0.8,0.286,0.4,0.8,0.8,0.81]
    }
    df = pd.DataFrame(data, index = ['Carbon dioxide','Ammonia','Methane','Oxygen','Nitrogen','Hydrogen','Helium','Xenon','Argon', 'Air'])
    return df['Molar Mass'][gas], df['Gamma'][gas], df['Cp'][gas], df['AA'][gas], df['BB'][gas], df['CC'][gas], df['DD'][gas], df['Lambda'][gas],df['Tmin'][gas], df['Tmax'][gas], df['alpha'][gas]

def main():
    st.set_page_config(layout="wide")
    with st.sidebar:
        st.title('Gas conduction calculation tool')
        st.write('info: jan.devreugd@tno.nl')
        
        st.header('Heat transfer at constant pressure:')
        gasses = ['Carbon dioxide','Ammonia','Methane','Oxygen','Nitrogen','Hydrogen','Helium','Xenon','Argon', 'Air']
        default_ix = gasses.index('Air')
        gas = st.selectbox('Select gas:',gasses,index=default_ix)
        T1 = st.number_input('T1 [K]:',value = 293)
        T2 = st.number_input('T2 [K]:',value = 292)
        Tav = (T1+T2)/2
        P = st.number_input('Gas pressure [Pa]:',value = 5)
        
        Mm, Gamma, Cp, AA, BB, CC, DD, Lambda, Tmin, Tmax, alpha = gasdata(gas,Tav)
        Kn = AA + BB*Tav + CC*Tav**2 + DD*Tav**3
        R0 = 8.314
        
        arange = st.slider('log (all separation) [m]',-10, 0, (-6,-3))
        a = np.logspace(arange[0],arange[1],10000)
        FreeLambda = (Gamma+1)*np.sqrt(R0/(2*np.pi*Mm*T2))/(2*(Gamma-1))
        Hg = alpha*FreeLambda*P*np.sqrt((T2/T1))*Kn/(Kn+a*alpha*FreeLambda*P*np.sqrt(T2/T1))
        
        st.markdown("""---""")
        
    with st.expander('gas data:'):    
        st.write('selected gas = ', gas)
        st.write('average temperature =', str(Tav) + 'K')
        st.write('Molar Mass = ', str(Mm) + 'kg')
        st.write('Gamma =', str(Gamma))
        st.write('Cp =', str(Cp))
        st.write('AA =', str(AA))
        st.write('BB =', str(BB))
        st.write('CC =', str(CC))
        st.write('DD =', str(DD))
        st.write('Lambda =', str(Lambda) + 'W/mK')
        st.write('Tmin =', str(Tmin) + 'K')
        st.write('Tmax =', str(Tmax) + 'K')
        st.write('thermal accomdation factor, alpha =', str(alpha))
        st.write('Kn =', str(Kn))
    
    col1, col2 = st.columns(2)
    with col1:
        fig=go.Figure()
        #fig = fig.add_trace(go.Scatter(x=df.col2,y=df.col1,mode='markers',name='line1'))
        fig = fig.add_trace(go.Scatter(x=a,y=Hg))
        fig = fig.update_xaxes(title_text = 'wall separation [m]', type='log')
        fig = fig.update_yaxes(title_text = 'Heat transfer coefficient [W/m<sup>2</sup>K]', type='log')
        fig = fig.update_layout(title='gas pressure = ' + str(P) + 'Pa')
        st.plotly_chart(fig,use_container_width=False)
    with col2:
        fig=go.Figure()
        #fig = fig.add_trace(go.Scatter(x=df.col2,y=df.col1,mode='markers',name='line1'))
        fig = fig.add_trace(go.Scatter(x=a,y=a*Hg))
        fig = fig.update_xaxes(title_text = 'wall separation [m]', type='log')
        fig = fig.update_yaxes(title_text = 'Effective thermal conductivity [W/mK]', type='log')
        fig = fig.update_layout(title='gas pressure = ' + str(P) + 'Pa')
        st.plotly_chart(fig,use_container_width=False)
    st.markdown("""---""")
      
    with st.sidebar:
        a = st.number_input('wall separation [m]:',value = 1E-6,step=1E-8,format = '%e')    
        Prange = st.slider('log (gas pressure) [Pa]',-3, 8, (-2,6))
        P = np.logspace(Prange[0],Prange[1],10000)  
        
        FreeLambda = (Gamma+1)*np.sqrt(R0/(2*np.pi*Mm*T2))/(2*(Gamma-1))
        Hg = alpha*FreeLambda*P*np.sqrt((T2/T1))*Kn/(Kn+a*alpha*FreeLambda*P*np.sqrt(T2/T1))
    
    col1, col2 = st.columns(2)
    with col1:    
        fig=go.Figure()
        #fig = fig.add_trace(go.Scatter(x=df.col2,y=df.col1,mode='markers',name='line1'))
        fig = fig.add_trace(go.Scatter(x=P,y=Hg))
        fig = fig.update_xaxes(title_text = 'gas pressure [Pa]', type='log')
        fig = fig.update_yaxes(title_text = 'Heat transfer coefficient [W/m<sup>2</sup>K]', type='log')
        fig = fig.update_layout(title='wall separation = ' + str(a) + 'm')
        st.plotly_chart(fig,use_container_width=False)
        with col2:    
            fig=go.Figure()
            #fig = fig.add_trace(go.Scatter(x=df.col2,y=df.col1,mode='markers',name='line1'))
            fig = fig.add_trace(go.Scatter(x=P,y=a*Hg))
            fig = fig.update_xaxes(title_text = 'gas pressure [Pa]', type='log')
            fig = fig.update_yaxes(title_text = 'Heat transfer coefficient [W/mK]', type='log')
            fig = fig.update_layout(title='wall separation = ' + str(a) + 'm')
            st.plotly_chart(fig,use_container_width=False)
main()        