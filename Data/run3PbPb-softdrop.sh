#!/usr/bin/env bash

set -x
declare -a namesArray=(\
""PbPb_LHC23zzh_pass4_544123_0510"")

options0=" --configuration json://../dpl-run3PbPb-softdrop.json"

declare -a jsonsArray=("$options0")

# Extract parameters from JSON for filename


# --aggregate-timeframe 10 is used to combine 10 generated events into a timeframe that is then converted to AOD tables
# note that if you need special configuration for the analysis tasks, it needs to be passed to proxy and converter as well

# Construct output filename
# output_filename="AnalysisResults_${namesArray[0]}_R${R}_pt${ptmin}_zcut${z_cut}_beta${beta}_n${n}.root"

# output_filename="AnalysisResults_${namesArray[0]}_R${R}_pt${ptmin}_zcut${z_cut}_beta${beta}_n${n}.root"

# if you want event generator, un-comment these following 2 lines
# o2-sim-dpl-eventgen ${jsonsArray[$i]} |\
# o2-sim-mctracks-to-aod ${jsonsArray[$i]} |\



o2-analysis-je-jet-deriveddata-producer ${jsonsArray[$i]} | \

o2-analysis-timestamp ${jsonsArray[$i]} | \

o2-analysis-event-selection ${jsonsArray[$i]} | \

o2-analysis-centrality-table ${jsonsArray[$i]} | \

o2-analysis-multiplicity-table ${jsonsArray[$i]} | \

o2-analysis-trackselection ${jsonsArray[$i]} | \

o2-analysis-tracks-extra-v002-converter ${jsonsArray[$i]} | \

o2-analysis-track-propagation ${jsonsArray[$i]} | \

o2-analysis-je-jet-finder-data-charged ${jsonsArray[$i]} | \

o2-analysis-je-jet-substructure-softdrop ${jsonsArray[$i]} &> log_sans-filtres.txt

 
   




# the very same analysis task can also directly run on an AO2D with McCollisions and McParticles:
# o2-analysis-mctracks-to-aod-simple-task -b --aod-file <AO2DFile>
# Rename the output file
# mv AnalysisResults.root $output_filename