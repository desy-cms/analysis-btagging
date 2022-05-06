#!/bin/csh -f

if ( $#argv < 5 ) then
   echo "You must enter the year, the type (sl or fh), and the trigger (trg or notrg), btag algo, btag wp, ['xx_opts'] or [status|hadd, condor_timestamp_dir (e.g. condor/20220504)]"
   exit
endif   

if ( ! -d 'condor' ) then
   echo "condor directory does not exist. Create it on nfs (more disk space) and link here."
   exit
endif

set year = $1
set type = $2
set trg = $3
set balgo = $4
set bwp = $5
set opts = ""
if ( $#argv == 6 ) then
   set opts = $6
endif

set exe = "BTagWeightStudies"

set samplesdir = $CMSSW_BASE"/src/Analysis/Tools/data/ntuples/$year/v6/mc"
set name  = 'btag_weight_'$balgo'_'$bwp'_'$type'_'$year'_'$trg
set samples = "QCD_bEnriched_HT100to200 QCD_bEnriched_HT200to300 QCD_bEnriched_HT300to500 QCD_bEnriched_HT500to700 QCD_bEnriched_HT700to1000 QCD_bEnriched_HT1000to1500 QCD_bEnriched_HT1500to2000 QCD_bEnriched_HT2000toInf QCD_HT100to200_BGenFilter QCD_HT200to300_BGenFilter QCD_HT300to500_BGenFilter QCD_HT500to700_BGenFilter QCD_HT700to1000_BGenFilter QCD_HT1000to1500_BGenFilter QCD_HT1500to2000_BGenFilter QCD_HT2000toInf_BGenFilter"

# Submit jobs
if ( $#argv <= 6 ) then
   # config
   set cfg = $name'.cfg'
   if ( ! -e $cfg ) then
      echo "$cfg file does not exist"
      exit
   endif
   # condor dirs
   set timestamp = `date +%Y%m%d`
   if ( $opts != "" ) then
      set timestamp = $timestamp'_btagweight'
   endif
   if ( ! -d condor/$timestamp ) then 
      mkdir -p condor/$timestamp
   endif
   cp -p $cfg condor/$timestamp
   cd condor/$timestamp
   # inputs   
   
   # submit to naf   
   foreach sample ( $samples )
      set filelist = $samplesdir'/'$sample'_rootFileList.txt'
      set label = $sample
      set output = 'histograms_'$label'_'$name'.root'
      if ( $opts != "" ) then
         naf_submit.py -e $exe -c $cfg -n $filelist -o $output -l $label -x 1 --opts $opts
      else
         naf_submit.py -e $exe -c $cfg -n $filelist -o $output -l $label -x 1
      endif
   end
   cd -
endif

# Check status or add histos
if ( $#argv == 7 ) then
   set option = $6
   set timestamp_dir = $7
   set nocondor_dir = `echo $timestamp_dir | awk '{print substr($0,8)}'`
   set mydir = `pwd`
   if ( ! -d $mydir/$nocondor_dir/$name ) then
      mkdir -p $mydir/$nocondor_dir/$name
   endif
   cd $timestamp_dir
   foreach sample ( $samples )
      set condor_dir = 'Condor_'$exe'_'$name'_'$sample
      if ( $option == "status" ) then
         naf_submit.py --status --dir $condor_dir
      endif
      if ( $option == "hadd" ) then
         cd $condor_dir
         hadd2.csh finished_jobs
         cp -p histograms_*.root $mydir/$nocondor_dir/$name/
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
