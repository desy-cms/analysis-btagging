#!/usr/bin/env python
import sys,os
from Analysis.Tools.utils import Process
from Analysis.BTagging.utils import BTagEfficiency
from ROOT import TCanvas, TMultiGraph, TSpline3, TSpline5, TSpline, TGraphSmooth, TFile, TH1
from ROOT import kRed, kBlue, kBlack, kMagenta, kGreen, kCyan, kOrange
import array
from rootpy.interactive import wait

TH1.SetDefaultSumw2()

myproc = str(sys.argv[1])
directory = str(sys.argv[2])
year = directory.split('_')[-2]
trg = directory.split('_')[-1]
mu = directory.split('_')[-3]
h_trg = '(trg)' if trg == 'trg' else '(notrg)'
#h_mu = 'SL' if mu == 'mu' else 'FH'
h_mu = mu.upper()
balgo = 'deepjet' if 'deepjet' in directory else 'deepcsv'
bwp = 'medium' if 'medium' in directory else 'tight'
h_balgo = "DeepJet" if balgo == 'deepjet' else 'DeepCSV'
h_bwp = 'Medium WP' if bwp == 'medium' else 'Tight WP'

qcd = Process(myproc,directory)

btageff = BTagEfficiency(process=qcd)
flavours = btageff.flavours()
#etabins = [0.0,0.9,1.1,1.35,1.5,1.6,2.0,2.2]
etabins = [0.0,1.3,1.6,2.0,2.2]
etaranges = []
ptmin = 30.
ptmax = 1500.
for i in range(len(etabins)-1):
   etamin = etabins[i]
   etamax = etabins[i+1]
   etaranges.append('%3.1f-%3.1f' % (etamin,etamax))
colors = [kBlue,kBlack,kRed,kGreen+1,kMagenta,kCyan,kOrange]
xbins = []
s0 = 10
s1 = 20
s2 = 25
s3 = 50
s4 = 100
s5 = 300
if trg == 'notrg':
   for i in xrange(30,40,5):
      xbins.append(i)
   
for i in xrange(40,100,20):
   xbins.append(i)
   
for i in xrange(100,150,25):
   xbins.append(i)
   
for i in xrange(150,400,50):
   xbins.append(i)
   
for i in xrange(400,600,100):
   xbins.append(i)
   
for i in xrange(600,1000,200):
   xbins.append(i)
   
for i in xrange(1000,1501,500):
   xbins.append(i)

if mu == 'sl':
   ptmin = 30.
   ptmax = 1200.
   xbins = []
   if trg == 'trg':   
      for i in xrange(int(ptmin),70,40):
         xbins.append(i)
      for i in xrange(70,150,80):
         xbins.append(i)
      for i in xrange(150,550,100):
         xbins.append(i)
      for i in xrange(550,1000,150):
         xbins.append(i)
      for i in xrange(1000,int(ptmax)+1,200):
         xbins.append(i)
   else:
      ptmin = 40.
      for i in xrange(int(ptmin),100,20):
         xbins.append(i)
      for i in xrange(100,400,25):
         xbins.append(i)
      for i in xrange(400,600,50):
         xbins.append(i)
      for i in xrange(600,1000,100):
         xbins.append(i)
      for i in xrange(1000,int(ptmax)+1,200):
         xbins.append(i)
   

axbins = array.array('d', xbins)
eff_eta = btageff.efficiencies(etabins,rebin=axbins,ptmin=ptmin,ptmax=ptmax)


mg = {}
c1 = {}
lg = {}
#spline = {}
#smooth = {}

