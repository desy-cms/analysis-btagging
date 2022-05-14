# Offline b-tag efficiencies

## Synopsis

In the macro `Analysis/BTagging/bin/BTagEfficiency.cc` the leading jet of every event is probebd for its
flavour content and passing a b-tag selection. The madgraph HT binned general QCD MC is used for full
hadronic jets, whereas for semileptonic jets, the pythia8 QCD MuEnriched samples, providing larger
statistics, are used.

## Submit jobs

Go to the directory 
```bash 
cd $CMSSW_BASE/src/Analysis/BTagging/test/btag_eff
```
You can use the script `submit_btag.py`. It considers that the configuration file name follows a
naming scheme: `btag_eff_<balgo>_<bwp>_<mode>_<year>_<trg>.cfg`

* `balgo`: btag algorithm, e.g. `deepjet`
* `bwp  `: btag working point, e.g. `medium`
* `mode `: `fh` for fullhadronic, `sl` for semileptonic
* `year `: year of data; e.g. `2017`
* `trg  `: `trg` when trigger is used, `notrg` when no trigger is used

:warning: In `$CMSSW_BASE/src/Analysis/BTagging/test/btag_eff` you need to create a directory called `condor`.
It is recommended that you create it in `nfs` or a file system, other than `afs`, with large quota. Then link
that directory in the `btag_eff` directory calling the link `condor`.

### Example
```bash
submit_btag.py \
--exe BTagEfficiency \
--cfg btag_eff_deepjet_medium_sl_2017_trg.cfg \
--label test \
--samples qcd_muenriched.txt \
--submit
```

To obtain the status of the submission, replace `--submit` by `status`. If jobs failed, use `--resubmit` instead.

### Samples file
Is a file containging information about the samples to be processed. The first line is the path to the rootFileList
in `$CMSSW_BASE/src`. The other lines are the aliases of the samples, i.e. the prefix of the rootFileList.txt files:

````
Analysis/Tools/data/ntuples/2017/v6/mc
QCD_HT100to200
QCD_HT200to300
QCD_HT300to500
QCD_HT500to700
QCD_HT700to1000
QCD_HT1000to1500
QCD_HT1500to2000
QCD_HT2000toInf
``` 

## Results
Once all jobs are finished, merge the root files, using the action `--hadd` instead of `--submit` in the command above.
The results will be available in the `./results/label` directory. 

:warning: The `results` directory can be in `afs`, but the  recommendation for the `condor` directory also applies for `results`.

