from evidence_plotter import plotter as p

# modelName file, Evidence Values, Title, ...... Please see the section in wiki 
f=p('models.txt','bao+sl+h0.txt','BAO+TDSL+$H_0$',bf_y=.5, bf_x=.42,ts=12)
f.plot()
