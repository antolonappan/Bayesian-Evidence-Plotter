import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['text.usetex']=True
plt.rcParams.update({'font.size': 15})
############################################



class plotter():
    def __init__(self,model_file,evidence_file,plotlabel,linec='black',lw_ref=0.3,
                 lw_bf=0.2,bf_x=0.2,bf_y=0.2,color='color',ts=10):
        self.model_file = str(model_file)
        self.evidence_file=str(evidence_file)
        self.plotlabel=str(plotlabel)
        self.linec=str(linec)
        self.lw_ref=float(lw_ref)
        self.lw_bf=float(lw_bf)
        self.bf_x=float(bf_x)
        self.bf_y=float(bf_y)
        self.color=str(color)
        self.ts=int(ts)
        self.Jef_color={'Insignificant':'b', 'Significant':'#FFA500',
                        'Strong':'g', 'Decisive':'r'}
        self.Jef_black={'Insignificant':'k:', 'Significant':'k-',
                        'Strong':'k--', 'Decisive':'k-.'}
        self.Jef_marker={'Insignificant':'o', 'Significant':'o',
                        'Strong':'o', 'Decisive':'*'}
    
    
    def file_check_return(self):
        try:
            model = self.get_models_list()
            evidence = self.get_evidence_values()
        except IOError or UnboundLocalError:
            raise Exception(FileNotFoundError)
        if len(model) == len(evidence):
            return model, -evidence
        else:
            raise Exception('ValueMatchError')
    
    def jeffrey_scale(self, _bf_):
        _bf_=abs(_bf_)
        if _bf_ <= 1.0:
            return 'Insignificant'
        elif 1 < _bf_ <= 2.5:
            return 'Significant'
        elif 2.5 < _bf_ <= 5.0:
            return 'Strong'
        elif _bf_ > 5.0:
            return 'Decisive'

    def get_models_list(self):
        with open (self.model_file) as f:
              model = f.readlines()
        model = [x.strip() for x in model]
        return model


    def get_evidence_values(self):
        data = np.loadtxt(self.evidence_file)
        return -data

       
    def bayes_factor(self):
        bayesfactor=[]
        evidence = self.get_evidence_values()
        for i in range(1,len(self.get_models_list())):
            bayesfactor.append((evidence[0]-evidence[i]))
        return bayesfactor


    def plot(self):
        plt.clf()
        model, evidence = self.file_check_return()
        bf=self.bayes_factor()
        x=np.arange(1,len(self.get_models_list())+1)
         
        if self.color=='color':
          if self.linec=='colored': 
            plt.plot((x[0], x[-1]), (evidence[0], evidence[0]), 'k--',lw=self.lw_ref)
            for i in range(1,len(model)):
                plt.plot((x[i], x[i]), (evidence[0], evidence[i]), 
                         '%s'%self.Jef_color[self.jeffrey_scale(bf[i-1])] ,lw=self.lw_bf)
                
          elif self.linec=='black':
              plt.plot((x[0], x[-1]), (evidence[0], evidence[0]), 'k--',lw=self.lw_ref)
              for i in range(1,len(model)):
                  plt.plot((x[i], x[i]), (evidence[0], evidence[i]), 'k-',lw=self.lw_bf)

        elif self.color=='bw':
            plt.plot((x[0], x[-1]), (evidence[0], evidence[0]), 'k-',lw=self.lw_ref)
            for i in range(1,len(model)):
                plt.plot((x[i], x[i]), (evidence[0], evidence[i]),
                         '%s'%self.Jef_black[self.jeffrey_scale(bf[i-1])] ,lw=6*self.lw_bf)
            
            
        for i in range(len(bf)):
            if bf[i]<0:
                plt.text(x[i+1]-self.bf_x,evidence[0]+.4+self.bf_y,r'$-%.2f$'%-bf[i],rotation='vertical')
            else:
                plt.text(x[i+1]-self.bf_x,evidence[0]-self.bf_y,r'$%.2f$'%bf[i],rotation='vertical')
        plt.scatter(x[0], evidence[0], c='k')
        if self.color=='color':
          for i in range(len(bf)):
            plt.plot(x[i+1], evidence[i+1], marker=self.Jef_marker[self.jeffrey_scale(bf[i])],
                     c=self.Jef_color[self.jeffrey_scale(bf[i])])
        elif self.color=='bw':
          for i in range(len(bf)):
            plt.plot(x[i+1], evidence[i+1], marker=self.Jef_marker[self.jeffrey_scale(bf[i])],
                     c='k')        
        plt.xlim(.5, len(model)+.5)
        plt.ylim(min(evidence)-1.2, max(evidence)+1.2)
        plt.xticks(x, model, rotation='vertical')
        plt.ylabel(r'$Log\;Evidence(\mathcal{Z})$')
        plt.title(self.plotlabel, fontsize=self.ts)
 #       plt.title(r'$CMB+SNIa+BAO$'+'('+r'$\;WITHOUT\;Ly$'+'-'+ r'$\alpha$'+')'+r'$+GROWTH+H+SL$', fontsize=self.ts)

        plt.savefig('%s.eps'%self.plotlabel,bbox_inches='tight')
