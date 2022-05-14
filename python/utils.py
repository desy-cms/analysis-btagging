import os
import glob
from ROOT import TFile, TH1F, TH2F, TGraphAsymmErrors, TH1
from Analysis.Tools.utils import Process

TH1.SetDefaultSumw2()

def sample_info(mydir):
   # sample info from directories with name like btag_weight_deepjet_medium_fh_2018_notrg
   info = {}
   info['trg']   = mydir.split('_')[-1]
   info['year']  = mydir.split('_')[-2]
   info['mode']  = mydir.split('_')[-3]
   info['bwp']   = mydir.split('_')[-4]
   info['balgo'] = mydir.split('_')[-5]
   return info


      # this class has to prepare pt, eta, phi and possibly m12 distributions, flavour dependent?
class BTagWeight:
   def __init__(self,process,histo_dir='kinematics',flavours=['b','bb','c','cc','udsg'],variables=['pt','eta','phi']):
      self.m_proc = process
      self.m_histo_dir = histo_dir
      self.m_flvs = flavours
      self.m_vars = variables
      self.m_jets = []
      self.m_dijets = []
      self.m_histos = {}
      self.m_histos_dijet = {}
      self.m_histos_proc = {}
      self.m_histos_dijet_proc = {}
      
   def histogram_directory(self):
      return self.m_histo_dir
      
   def flavours(self):
      return self.m_flvs
      
   def histograms(self,process=False):
      if process:
         return self.m_histos_proc
      return self.m_histos
      
   def histograms_dijet(self,process=False):
      if process:
         return self.m_histos_dijet_proc
      return self.m_histos_dijet
      
   def jets(self):
      return self.m_jets
      
   def dijets(self):
      return self.m_dijets
      
   # read histograms from the files   
   def readTH1(self,lumi_scale=False):
      h1 = {}
      pbins = []
      jets = []
      njets = -1
      h_types = self.m_vars
      flv_all = self.flavours()
      flv_all.append('all')
      for pbin, pfile in self.m_proc.rootFiles().items():  # need to think better these loops to avoid more loops below
         ls = self.m_proc.luminosityScale()[pbin]
         h1[pbin] = {}
         pbins.append(pbin)
         tfile = TFile( pfile, 'OLD' )
         # get number of jets
         h_dir = tfile.GetDirectory(self.m_histo_dir)
         h_dir_keys = h_dir.GetListOfKeys()
         histo_names = {}
         for typ in h_types:
            histo_names[typ] = [x.GetName() for x in h_dir_keys if typ+'_jet' in x.GetName() and x.GetName().count('_')==1 and len(x.GetName())==(len(typ)+5)]
         if not jets:  # number of jets is the same for all process bins
            njets = len(histo_names['pt'])
            for j in range(1,njets+1):
               jet = 'jet{}'.format(j)
               jets.append(jet)
         for flv in flv_all:
            h1[pbin][flv]={}
            for jet in jets:
               h1[pbin][flv][jet]={}
               for typ in h_types:
                  h_name = '{}_{}_{}'.format(typ,jet,flv)
                  if flv == 'all':
                     h_name = '{}_{}'.format(typ,jet)
                  h1[pbin][flv][jet][typ] = h_dir.Get(h_name)
                  h1[pbin][flv][jet][typ].SetName('{}_{}'.format(h_name,pbin))
                  h1[pbin][flv][jet][typ].SetDirectory(0) # Important!
                  if lumi_scale:
                     h1[pbin][flv][jet][typ].Scale(ls)
         tfile.Close()
         
      self.m_histos_proc = h1
      self.m_jets = jets
         
      h1_add_proc = {}
      for f,flv in enumerate(flv_all):
         h1_add_proc[flv] = {}
         for jet in jets:
            h1_add_proc[flv][jet] = {}
            for typ in h_types:
               h_name = typ+'_'+jet+'_'+flv
               for b,pbin in enumerate(pbins):
                  if b == 0:
                     h1_add_proc[flv][jet][typ] = h1[pbin][flv][jet][typ].Clone(h_name)
                  else:
                     h1_add_proc[flv][jet][typ].Add(h1[pbin][flv][jet][typ])
                  h1_add_proc[flv][jet][typ].SetDirectory(0) # Important!
               
               
      self.m_histos = h1_add_proc
      
   # read histograms from the files   
   def readTH1Dijet(self,lumi_scale=False):
      h1 = {}
      pbins = []
      jets = []
      njets = -1
      h_types = self.m_vars
      flv_all = self.flavours()
      flv_all = ['all']
      for pbin, pfile in self.m_proc.rootFiles().items():  # need to think better these loops to avoid more loops below
         ls = self.m_proc.luminosityScale()[pbin]
         h1[pbin] = {}
         pbins.append(pbin)
         tfile = TFile( pfile, 'OLD' )
         # get number of jets
         h_dir = tfile.GetDirectory(self.m_histo_dir)
         h_dir_keys = h_dir.GetListOfKeys()
         histo_names = {}
         for typ in h_types:
            histo_names[typ] = [x.GetName() for x in h_dir_keys if typ+'_jet' in x.GetName() and x.GetName().count('_')==1 and len(x.GetName())==(len(typ)+6)]
         if not jets:  # number of jets is the same for all process bins
            for j2 in histo_names['m']:
               jets.append(j2[2:])
            njets = len(jets)
         for flv in flv_all:
            h1[pbin][flv]={}
            for jet in jets:
               h1[pbin][flv][jet]={}
               for typ in h_types:
                  h_name = '{}_{}_{}'.format(typ,jet,flv)
                  if flv == 'all':
                     h_name = '{}_{}'.format(typ,jet)
                  h1[pbin][flv][jet][typ] = h_dir.Get(h_name)
                  h1[pbin][flv][jet][typ].SetName('{}_{}'.format(h_name,pbin))
                  h1[pbin][flv][jet][typ].SetDirectory(0) # Important!
                  if lumi_scale:
                     h1[pbin][flv][jet][typ].Scale(ls)
         tfile.Close()
         
      self.m_histos_dijet_proc = h1
      self.m_dijets = jets
         
      h1_add_proc = {}
      for f,flv in enumerate(flv_all):
         h1_add_proc[flv] = {}
         for jet in jets:
            h1_add_proc[flv][jet] = {}
            for typ in h_types:
               h_name = typ+'_'+jet+'_'+flv
               for b,pbin in enumerate(pbins):
                  if b == 0:
                     h1_add_proc[flv][jet][typ] = h1[pbin][flv][jet][typ].Clone(h_name)
                  else:
                     h1_add_proc[flv][jet][typ].Add(h1[pbin][flv][jet][typ])
                  h1_add_proc[flv][jet][typ].SetDirectory(0) # Important!
               
               
      self.m_histos_dijet = h1_add_proc
      
