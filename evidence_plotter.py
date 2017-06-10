import numpy as np
import matplotlib.pyplot as plt
#import glob
plt.rcParams['text.usetex']=True
#listoffiles = glob.glob("*.txt")
############################################



class plotter():
    def __init__(self,model_file,evidence_file,plotlabel,lw_ref=0.3,lw_bf=0.2,bf_x=0.2,bf_y=0.2,color='r'):
        self.model_file = str(model_file)
        self.evidence_file=str(evidence_file)
        self.plotlabel=str(plotlabel)
        self.lw_ref=float(lw_ref)
        self.lw_bf=float(lw_bf)
        self.bf_x=float(bf_x)
        self.bf_y=float(bf_y)
        self.color=str(color)

    def get_models_list(self):

#        if self.model_file in listoffiles:
        try:
            with open (self.model_file) as f:
                model = f.readlines()
            model = [x.strip() for x in model]
            return model
#        else:
        except IOError or UnboundLocalError:
            print('FileError: %s not found in the directory!\n'%self.model_file)

        

    def get_evidence_values(self):

        try:
#        if self.evidence_file in listoffiles:
            data = np.loadtxt(self.evidence_file)
            return -data

        except IOError or UnboundLocalError:
            print('FileError: %s not found in the directory!\n'%self.evidence_file)
        
        
    def bayes_factor(self):
        bayesfactor=[]
        try:
            evidence = self.get_evidence_values()
            for i in range(1,len(self.get_models_list())):
                bayesfactor.append((evidence[0]-evidence[i]))
            return bayesfactor
        except TypeError:
            print('FileError')
    def plot(self):
        model=self.get_models_list()
        evidence = self.get_evidence_values()
        bf=self.bayes_factor()
        try:
            x=np.arange(1,len(self.get_models_list())+1)
            plt.plot((x[0], x[-1]), (-evidence[0], -evidence[0]), 'k--',lw=self.lw_ref)
            for i in range(1,len(model)):
                plt.plot((x[i], x[i]), (-evidence[0], -evidence[i]), 'k-',lw=self.lw_bf)
            for i in range(len(bf)):
                if bf[i]<0:
                    plt.text(x[i+1]-self.bf_x,-evidence[0]+self.bf_y,r'$%.2f$'%-bf[i],rotation='vertical')
                else:
                    plt.text(x[i+1]-self.bf_x,-evidence[0]-self.bf_y,r'$%.2f$'%bf[i],rotation='vertical')
            plt.plot(x, -evidence, '%so'%self.color,label=r'$%s$'%self.plotlabel)
            plt.xlim(.5, len(model)+.5)
            plt.xticks(x, model, rotation='vertical')
            plt.ylabel(r'$Log\;Evidence(\mathcal{Z})$')
            plt.legend(loc='down right')
        except TypeError:
            print('FileError')
        try:
            plt.savefig('%s.pdf'%self.plotlabel,bbox_inches='tight')
            plt.gcf().clear()
        except RuntimeError:
            pass
