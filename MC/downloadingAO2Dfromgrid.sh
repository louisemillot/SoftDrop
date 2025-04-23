# will download all the fileType files found inside the alienOriginFolder folder, while preserving folder structureAO2Dtype=data

AO2Dtype=sim
productionName=LHC24g3
fileType=AO2D.root
nFilesToDownload=10
nFilesToOmit=0

alienOriginFolder=/alice/sim/2024/$productionName/0/544491/

# destinationFolder=/eos/home-u/username/LxplusWorkspace/AO2D_Downloads/$AO2Dtype/$ProductionName # if downloading to cern disk, with home-u and username set according to user account
destinationFolder=~/alice/MyWork/AO2D_Downloads/$AO2Dtype/$ProductionName # if downloading to local

alien.py cp -retry 2 -l $nFilesToDownload -o $nFilesToOmit -glob $fileType alien:$alienOriginFolder file:$destinationFolder/

# # -o int : skip first <offset> files found in the src directory (for recursive copy)
# # /eos/home-u/user/ folder has lot of disk space
# # will download all the fileType files found inside the alienOriginFolder folder, while preserving folder structure


# AO2Dtype=sim
# productionName=LHC20e3a
# fileType=AO2D.root
# nFilesToDownload=10
# nFilesToOmit=0

# alienOriginFolder=/alice/sim/2020/$productionName/296749/PWGZZ/Run3_Conversion/334_20220726-2035

# # destinationFolder=/eos/home-u/username/LxplusWorkspace/AO2D_Downloads/$AO2Dtype/$ProductionName # if downloading to cern disk, with home-u and username set according to user account
# destinationFolder=~/alice/MyWork/AO2D_Downloads/$AO2Dtype/$ProductionName # if downloading to local

# alien.py cp -retry 2 -l $nFilesToDownload -o $nFilesToOmit -glob $fileType alien:$alienOriginFolder file:$destinationFolder/

# -o int : skip first <offset> files found in the src directory (for recursive copy)
# /eos/home-u/user/ folder has lot of disk space
# will download all the fileType files found inside the alienOriginFolder folder, while preserving folder structure

# AO2Dtype=data
# productionName=LHC18q
# fileType=AO2D.root
# nFilesToDownload=1
# nFilesToOmit=0

# alienOriginFolder=/alice/data/2018/LHC18q/000296132/pass3/PWGZZ/Run3_Conversion/339_20220722-1611_child_2

# # destinationFolder=/eos/home-u/username/LxplusWorkspace/AO2D_Downloads/$AO2Dtype/$ProductionName # if downloading to cern disk, with home-u and username set according to user account
# destinationFolder=~/alice/MyWork/AO2D_Downloads/$AO2Dtype/$ProductionName # if downloading to local

# alien.py cp -retry 2 -l $nFilesToDownload -o $nFilesToOmit -glob $fileType alien:$alienOriginFolder file:$destinationFolder/

# # -o int : skip first <offset> files found in the src directory (for recursive copy)
# # /eos/home-u/user/ folder has lot of disk space
# # will download all the fileType files found inside the alienOriginFolder folder, while preserving folder structure