############################################################################      

class BTagEfficiency:
   def __init__(self,process,btag_dir='btag_jets',nobtag_dir='all_jets',h1_pt='pt_jet',h2_pt_eta='pt_eta_jet',rebin=None):
      self.m_proc = process
      self.m_btag_dir = btag_dir
      self.m_nobtag_dir = nobtag_dir
      self.m_h1_pt = h1_pt
      self.m_h2_pt_eta = h2_pt_eta
      self.m_flavours = ['b','bb','c','cc','udsg']
      self.m_rebin = rebin
      self.m_h1_pt_eta = {}
      # relevant histograms
      h_dir = {}
      h_dir['btag'] = btag_dir
      h_dir['nobtag'] = nobtag_dir
      self.m_hdir = h_dir
      h1 = self.readTHs()
      h2 = self.readTHs(th2=True)
      self.m_h1 = h1
      self.m_h2 = h2
      # integrate over process bins
      self.m_h1_full = self.addProcessBins()
      self.m_h2_full = self.addProcessBins(th2=True)
      self.m_h1_full_ls = self.addProcessBins(lumiscale=True)
      self.m_h2_full_ls = self.addProcessBins(lumiscale=True,th2=True)
      
      self.m_efficiencies = {}
   
   # efficiencies
   def efficiencies(self,etabins=None,rebin=None,ptmin=None,ptmax=None):
      eff = {}
      if etabins:
         h1 = self.etaProjections(etabins)
         for flv in self.m_flavours:
            eff[flv] = {}
            for i in range(len(etabins)-1):
               etamin = etabins[i]
               etamax = etabins[i+1]
               etarange = '%3.1f-%3.1f' % (etamin,etamax)
               hh_num = h1['btag'][flv][etarange]
               hh_den = h1['nobtag'][flv][etarange]
               if ptmax:
                  ptmax_bin = hh_num.GetXaxis().FindBin(ptmax)
                  hh_nbins = hh_num.GetNbinsX()
                  for j in range(ptmax_bin,hh_nbins+1):
                     hh_num.SetBinContent(j,0.)
                     hh_num.SetBinError(j,0.)
                     hh_den.SetBinContent(j,0.)
                     hh_den.SetBinError(j,0.)
               if ptmin:
                  ptmin_bin = hh_num.GetXaxis().FindBin(ptmin)
                  for j in range(1,ptmin_bin):
                     hh_num.SetBinContent(j,0.)
                     hh_num.SetBinError(j,0.)
                     hh_den.SetBinContent(j,0.)
                     hh_den.SetBinError(j,0.)
               if rebin:
                  hh_num_rb = hh_num.Rebin(len(rebin)-1,"hh_num_rb",rebin)
                  hh_den_rb = hh_den.Rebin(len(rebin)-1,"hh_num_rb",rebin)
               else:
                  hh_num_rb = hh_num
                  hh_den_rb = hh_den
               eff[flv][etarange] = TGraphAsymmErrors(hh_num_rb,hh_den_rb,"cl=0.683 b(1,1) mode");
            
         self.m_efficiencies = eff
         return self.m_efficiencies
      h1 = self.m_h1_full
      for flv in self.m_flavours:
         hh_num = h1['btag'][flv]
         hh_den = h1['nobtag'][flv]
         if ptmax:
            ptmax_bin = hh_num.GetXaxis().FindBin(ptmax)
            hh_nbins = hh_num.GetNbinsX()
            for j in range(ptmax_bin,hh_nbins+1):
               hh_num.SetBinContent(j,0.)
               hh_num.SetBinError(j,0.)
               hh_den.SetBinContent(j,0.)
               hh_den.SetBinError(j,0.)
         if ptmin:
            ptmin_bin = hh_num.GetXaxis().FindBin(ptmin)
            for j in range(1,ptmin_bin):
               hh_num.SetBinContent(j,0.)
               hh_num.SetBinError(j,0.)
               hh_den.SetBinContent(j,0.)
               hh_den.SetBinError(j,0.)
         if rebin:
            hh_num_rb = hh_num.Rebin(len(rebin)-1,"hh_num_rb",rebin)
            hh_den_rb = hh_den.Rebin(len(rebin)-1,"hh_num_rb",rebin)
         else:
            hh_num_rb = hh_num
            hh_den_rb = hh_den
         eff[flv] = TGraphAsymmErrors(hh_num_rb,hh_den_rb,"cl=0.683 b(1,1) mode");
      self.m_efficiencies = eff
      return self.m_efficiencies
      
   
   # add process bins
   def addProcessBins(self,lumiscale=False,th2=False):
      # integrate over bins
      h1 = self.m_h1
      if th2:
         h1 = self.m_h2
      h1_full = {}
      for hd in self.m_hdir.keys():
         h1_full[hd] = {}
         for flv in self.m_flavours:
            for i,b in enumerate(self.m_proc.bins()):
               ls = self.m_proc.luminosityScale()[b]
               if i==0:
                  h1_full[hd][flv] = h1[b][hd][flv].Clone()
                  if lumiscale:
                     h1_full[hd][flv].Scale(ls)
               else:
                  h1_full[hd][flv].Add(h1[b][hd][flv])
                  if lumiscale:
                     h1_full[hd][flv].Add(h1[b][hd][flv],lumiscale)
      return h1_full
   
   
   # read histograms from the files   
   def readTHs(self,th2=False):
      h1 = {}
      hname = self.m_h1_pt
      if th2:
         hname = self.m_h2_pt_eta
      for pbin, pfile in self.m_proc.rootFiles().items():  # need to think better these loops to avoid more loops below
         h1[pbin] = {}
         hfile = TFile( pfile, 'OLD' )
         for hd in self.m_hdir.keys():
            h1[pbin][hd] = {}
            for flv in self.m_flavours:
               h1[pbin][hd][flv] = hfile.Get(self.m_hdir[hd]+'/'+hname+'_'+flv)
               h1[pbin][hd][flv].SetDirectory(0)
               if not th2:
                  if self.m_rebin and not isinstance(self.m_rebin, list):
                     h1[pbin][hd][flv].Rebin(self.m_rebin)
         hfile.Close()
      return h1
      
   def histograms1D(self):
      return self.m_h1 
         
   def histograms1DFull(self,lumiscaled=False):
      if lumiscaled:
          return self.m_h1_full_ls
      return self.m_h1_full 
         
   def histograms2D(self):
      return self.m_h2 
         
   def histograms2DFull(self,lumiscaled=False):
      if lumiscaled:
          return self.m_h2_full_ls
      return self.m_h2_full 
      
   def etaProjections(self,etabins,lumiscaled=False):
      h1s_eta = {}
      h2s = self.histograms2DFull(lumiscaled)
      for hd,h_flv in h2s.items():
         h1s_eta[hd] = {}
         for flv,h2 in h_flv.items():
            h1s_eta[hd][flv] = {}
            for i in range(len(etabins)-1):
               etamin = etabins[i]
               etamax = etabins[i+1]
               etarange = '%3.1f-%3.1f' % (etamin,etamax)
               h1s_eta[hd][flv][etarange] = self.etaProjection(etamin,etamax,flv,hd,lumiscaled)
      return h1s_eta
         
   # projection  of 2D pt_eta histogram 
   def etaProjection(self,etamin,etamax,flavour,hdir,lumiscaled=False):
      h2 = self.histograms2DFull(lumiscaled)[hdir][flavour]
      if etamin < 0 or etamax < 0:
         print('Warning! Eta min or eta max must be positive. The projection is for |eta|.')
         return None
      if etamin > etamax:
         a = etamax
         etamax = etamin
         etamin = a
      etarange = '%3.1f-%3.1f' % (etamin,etamax)
      b1p = h2.GetYaxis().FindBin(etamin)
      b2p = h2.GetYaxis().FindBin(etamax)
      h1 = h2.ProjectionX("_px",b1p,b2p,"e")
      h1.SetName('pt_jet_%s_%s_eta_%s'%(flavour,hdir,etarange))
      b1n = h2.GetYaxis().FindBin(-etamax)
      b2n = h2.GetYaxis().FindBin(-etamin)
      if b2n == b1p:
         b2n -= 1;
      h1n = h2.ProjectionX("_px",b1n,b2n,"e")
      h1.Add(h1n)
      if self.m_rebin and not isinstance(self.m_rebin, list):
         h1.Rebin(self.m_rebin)
      return h1
      
   def flavours(self):
      return self.m_flavours

