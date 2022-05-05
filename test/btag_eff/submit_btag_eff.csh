#!/bin/csh -f

if ( $#argv < 5 ) then
   echo "You must enter the year, the type (sl or fh), and the trigger (trg or notrg), btag algo, btag wp, [status|hadd, condor_timestamp_dir (e.g. condor/20220504)]"
   exit
endif   

set year = $1
set type = $2
set trg = $3
set balgo = $4
set bwp = $5

if ( ! -d 'condor' ) then
   echo "condor directory does not exist. Create it on nfs and link here."
   exit
endif

set name  = 'btag_eff_'$balgo'_'$bwp'_'$type'_'$year'_'$trg
set samples = "QCD_HT100to200 QCD_HT200to300 QCD_HT300to500 QCD_HT500to700 QCD_HT700to1000 QCD_HT1500to2000 QCD_HT2000toInf"
if ( $type == "sl" ) then
   set samples = "QCD_Pt-50To80_MuEnrichedPt5 QCD_Pt-80To120_MuEnrichedPt5 QCD_Pt-120To170_MuEnrichedPt5 QCD_Pt-170To300_MuEnrichedPt5 QCD_Pt-300To470_MuEnrichedPt5 QCD_Pt-470To600_MuEnrichedPt5 QCD_Pt-600To800_MuEnrichedPt5 QCD_Pt-800To1000_MuEnrichedPt5 QCD_Pt-1000ToInf_MuEnrichedPt5"
endif


# Submit jobs
if ( $#argv == 5 ) then
   # config
   set cfg = $name'.cfg'
   if ( ! -e $cfg ) then
      echo "$cfg file does not exist"
      exit
   endif
   # condor dirs
   set timestamp = `date +%Y%m%d`
   if ( ! -d condor/$timestamp ) then 
      mkdir -p condor/$timestamp
   endif
   cp -p $cfg condor/$timestamp
   cd condor/$timestamp
   # inputs   
   set filesdir = '/afs/desy.de/user/w/walsh/issues/cms/10/dev/CMSSW_10_6_29/src/Analysis/Tools/data/ntuples/2017/v6/mc'
   # submit to naf   
   foreach sample ( $samples )
      set filelist = $filesdir'/'$sample'_rootFileList.txt'
      set output = 'histograms_'$sample'_'$name'.root'
      naf_submit.py -e BTagEfficiency -c $cfg -n $filelist -o $output -l $sample -x 1
   end
   cd -
endif

if ( $#argv == 6 ) then
   echo "You must enter the year, the type (sl or fh), and the trigger (trg or notrg), btag algo, btag wp, status|hadd, condor_timestamp_dir (e.g. condor/20220504)"
   exit
endif

# Check status or add histos
if ( $#argv == 7 ) then
   set option = $6
   set timestamp_dir = $7
   set mydir = `pwd`
   cd $timestamp_dir
   foreach sample ( $samples )
      set condor_dir = 'Condor_BTagEfficiency_'$name'_'$sample
      if ( $option == "status" ) then
         naf_submit.py --status --dir $condor_dir
      endif
      if ( $option == "hadd" ) then
         cd $condor_dir
         hadd2.csh finished_jobs
         cp -p histograms_*.root ../
         cd -
      endif
   end
   cd $mydir
endif

# queue status
echo "--------------"
echo "OWNER BATCH_NAME      SUBMITTED   DONE   RUN    IDLE   HOLD  TOTAL JOB_IDS"
condor_q  | grep "$USER ID"
echo tchau!

exit
