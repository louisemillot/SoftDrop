#!/usr/bin/env bash

# An example for a DPL Pythia8 event generation (without vertex smearing) and injection into analysis framework

set -x
declare -a namesArray=(\
"pythia")
options0=" --configuration json://dpl-config2.json"
# options0="-b --configuration json://dpl-config-hybrid-tracks-run2-deriveddataproducer.json"

declare -a jsonsArray=("$options0")

# --aggregate-timeframe 10 is used to combine 10 generated events into a timeframe that is then converted to AOD tables
# note that if you need special configuration for the analysis tasks, it needs to be passed to proxy and converter as well



# if you want event generator un-comment these following 2 lines
# o2-sim-dpl-eventgen ${jsonsArray[$i]} |\
# o2-sim-mctracks-to-aod ${jsonsArray[$i]} |\

o2-analysis-je-mctracks-to-aod-softdrop ${jsonsArray[$i]} | \




o2-analysis-je-jet-deriveddata-producer ${jsonsArray[$i]} | \
o2-analysis-bc-converter ${jsonsArray[$i]} | \
o2-analysis-run2bcinfos-converter ${jsonsArray[$i]} | \
o2-analysis-collision-converter ${jsonsArray[$i]} | \
o2-analysis-zdc-converter  ${jsonsArray[$i]} | \

o2-analysis-timestamp ${jsonsArray[$i]} | \
o2-analysis-event-selection ${jsonsArray[$i]} | \
o2-analysis-centrality-table ${jsonsArray[$i]} | \
o2-analysis-multiplicity-table ${jsonsArray[$i]} | \
o2-analysis-track-dca-filler-run2 ${jsonsArray[$i]} | \

# o2-analysis-mc-converter ${jsonsArray[$i]} | \
o2-analysis-mccollision-converter ${jsonsArray[$i]} | \
o2-analysis-trackselection ${jsonsArray[$i]} | \
o2-analysis-tracks-extra-v002-converter ${jsonsArray[$i]} | \


o2-analysis-ft0-corrected-table ${jsonsArray[$i]} | \
 
o2-analysis-je-jet-finder-data-charged ${jsonsArray[$i]} | \
o2-analysis-je-track-efficiency ${jsonsArray[$i]} | \
   
o2-analysis-je-jet-spectra-charged ${jsonsArray[$i]} | \

o2-analysis-je-estimator-rho ${jsonsArray[$i]} &> pythia8.log
   




# the very same analysis task can also directly run on an AO2D with McCollisions and McParticles:
# o2-analysis-mctracks-to-aod-simple-task -b --aod-file <AO2DFile>
# mv AnalysisResults.root AnalysisResults_hi_${namesArray[$i]}.root