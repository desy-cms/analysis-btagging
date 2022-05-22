#include "Analysis/Tools/interface/Analyser.h"
#include "Analysis/MssmHbb/interface/MssmHbbAnalyser.h"

// this example has no selection
// for MC it will apply the generator weights

using namespace std;
using namespace analysis;
using namespace analysis::mssmhbb;

int main(int argc, char ** argv)
{
   MssmHbbAnalyser analyser(argc,argv);
   auto config = analyser.config();
   
// HISTOGRAMS definitions  
   analyser.jetHistograms("kinematics");
   analyser.jetHistograms("trigger");
   for ( int r = 1; r <= config->nBJetsMin(); ++r )
      analyser.jetHistograms(Form("btag%d",r));
   
   bool pass = true;
   
   for ( int i = 0 ; i < analyser.nEvents() ; ++i )
   {
   
      if ( ! analyser.event(i)                  )   continue;
   // JETS
      if ( ! analyser.selectionJetId()          )   continue;  // selection  : jet identification 
      if ( ! analyser.selectionJetPileupId()    )   continue;  // selection  : jet Pileup identification 
      if ( ! analyser.selectionNJets()          )   continue;  // selection  : number of jets 
      analyser.actionApplyJER();                               // correction : jet energy resolution smearing
      analyser.actionApplyBjetRegression();                    
      
      // jets pt and eta selection
      pass = true;
      for ( int r = 1; r <= config->nJetsMin(); ++r )
      {
         pass = ( pass && analyser.selectionJet(r) );
      } // end jets loop
      
      if ( ! pass ) continue;
      
      if ( ! analyser.selectionJetDr(1,2)      )   continue;
      if ( ! analyser.selectionJetDr(1,3)      )   continue;
      if ( ! analyser.selectionJetDr(2,3)      )   continue;
      if ( ! analyser.selectionJetDeta(1,2)    )   continue;

   // muons
      if ( ! analyser.selectionMuonId()         )   continue;
      if ( ! analyser.selectionNMuons()         )   continue;
      if ( ! analyser.selectionMuons()          )   continue;
      if ( ! analyser.muonJet()                 )   continue;    // muon-jet association
      
      analyser.fillJetHistograms("kinematics");
      
   // trigger
      if ( ! analyser.selectionHLT()            )   continue;
      if ( ! analyser.selectionL1 ()            )   continue;  // to be used mainly in case of "OR" of seeds
      
      // jets 1 and 2 matching to online jets and btag
      if ( config->nJetsMin() >= 1  &&  ! analyser.onlineJetMatching(1)     )   continue;
      if ( config->nJetsMin() >= 2  &&  ! analyser.onlineJetMatching(2)     )   continue;
      if ( config->nBJetsMin() >= 1  && ! analyser.onlineBJetMatching(1)    )   continue;
      if ( config->nBJetsMin() >= 2  && ! analyser.onlineBJetMatching(2)    )   continue;
      
      // muon trigger matching
      if ( ! analyser.onlineMuonMatching()     )   continue;
      
      // re-doing association with muons matched to online
      // at least one of the leading jets will have a muon (ofline+online)
      if ( ! analyser.muonJet()                 )   continue;    // muon-jet association
      
      analyser.fillJetHistograms("trigger");
      
      // jets btag selection
      auto jet1 = analyser.selectedJets()[0];
      auto jet2 = analyser.selectedJets()[1];
      // assume jet1 has muon
      int jet1_eff = 3;
      int jet2_eff = 1;
      if ( config->btagEfficiencies(1) != "" )
      {
         // if both jets have a muon, the SL jet is the one with highest leading muon 
         if ( jet1->muon() && jet2->muon() )
         {
            if ( jet1->muon()->pt() < jet2->muon()->pt() )
            {
               jet1_eff = 1;
               jet2_eff = 3;
            }
         }
         else // only one of the jets has muon and that is jet2
         {
            if ( jet2->muon() )
            {
               jet1_eff = 1;
               jet2_eff = 3;
            }
         }
         analyser.actionApplyBtagEfficiency(1,jet1_eff); // btag1
         analyser.fillJetHistograms(Form("btag%d",1));
         
         analyser.actionApplyBtagEfficiency(2,jet2_eff); // btag2
         analyser.fillJetHistograms(Form("btag%d",2));

         analyser.actionApplyBtagEfficiency(3,2);        // btag3
         analyser.fillJetHistograms(Form("btag%d",3));
      }
      else
      {
         if ( !  analyser.selectionBJet(1) ) continue;  // btag1
         analyser.actionApplyBtagSF(1);
         analyser.fillJetHistograms(Form("btag%d",1));
         if ( !  analyser.selectionBJet(2) ) continue;  // btag2
         analyser.actionApplyBtagSF(2);
         analyser.fillJetHistograms(Form("btag%d",2));
         if ( !  analyser.selectionBJet(3) ) continue;  // btag3
         analyser.actionApplyBtagSF(3);
         analyser.fillJetHistograms(Form("btag%d",3));
      }
      
      
      if ( ! pass ) continue;
      
   }  //end event loop
   

} // end main
      
