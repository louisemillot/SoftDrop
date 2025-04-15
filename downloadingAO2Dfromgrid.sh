# will download all the fileType files found inside the alienOriginFolder folder, while preserving folder structureAO2Dtype=data

AO2Dtype=sim
productionName=LHC20e3a
fileType=AO2D.root
nFilesToDownload=240
nFilesToOmit=0

alienOriginFolder=/alice/sim/2020/$productionName/296749/PWGZZ/Run3_Conversion/334_20220726-2035

# destinationFolder=/eos/home-u/username/LxplusWorkspace/AO2D_Downloads/$AO2Dtype/$ProductionName # if downloading to cern disk, with home-u and username set according to user account
destinationFolder=~/alice/MyWork/AO2D_Downloads/$AO2Dtype/$ProductionName # if downloading to local

alien.py cp -retry 2 -l $nFilesToDownload -o $nFilesToOmit -glob $fileType alien:$alienOriginFolder file:$destinationFolder/

# -o int : skip first <offset> files found in the src directory (for recursive copy)
# /eos/home-u/user/ folder has lot of disk space
# will download all the fileType files found inside the alienOriginFolder folder, while preserving folder structure