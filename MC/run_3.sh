#!/usr/bin/env bash

# An example for a DPL Pythia8 event generation (without vertex smearing) and injection into analysis framework

set -x
declare -a namesArray=(\
""PbPb_LHC24g3"")

options0=" --configuration json://../dpl-config_Run3.json"

declare -a jsonsArray=("$options0")

# Extract parameters from JSON for filename
R=$(jq -r '.["my-custom-task"].R' "../dpl-config_Run3.json")
ptmin=$(jq -r '.["my-custom-task"].ptmin' "../dpl-config_Run3.json")
z_cut=$(jq -r '.["my-custom-task"].z_cut' "../dpl-config_Run3.json")
beta=$(jq -r '.["my-custom-task"].beta' "../dpl-config_Run3.json")
n=$(jq -r '.["my-custom-task"].n' "../dpl-config_Run3.json")

# --aggregate-timeframe 10 is used to combine 10 generated events into a timeframe that is then converted to AOD tables
# note that if you need special configuration for the analysis tasks, it needs to be passed to proxy and converter as well

# Construct output filename
# output_filename="AnalysisResults_${namesArray[0]}_R${R}_pt${ptmin}_zcut${z_cut}_beta${beta}_n${n}.root"
output_filename="AnalysisResults_${namesArray[0]}_R${R}_pt${ptmin}_zcut${z_cut}_beta${beta}_n${n}.root"

# if you want event generator, un-comment these following 2 lines
# o2-sim-dpl-eventgen ${jsonsArray[$i]} |\
# o2-sim-mctracks-to-aod ${jsonsArray[$i]} |\

o2-analysis-je-mctracks-to-aod-softdrop ${jsonsArray[$i]} | \

o2-analysis-je-jet-deriveddata-producer ${jsonsArray[$i]} | \
# o2-analysis-bc-converter ${jsonsArray[$i]} | \
# o2-analysis-run2bcinfos-converter ${jsonsArray[$i]} | \
# o2-analysis-collision-converter ${jsonsArray[$i]} | \
# o2-analysis-zdc-converter  ${jsonsArray[$i]} | \

o2-analysis-timestamp ${jsonsArray[$i]} | \
o2-analysis-event-selection ${jsonsArray[$i]} | \
o2-analysis-centrality-table ${jsonsArray[$i]} | \
o2-analysis-multiplicity-table ${jsonsArray[$i]} | \
# o2-analysis-track-dca-filler-run2 ${jsonsArray[$i]} | \

# o2-analysis-mc-converter ${jsonsArray[$i]} | \
o2-analysis-mccollision-converter ${jsonsArray[$i]} | \
o2-analysis-trackselection ${jsonsArray[$i]} | \
o2-analysis-tracks-extra-v002-converter ${jsonsArray[$i]} | \
o2-analysis-track-propagation ${jsonsArray[$i]} | \



# o2-analysis-ft0-corrected-table ${jsonsArray[$i]} | \
 
o2-analysis-je-jet-finder-data-charged ${jsonsArray[$i]} | \
o2-analysis-je-track-efficiency ${jsonsArray[$i]} | \
   
# o2-analysis-je-jet-spectra-charged ${jsonsArray[$i]} | \

o2-analysis-je-estimator-rho ${jsonsArray[$i]} &> pythiaRun3.log 
   




# the very same analysis task can also directly run on an AO2D with McCollisions and McParticles:
# o2-analysis-mctracks-to-aod-simple-task -b --aod-file <AO2DFile>
# Rename the output file
mv AnalysisResults.root $output_filename