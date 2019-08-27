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
   analyser.jetHistograms("kinematics");
   analyser.jetHistograms("jet1btag");
   analyser.jetHistograms("jet2btag");
   
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
      analyser.fillJetHistograms("kinematics");                // histograms : jets fill
   // BTAG - test of btag only, no selection
      for ( int ib = 0; ib < config->nBJetsMin(); ++ib )
      {
         int r = ib+1;
         if (   analyser.selectionBJet(r)          )
         {
            float sf = analyser.getBtagSF(r);  // only retrieve scale factor to be applied to histograms below
            analyser.fillJetHistograms(r,Form("jet%dbtag",r),sf);                  // histograms : jet 1 fill weighting by the SF
         }
      }
   }  //end event loop
   

} // end main
      
