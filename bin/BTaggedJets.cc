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
   analyser.jetHistograms("selection01");
   analyser.jetHistograms("selection02");
//   analyser.jetHistograms("selection03");
   
   for ( int i = 0 ; i < analyser.nEvents() ; ++i )
   {
      if ( ! analyser.event(i)                  )   continue;
      
      analyser.actionApplyPileupWeight();                      // correction : pileup reweight
   // JETS
      analyser.actionApplyJER();                               // correction : jet energy resolution smearing
      analyser.actionApplyBjetRegression();                    // correction : jet energy regression (for b jets)
      if ( ! analyser.selectionJetId()          )   continue;  // selection  : jet identification 
      if ( ! analyser.selectionJetPileupId()    )   continue;  // selection  : jet Pileup identification 
      if ( ! analyser.selectionNJets()          )   continue;  // selection  : number of jets 
      if ( ! analyser.selectionJet(1)           )   continue;  // selection  : jet1 pt and eta 
      if ( ! analyser.selectionJet(2)           )   continue;  // selection  : jet2 pt and eta 
      if ( ! analyser.selectionJetDphi(1,2)     )   continue;  // selection  : delta_phi_jets (1,2) [or  MIN(neg): analyser.selectionJetDphi(1,2,-2.0) / MAX(pos): analyser.selectionJetDphi(1,2,+2.0)]
      analyser.fillJetHistograms("selection01");               // histograms : jets fill
   // BTAG
      if ( ! analyser.selectionBJet(1)          )   continue;
      analyser.actionApplyBtagSF(1);
      analyser.fillJetHistograms("selection02");               // histograms : jets fill
//      if ( ! analyser.selectionBJet(2)          )   continue;
//      analyser.actionApplyBtagSF(2);
//      analyser.fillJetHistograms("selection03");               // histograms : jets fill
      
   }  //end event loop
   

} // end main
      
