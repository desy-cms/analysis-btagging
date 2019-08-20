/**\class BTagging BTaggingAnalyser.cc Analysis/BTagging/src/BTaggingAnalyser.cc

 Description: [one line class summary]

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  Roberval Walsh
//         Created:  Mon, 05 Mar 2019 18:30:00 GMT
//
//

// system include files
#include <iostream>
// user include files
#include "Analysis/BTagging/interface/BTaggingAnalyser.h"

//
// class declaration
//

using namespace analysis;
using namespace analysis::tools;
using namespace analysis::btagging;


//
// constructors and destructor
//
BTaggingAnalyser::BTaggingAnalyser()
{
}

BTaggingAnalyser::BTaggingAnalyser(int argc, char ** argv) : BaseAnalyser(argc,argv), Analyser(argc,argv)
{
}

BTaggingAnalyser::~BTaggingAnalyser()
{
   // do anything here that needs to be done at desctruction time
   // (e.g. close files, deallocate resources etc.)
}


//
// member functions
//
// ------------ method called for each event  ------------


