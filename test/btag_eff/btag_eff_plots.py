#!/usr/bin/env python

## Offline b-tag efficiency
### Also comparison between two efficiencies

import sys,os
from Analysis.Tools.utils import Process
from Analysis.BTagging.utils import BTagEfficiency
from ROOT import TCanvas, TMultiGraph,TLine
from ROOT import kRed, kBlue, kBlack, kMagenta, kGreen, kCyan
from rootpy.interactive import wait

flavours = ['b','bb','c','cc','udsg']


myproc1 = str(sys.argv[1])
directory1 = str(sys.argv[2])
year1 = directory1.split('_')[-2]
trg1 = directory1.split('_')[-1]
mu1 = directory1.split('_')[-3]
h_trg1 = '(w/ trigger)' if trg1 == 'trg' else '(w/o trigger)'
h_mu1 = 'SL' if mu1 == 'mu' else 'FH'
balgo1 = 'deepjet' if 'deepjet' in directory1 else 'deepcsv'
bwp1 = 'medium' if 'medium' in directory1 else 'tight'
h_balgo1 = "DeepJet" if balgo1 == 'deepjet' else 'DeepCSV'
h_bwp1 = 'Medium WP' if bwp1 == 'medium' else 'Tight WP'

qcd1 = Process(myproc1,directory1)
btageff1 = BTagEfficiency(process=qcd1,btag_dir='btag_jets',nobtag_dir='all_jets',h1_pt='pt_jet',h2_pt_eta='pt_eta_jet',rebin=20)
eff1 = {}


if len(sys.argv) > 3:
   myproc2 = str(sys.argv[3])
   directory2 = str(sys.argv[4])
   year2 = directory2.split('_')[-2]
   trg2 = directory2.split('_')[-1]
   mu2 = directory2.split('_')[-3]
   h_trg2 = '(w/ trigger)' if trg2 == 'trg' else '(w/o trigger)'
   h_mu2 = 'SL' if mu2 == 'mu' else 'FH'
   balgo2 = 'deepjet' if 'deepjet' in directory2 else 'deepcsv'
   bwp2 = 'medium' if 'medium' in directory2 else 'tight'
   h_balgo2 = "DeepJet" if balgo2 == 'deepjet' else 'DeepCSV'
   h_bwp2 = 'Medium WP' if bwp2 == 'medium' else 'Tight WP'

   qcd2 = Process(myproc2,directory2)
   btageff2 = BTagEfficiency(process=qcd2,btag_dir='btag_jets',nobtag_dir='all_jets',h1_pt='pt_jet',h2_pt_eta='pt_eta_jet',rebin=20)
   eff2 = {}
   
   
canvas = {}
mg = {}
leg = {}

for flv in flavours:
   canvas[flv] =  TCanvas( 'c_'+flv, 'btag efficiency', 200, 10, 820, 640 )
   canvas[flv].SetLeftMargin(0.125)
   canvas[flv].SetRightMargin(0.075)
   canvas[flv].SetTopMargin(0.105)
   canvas[flv].SetBottomMargin(0.135)
   
   eff1[flv] = btageff1.efficiencies()[flv]
   eff1[flv].SetTitle(year1+' '+h_mu1+' '+h_balgo1+' '+h_bwp1+' ('+trg1+') ')
   eff1[flv].SetMarkerStyle(20)
   eff1[flv].SetMarkerSize(0.8)
   eff1[flv].SetMarkerColor(kBlue)
   eff1[flv].SetLineColor(kBlue)  
   
   mg[flv] = TMultiGraph()
   mg[flv].Add(eff1[flv],'p')
   if len(sys.argv) > 3:
      eff2[flv] = btageff2.efficiencies()[flv]
      eff2[flv].SetTitle(year2+' '+h_mu2+' '+h_balgo2+' '+h_bwp2+' ('+trg2+') ')
      eff2[flv].SetMarkerStyle(20)
      eff2[flv].SetMarkerSize(0.8)
      eff2[flv].SetMarkerColor(kRed)
      eff2[flv].SetLineColor(kRed)
      mg[flv].Add(eff2[flv],'p')
      
   mg[flv].Draw('a')
#    x1=0.12
#    x2=0.67
#    y1=0.12
#    y2=0.28
#    if not 'b' in flv:
#       y1 =0.76+0.08
#       y2 =0.88+0.08
#    if 'cc' in flv:
#       x1 = 0.33
#       x2 = 0.88
   x1=0.125
   x2=0.925
   y1=0.785
   y2=0.905
   
   leg[flv] = canvas[flv].BuildLegend(x1,y1,x2,y2)
   
   print(leg[flv].GetX1NDC(),leg[flv].GetX2NDC(),leg[flv].GetY1NDC(),leg[flv].GetY2NDC())
   leg[flv].SetHeader(flv+' jets')
   leg[flv].SetTextSize(0.040)
   mg[flv].GetHistogram().GetXaxis().SetRangeUser(0.,1200.)
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
#   line = TLine(0.,1.,1200.,1.);
#   line.Draw("same");
   
   canvas[flv].Modified()
   canvas[flv].Update()
   resdir = './results'
   if not os.path.exists(resdir):
      os.makedirs(resdir)
   outfile = resdir+'/btag_eff_'+flv+'jets_'+year1+'_'+balgo1+'_'+bwp1+'_'+h_mu1+'_'+trg1
   if len(sys.argv) > 3:
      outfile += '_x_'+balgo2+'_'+bwp2+'_'+year2+'_'+balgo2+'_'+bwp2+'_'+h_mu2+'_'+trg2
   outfile +='.png'
   
   canvas[flv].SaveAs(outfile)
   
   if flv == 'udsg':
      mg[flv].GetHistogram().GetYaxis().SetRangeUser(0.005,1.19)
      if bwp1 == 'tight' or bwp2 == 'tight':
         mg[flv].GetHistogram().GetYaxis().SetRangeUser(0.0005,1.19)
      canvas[flv].SetLogy()
      outfile = resdir+'/btag_eff_'+flv+'jets_'+year1+'_'+balgo1+'_'+bwp1+'_'+h_mu1+'_'+trg1
      if len(sys.argv) > 3:
         outfile += '_x_'+balgo2+'_'+bwp2+'_'+year2+'_'+balgo2+'_'+bwp2+'_'+h_mu2+'_'+trg2
      outfile +='_log.png'

      canvas[flv].SaveAs(outfile)
   
wait(True) # close with middle mouse button
