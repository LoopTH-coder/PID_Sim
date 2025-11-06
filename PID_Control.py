# -*- coding: utf-8 -*-
"""
PID

@author: niazz
"""
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
pio.renderers.default='browser'

# %% Functions 
def pid(Kp, Ki, Kd, dt, sp, pv, lstpas_er, integ, integ_max):
    # Error
    er = sp - pv
    # Integral
    if integ > integ_max:
        integ = integ_max
    elif integ < 0:
        integ = 0.0
    else:
        integ += er * dt
    # Derivative 
    deriv = (er-lstpas_er)/dt
    cntrl = Kp*er + Ki*integ + Kd*deriv
    return cntrl, er, integ

# %%Time
st_time = 0.0125
e_time = 180.0
_t = 0.0

# %% PID Setup
s_point = 0.0
_Kp = 25.0
_Ki = 0.1
_Kd = 0.5
_integ_max = 1

# %% Last Pass
er_last = 0.0
c_pv = 0.0
p_integ = 0.0

# %% Data Storage
t = []
e = []
cntrl = []
integral = []
process_v = []
s_p = []

# %% Run
for i in range(0, round(e_time/st_time)):
    _t += st_time
    cntrl_out, er_out, integ_out = pid(_Kp, _Ki, _Kd,
                                       st_time, s_point,
                                       c_pv, er_last,
                                       p_integ, _integ_max)
    c_pv += cntrl_out * (1 - np.exp(-st_time/5.0))
    # Step change
    if _t >= 30:
        s_point = 1
    
    t.append(_t)
    er_last = er_out
    e.append(er_out)
    p_integ = integ_out
    integral.append(integ_out)
    cntrl.append(cntrl_out)
    s_p.append(s_point)
    process_v.append(c_pv)
# %% Plots
fig = px.scatter()

fig1 = go.Scatter(x=t, y=process_v, name = "Control Output")
fig2 = go.Scatter(x=t, y=s_p,  name="Setpoint")

fig.add_trace(fig1)
fig.add_trace(fig2)

fig.show()    
    