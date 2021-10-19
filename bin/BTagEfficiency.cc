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
      
   // Muons
      if ( ! analyser.selectionMuonId()         )   continue;
      if ( ! analyser.selectionNMuons()         )   continue;
      if ( ! analyser.selectionMuons()          )   continue;
      
   // JETS
      analyser.actionApplyJER();                               // correction : jet energy resolution smearing
      analyser.actionApplyBjetRegression();                    // correction : jet energy regression (for b jets)
      if ( ! analyser.selectionJetId()          )   continue;  // selection  : jet identification 
      if ( ! analyser.selectionJetPileupId()    )   continue;  // selection  : jet Pileup identification 
      if ( ! analyser.selectionNJets()          )   continue;  // selection  : number of jets 
      if ( ! analyser.selectionLeadJets()       )   continue;
      if ( ! analyser.selectionLeadJetsDphi()   )   continue;
      if ( ! analyser.selectionLeadJetsDr()     )   continue;
      if ( ! analyser.selectionLeadJetsMuon()   )   continue;
      // all jets histograms
      for ( int j1 = 1; j1 <= config->nJetsMin(); ++j1 )
         analyser.fillHistograms(j1,"all_jets");
      // btag jets histograms
      for ( int j1 = 1; j1 <= config->nBJetsMin(); ++j1 )
         if ( analyser.selectionBJet(j1) ) analyser.fillHistograms(j1,"btag_jets",analyser.getBtagSF(j1));
   }  //end event loop
   

} // end main
      
