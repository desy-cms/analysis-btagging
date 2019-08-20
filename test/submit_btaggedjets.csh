#!/bin/csh -f

if ( $#argv < 1 ) then
   echo "Usage: submit.csh HT_bin [btag_wp=medium] [btag_algo=deepflavour] [test=0]"
   exit
endif

set htbin    = $1
set btagwp   = $2
if ( $btagwp != "loose" && $btagwp != "medium" &&  $btagwp != "tight ") then
   set btagwp = "medium"
endif
set btagalgo = $3
if ( $btagalgo != "deepflavour" && $btagalgo != "deepcsv" ) then
   set btagalgo = "deepflavour"
endif
@ test       = 0
if ( $#argv == 4 ) then
   @ test = $4
endif
set nevents  = -1
set breg     = "true"

if ( $test == 1 ) then
   echo "Just the configuration will be produced."
   echo "No jobs will be submitted" 
endif


# defaults deepflavour
set btagloose  = 0.0521
set btagmedium = 0.3033
set btagtight  = 0.7489
set jerptres = Fall17_V3_MC_PtResolution_AK4PFchs.txt
set jersf    = Fall17_V3_MC_SF_AK4PFchs.txt
set btagsf   = DeepFlavour_94XSF_V1_B_F.csv
# in case deepcsv
if ( $btagalgo == "deepcsv" ) then
   set btagloose  = 0.1522
   set btagmedium = 0.4941
   set btagtight  = 0.8001
   set btagsf = DeepCSV_94XSF_V3_B_F.csv
endif

set mypileup = "PileupWeight_Run2017CDEF_QCD_"$htbin".root"

set rootfilelist = "../ntuples-2017/qcd_madgraph/rootFileList_QCD_"$htbin"_TuneCP5_13TeV-madgraph-pythia8_ntuplizer_94X_mc_2017_fall17-v4.txt"

set outputroot = "Histograms_QCD_"$htbin"_"$btagalgo"_"$btagwp".root"

set oldcfg = "btaggedjets.cfg"
set newcfg = "btaggedjets_QCD_"$htbin"_"$btagalgo"_"$btagwp".cfg"

rm -f $newcfg > /dev/null
cp -p $oldcfg $newcfg

sed -i "s~NUM_EVENTS~$nevents~g"                $newcfg
sed -i "s~ROOTFILELIST~$rootfilelist~g"         $newcfg
sed -i "s~OUTPUTROOT~$outputroot~g"             $newcfg
sed -i "s~BTAG_ALGO~$btagalgo~g"                $newcfg
sed -i "s~BTAG_LOOSE~$btagloose~g"              $newcfg
sed -i "s~BTAG_MEDIUM~$btagmedium~g"            $newcfg
sed -i "s~BTAG_TIGHT~$btagtight~g"              $newcfg
sed -i "s~BTAG_WP~$btagwp~g"                    $newcfg
sed -i "s~BTAG_SF~$btagsf~g"                    $newcfg
sed -i "s~JER_PTRESOLUTION~$jerptres~g"         $newcfg
sed -i "s~JER_SF~$jersf~g"                      $newcfg
sed -i "s~BJET_REGRESSION~$breg~g"              $newcfg
sed -i "s~PILEUP_WEIGHT~$mypileup~g"            $newcfg



# comment below for tests
if ( $test == 0 ) then
   naf_mult_submit.py -e BTaggedJets -c $newcfg -x 10
   rm -f $newcfg > /dev/null
endif

exit
