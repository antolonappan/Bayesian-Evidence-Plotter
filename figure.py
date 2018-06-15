from evidence_plotter import plotter as p
f=p('model_name.txt','bao+sl+h0.txt','BAO+TDSL+$H_0$',bf_y=.5, bf_x=.42,ts=12)
#f=p('model_name.txt','cmb+jla.txt',r'$CMB+SNIa$',lw_bf=.4,bf_x=.43,bf_y=.4,ts=13)
#f=p('model_name.txt','cmb+jla+bao.txt',r'$CMB+SNIa+BAO$',lw_bf=.4,bf_x=.42,bf_y=.5,ts=13)
#f=p('model_name.txt','all.txt',r'$CMB+SNIa+BAO+GROWTH+SL+H$',lw_bf=.4,bf_x=.45,bf_y=.7,ts=13)
f.plot()

