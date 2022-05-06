#include "Analysis/Tools/interface/Analyser.h"

// this example has no selection
// for MC it will apply the generator weights

using namespace std;
using namespace analysis;
using namespace analysis::tools;

int main(int argc, char ** argv)
{
   Analyser analyser(argc,argv);
   auto config = analyser.config();
   
// HISTOGRAMS definitions  
   analyser.jetHistograms("kinematics");
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
      
      // jets pt and eta selection
      pass = true;
      for ( int r = 1; r <= config->nJetsMin(); ++r )
      {
         pass = ( pass && analyser.selectionJet(r) );
      } // end jets loop
      
      if ( ! pass ) continue;
      analyser.fillJetHistograms("kinematics");
      
      // jets btag selection
      for ( int r = 1; r <= config->nBJetsMin(); ++r ) // loop over bjets
      {
         if ( config->btagEfficiencies() != "" )
         {
            analyser.actionApplyBtagEfficiency(r);
         }
         else
         {
            pass = ( pass && analyser.selectionBJet(r) );
            if ( ! pass ) break;
            analyser.actionApplyBtagSF(r);
         }
         analyser.fillJetHistograms(Form("btag%d",r));
      }
      if ( ! pass ) continue;
      
   }  //end event loop
   

} // end main
      