# class Process:
#    def __init__(self,alias,directory):
#       self.m_alias = alias
#       self.m_dir = directory
#       xs = {}
#       if self.m_alias=='QCD_HT':
#          xs['100to200']   = 23700000.0
#          xs['200to300']   = 1547000.0
#          xs['300to500']   = 322600.0
#          xs['500to700']   = 29980.0
#          xs['700to1000']  = 6334.0
#          xs['1000to1500'] = 1088.0
#          xs['1500to2000'] = 99.11
#          xs['2000toInf']  = 20.23
#       if self.m_alias=='bEnriched':
#          xs['100to200']   = 1117000.0
#          xs['200to300']   = 80430.0
#          xs['300to500']   = 16620.0
#          xs['500to700']   = 1487.0
#          xs['700to1000']  = 296.5
#          xs['1000to1500'] = 46.61
#          xs['1500to2000'] = 3.72
#          xs['2000toInf']  = 0.6462
#       if self.m_alias=='BGenFilter':
#          xs['100to200']   = 1282000.0
#          xs['200to300']   = 111800.0
#          xs['300to500']   = 28070.0
#          xs['500to700']   = 3082.0
#          xs['700to1000']  = 724.2
#          xs['1000to1500'] = 138.2
#          xs['1500to2000'] = 13.61
#          xs['2000toInf']  = 2.909
#       if self.m_alias=='QCD_Mu':
#          xs['50To80']    = 376600.0
#          xs['80To120']   = 88930.0
#          xs['120To170']  = 21230.0
#          xs['170To300']  = 7055.0
#          xs['300To470']  = 619.3
#          xs['470To600']  = 59.24
#          xs['600To800']  = 18.21
#          xs['800to1000'] = 3.275
#          xs['1000toInf'] = 1.078
#       self.m_xsections = xs
#       self.m_bins = xs.keys()
#       #root files
#       rf = {}
#       ngen = {}
#       lumi_scale = {}
#       if len(xs) > 0:
#          keyword = self.m_alias
#          if self.m_alias == 'QCD_Mu':
#             keyword = 'MuEnrichedPt5'
#          ld = glob.glob(directory+'/*'+keyword+'*.root')
#          for b in self.m_bins:
#             f = [s for s in ld if b in s]
#             if len(f) == 0:
#                print(alias+': No file for bin '+b+'. Skipping!')
#                continue
#             if len(f) > 1:
#                print('There is more than 1 file with bin '+b+'. The first one, '+f[0]+' will be considered')
#             rf[b] = f[0]
#             # get number of generator+pileup weighted generated events
#             hfile = TFile( f[0], 'OLD' )
#             h_wf = hfile.Get('workflow')
#             ngen[b] = h_wf.GetBinContent(3)
#             lumi_scale[b] = xs[b]/ngen[b]
#             hfile.Close()
#       self.m_rootfiles = rf
#       self.m_ngen = ngen
#       self.m_lumi_scale = lumi_scale
#       # scale to same lumi
#       
#       
#       
#    def alias(self):
#       return self.m_alias
#       
#    def crossSections(self):
#       return self.m_xsections
#       
#    def bins(self):
#       return self.m_bins
#       
#    def neventsGenerated(self):
#       return self.m_ngen
#          
#    def rootFiles(self):
#       return self.m_rootfiles
#       
#    def luminosityScale(self,lumi=1000.):
#       ls = {}
#       for b in self.m_bins:
#          ls[b] = self.m_lumi_scale[b]*lumi
#       return ls
# 
