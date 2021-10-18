#ifndef Analysis_BTagging_BTaggingAnalyser_h
#define Analysis_BTagging_BTaggingAnalyser_h 1

// -*- C++ -*-
//
// Package:    Analysis/BTagging
// Class:      Analysis
// 
/**\class Analysis BTaggingAnalyser.cc Analysis/BTagging/src/BTaggingAnalyser.cc

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
#include <memory>
#include <vector>
#include <string>
// 

#include "Analysis/Tools/interface/Analyser.h"

//
// class declaration
//

namespace analysis {
   namespace btagging {

      class BTaggingAnalyser : public analysis::tools::Analyser {
         
         public:
            BTaggingAnalyser();
            BTaggingAnalyser(int argc, char ** argv);
           ~BTaggingAnalyser();
           
            // ----------member data ---------------------------
         protected:
            std::vector<float> bins_btag_;
            int nbins_btag_;
                           
         private:
            void btag_binning();
            void create_histograms(const std::string & label, const std::string & extra = "");
            void fill_histograms(const int & rank,const std::string & label, const float & sf, const std::string & extra = "");
               
         public:
            virtual void histograms(const std::string & label);
            virtual void fillHistograms(const int & rank, const std::string & label, const float & sf=1);

      };
   }
}

#endif  // Analysis_BTagging_BTaggingAnalyser_h
