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


void BTaggingAnalyser::histograms( const std::string & label)
{
   if ( label == "" )
   {
      std::cout << "-warning- BTaggingAnalyser::histograms - no label given for histograms (root directory)" << std::endl;
      return;
   }
   
   this->output()->cd();
   if ( this->output()->FindObjectAny(label.c_str()) )  return;
   
   this->output()->mkdir(label.c_str());
   this->output()->cd(label.c_str());
   
   create_histograms(label);
   if ( config_->isMC() && config_->histogramJetsPerFlavour() )
   {
      for ( auto & flv : flavours_ ) // flavour dependent histograms
      {
         create_histograms(label,flv);
      }
   }
   
}
void BTaggingAnalyser::create_histograms( const std::string & label,  const std::string & extra )
{
   std::string xx = "";
   if ( extra != "" ) xx = "_"+extra;;
   const char * x = xx.c_str();
   const char * l = label.c_str();
   
   btag_binning();
   
   // 1D histograms
   h1_[Form("pt_jet_%s%s"  , l,x)]  = std::make_shared<TH1F>( Form("pt_jet%s" ,x) , Form("pt_jet_%s%s" ,l,x)  ,1500 , 0   , 1500  );
   h1_[Form("eta_jet_%s%s" , l,x)]  = std::make_shared<TH1F>( Form("eta_jet%s",x) , Form("eta_jet_%s%s",l,x)  , 600 , -3, 3 );
   h1_[Form("phi_jet_%s%s" , l,x)]  = std::make_shared<TH1F>( Form("phi_jet%s",x) , Form("phi_jet_%s%s",l,x)  , 360 , -180, 180 );
   if ( config_->btagAlgorithm() != "" )
      h1_[Form("btag_jet_%s%s", l,x)]  = std::make_shared<TH1F>(Form("btag_jet%s",x), Form("btag_jet_%s%s",l,x) , nbins_btag_, &bins_btag_[0] );
   
   // 2D histograms
   h2_[Form("pt_eta_jet_%s%s",l,x)]  = std::make_shared<TH2F>(Form("pt_eta_jet%s",x) , Form("pt_eta_jet_%s%s",l,x) ,1500 , 0   , 1500, 600, -3, 3  );
   
   
   // Histo titles
   h1_[Form("pt_jet_%s%s" , l,x)] -> GetXaxis() -> SetTitle("Jet p_{T} [GeV]");
   h1_[Form("eta_jet_%s%s", l,x)] -> GetXaxis() -> SetTitle("Jet  #eta");
   h1_[Form("phi_jet_%s%s", l,x)] -> GetXaxis() -> SetTitle("Jet  #phi");
   h1_[Form("btag_jet_%s%s",l,x)] -> GetXaxis() -> SetTitle("Jet btag discriminator");
   h2_[Form("pt_eta_jet_%s%s",l,x)] -> GetXaxis() -> SetTitle("Jet p_{T} [GeV]");
   h2_[Form("pt_eta_jet_%s%s",l,x)] -> GetYaxis() -> SetTitle("Jet #eta");

}

void BTaggingAnalyser::fillHistograms( const int & rank, const std::string & label, const float & sf )
{
   fill_histograms(rank,label,sf);
   if ( config_->isMC() && config_->histogramJetsPerFlavour() )
   {
      std::string flv = "udsg";
      int j = rank-1;
      auto jet = selectedJets_[j];
      if ( config_ -> useJetsExtendedFlavour() )
      {
         flv = jet->extendedFlavour();
      }
      else
      {
         if ( abs(jet->flavour()) == 4 ) flv = "c"; 
         if ( abs(jet->flavour()) == 5 ) flv = "b"; 
      }
      fill_histograms(rank,label,sf,flv);
   }
   
}

void BTaggingAnalyser::fill_histograms( const int & rank, const std::string & label, const float & sf, const std::string & extra )
{
   if ( rank > config_->nJetsMin() ) 
   {
      return;
   }
   if ( label == "" ) return;
   
   this->output()->cd();
   this->output()->cd(label.c_str());
   
   std::string xx = "";
   if ( extra != "" ) xx = "_"+extra;;
   const char * x = xx.c_str();
   const char * l = label.c_str();
   
   
   int j = rank-1;
   auto jet = selectedJets_[j];
   // 1D histograms
   h1_[Form("pt_jet_%s%s" , l,x)]  -> Fill(jet->pt(),weight_*sf);
   h1_[Form("eta_jet_%s%s", l,x)]  -> Fill(jet->eta(),weight_*sf);
   h1_[Form("phi_jet_%s%s", l,x)]  -> Fill(jet->phi()*180./acos(-1.),weight_*sf);
   if ( config_->btagAlgorithm() != "")
   {
      float mybtag = JetAnalyser::btag(*jet,config_->btagAlgorithm());
      h1_[Form("btag_jet_%s%s",l,x)] -> Fill(mybtag,weight_*sf);
   }
   
   // 2D histograms
   h2_[Form("pt_eta_jet_%s%s",l,x)] -> Fill(jet->pt(), jet->eta(), weight_*sf);
   
   
}

void BTaggingAnalyser::btag_binning()
{
   // uniform binning for btag
   float size = 0.0002;
   nbins_btag_ = int(1./size);
   bins_btag_.clear();
   for ( int i = 0; i<nbins_btag_+1; ++i)
      bins_btag_.push_back(size*i);
   
}
bool BTaggingAnalyser::selectionLeadJets()
{
   bool ok = true;
   for ( int j1 = 1; j1 <= this->config()->nJetsMin(); ++j1 )
   {
      if ( ! this->selectionJet(j1) ) 
      {
         ok = false;
         break;
      }
   }
   return ok;
   
}
bool BTaggingAnalyser::selectionLeadJetsDphi()
{
   bool ok = true;
   for ( int j1 = 1; j1 <= this->config()->nJetsMin(); ++j1 )
   {
      for ( int j2 = j1+1; j2 <= this->config()->nJetsMin(); ++j2 )
      {
         if ( ! this->selectionJetDphi(j1,j2) )
         {
            ok = false;
            break;
         }
      }
      if ( ! ok ) break;
   }
   return ok;
   
}
