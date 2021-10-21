#include "Analysis/BTagging/interface/BTaggingAnalyser.h"

// this example has no selection
// for MC it will apply the generator weights

using namespace std;
using namespace analysis;
using namespace analysis::tools;
using namespace analysis::btagging;

int main(int argc, char ** argv)
{
   BTaggingAnalyser analyser(argc,argv);
   auto config = analyser.config();
   
// HISTOGRAMS definitions  
   // create some predefined jet histograms
   // if not defined, the number of jets is nJetMin from the configurations
   analyser.histograms("all_jets");
   analyser.histograms("btag_jets");
   
   for ( int i = 0 ; i < analyser.nEvents() ; ++i )
   {
      if ( ! analyser.event(i)                  )   continue;
      
   // trigger
      if ( ! analyser.selectionHLT()            )   continue;
      if ( ! analyser.selectionL1 ()            )   continue;  // to be used mainly in case of "OR" of seeds
      
   // muons
      if ( ! analyser.selectionMuonId()         )   continue;
      if ( ! analyser.selectionNMuons()         )   continue;
      if ( ! analyser.selectionMuons()          )   continue;
      if ( ! analyser.onlineMuonMatching()      )   continue;
      
   // jets
      analyser.actionApplyJER();                               
      analyser.actionApplyBjetRegression();                    
      if ( ! analyser.selectionJetId()          )   continue;  
      if ( ! analyser.selectionJetPileupId()    )   continue;  
      if ( ! analyser.selectionNJets()          )   continue;  
      if ( ! analyser.selectionLeadJets()       )   continue;
      if ( ! analyser.selectionLeadJetsDphi()   )   continue;
      if ( ! analyser.selectionLeadJetsDr()     )   continue;
      // trigger matching
      if ( ! analyser.onlineLeadJetsMatching()  )   continue;
      if ( ! analyser.onlineLeadBJetsMatching() )   continue;
      if ( ! analyser.selectionLeadJetsMuon()   )   continue;
      
      // all jets histograms
      for ( int j1 = 1; j1 <= config->nJetsMin(); ++j1 )
         analyser.fillHistograms(j1,"all_jets");
      // btag jets histograms
      for ( int j1 = 1; j1 <= config->nBJetsMin(); ++j1 )
         if ( analyser.selectionBJet(j1) ) analyser.fillHistograms(j1,"btag_jets",analyser.getBtagSF(j1));
   }  //end event loop
   

} // end main
      