for flv in flavours:
   c1[flv] =  TCanvas( 'c_'+flv, 'btag efficiency', 2000, 10, 820, 640 )
   c1[flv].SetLeftMargin(0.125)
   c1[flv].SetRightMargin(0.075)
   c1[flv].SetTopMargin(0.105)
   c1[flv].SetBottomMargin(0.135)
   
   
   mg[flv] = TMultiGraph()
   for i,er in enumerate(etaranges):
      eff_eta[flv][er].SetMarkerStyle(20)
      eff_eta[flv][er].SetMarkerColor(colors[i])
      eff_eta[flv][er].SetLineColor(colors[i])
      eff_eta[flv][er].SetTitle('|#eta| = [%s]'%er)
      mg[flv].Add(eff_eta[flv][er],'p')
      mg[flv].GetHistogram().GetXaxis().SetRangeUser(0.,ptmax)
      mg[flv].GetHistogram().GetYaxis().SetRangeUser(0.,1.)
      mg[flv].GetHistogram().GetXaxis().SetTitle('jet p_{T} [GeV]')
      mg[flv].GetHistogram().GetYaxis().SetTitle('efficiency')
   
#   spline[flv] = {}
#   smooth[flv] = {}
#   for i,er in enumerate(etaranges):
#      spline[flv][er] = TSpline('g_'+flv+'_'+er,eff_eta[flv][er])
#      spline[flv][er].Draw('same')
#      smooth[flv][er] = TGraphSmooth('gs_'+flv+'_'+er)
#      gs = smooth[flv][er].Approx(eff_eta[flv][er],"linear",100)
#      gs.SetLineColor(colors[i])
#      mg[flv].Add(gs)
      
   mg[flv].Draw('A')
#    x1=0.12
#    x2=0.47
#    y1=0.12
#    y2=0.43
# #   if not 'b' in flv:
#    if trg == 'notrg':
#       if 'udsg' in flv or flv == 'cc':
#          y1 = 0.61
#          y2 = 0.88
#    if 'c' in flv and not 'cc' in flv:
#       x1 = 0.53
#       x2 = 0.88
#       y1 = 0.61
#       y2 = 0.88
   x1=0.125
   x2=0.925
   y1=0.785
   y2=0.905

   lg[flv] = c1[flv].BuildLegend(x1,y1,x2,y2)
   lg[flv].SetNColumns(2);
   lg[flv].SetTextSize(0.037);
   header = flv+' jets: '+year+' '+h_mu+' '+h_balgo+' '+h_bwp+' '+h_trg
   lg[flv].SetHeader(header)
   
   mg[flv].GetHistogram().GetXaxis().SetRangeUser(0.,ptmax)
   mg[flv].GetHistogram().GetYaxis().SetRangeUser(0.,1.19)
   mg[flv].GetHistogram().GetXaxis().SetTitle('jet p_{T} [GeV]')
   mg[flv].GetHistogram().GetYaxis().SetTitle('efficiency')
   mg[flv].GetHistogram().GetXaxis().SetLabelFont(42)
   mg[flv].GetHistogram().GetXaxis().SetLabelSize(0.045)
   mg[flv].GetHistogram().GetXaxis().SetTitleSize(0.045)
   mg[flv].GetHistogram().GetXaxis().SetTitleOffset(1.4)
   mg[flv].GetHistogram().GetYaxis().SetLabelFont(42)
   mg[flv].GetHistogram().GetYaxis().SetLabelSize(0.045)
   mg[flv].GetHistogram().GetYaxis().SetTitleSize(0.045)
   mg[flv].GetHistogram().GetYaxis().SetTitleOffset(1.)
   
   c1[flv].Modified()
   c1[flv].Update()
   
   posdir = directory.rfind('/') - len(directory)
   resdir = directory[:posdir]+'/results/eta_dependence'
   if not os.path.exists(resdir):
      os.makedirs(resdir)
#    

   if 'udsg' in flv:
      mg[flv].GetHistogram().GetYaxis().SetRangeUser(0.005,1.9)
      c1[flv].SetLogy()
      
   naming = balgo+'_'+bwp+'_'+mu+'_'+year+'_'+trg
   
   outfile = resdir+'/btag_eff_eta_'+flv+'_jets_'+naming
   outfile +='.png'
   
   c1[flv].SaveAs(outfile)

outroot = resdir+'/btag_eff_'+naming+'.root'
f_g = TFile(outroot,"RECREATE");

for flv in flavours:
   for i,er in enumerate(etaranges):
      eff_eta[flv][er].Write('btag_eff_'+flv+'_pt_eta_'+er)
   
f_g.Close()

print('The End')
wait(True) # close with middle mouse button
