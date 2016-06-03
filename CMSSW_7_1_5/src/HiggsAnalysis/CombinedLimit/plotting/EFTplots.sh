
#lumi=$1

# get the data
#for model in invisibleHiggs D5a D5b
#do
#  for lumi in 20 300 3000 
#  do
#    python EFTlimits.py $model $lumi
#  done
#done

# plot the data one model per plot
#for model in D5a D5b D5c
#do
#    python plotEFTlumis.py ${model}/combined_${model}_3000fb.root ${model}/combined_${model}_300fb.root ${model}/combined_${model}_20fb.root
#done

# plot the data, dimension per plot
# D5
#python plot4EFTs.py D5a/combined_D5a_3000fb.root D5a/combined_D5a_300fb.root D5a/combined_D5a_20fb.root D5b/combined_D5b_3000fb.root D5b/combined_D5b_300fb.root D5b/combined_D5b_20fb.root D5c/combined_D5c_3000fb.root D5c/combined_D5c_300fb.root D5c/combined_D5c_20fb.root D5d/combined_D5d_3000fb.root D5d/combined_D5d_300fb.root D5d/combined_D5d_20fb.root
#python plot2EFTs.py D5a/combined_D5a_3000fb.root D5a/combined_D5a_300fb.root D5a/combined_D5a_20fb.root D5b/combined_D5b_3000fb.root D5b/combined_D5b_300fb.root D5b/combined_D5b_20fb.root
# D6
# doesnt work i think
#python plot4EFTs.py D6a/combined_D6a_3000fb.root D6a/combined_D6a_300fb.root D6a/combined_D6a_20fb.root D6b/combined_D6b_3000fb.root D6b/combined_D6b_300fb.root D6b/combined_D6b_20fb.root
# D7
#python plot4EFTs.py D7a/combined_D7a_3000fb.root D7a/combined_D7a_300fb.root D7a/combined_D7a_20fb.root D7b/combined_D7b_3000fb.root D7b/combined_D7b_300fb.root D7b/combined_D7b_20fb.root D7c/combined_D7c_3000fb.root D7c/combined_D7c_300fb.root D7c/combined_D7c_20fb.root D7d/combined_D7d_3000fb.root D7d/combined_D7d_300fb.root D7d/combined_D7d_20fb.root

#scarcer data
# D5
#python plot4EFTs.py D5a/combined_D5a_3000fb.root D5a/combined_D5a_300fb.root D5a/combined_D5a_20fb.root D5b/combined_D5b_3000fb.root D5b/combined_D5b_300fb.root D5b/combined_D5b_20fb.root D5c/combined_D5c_3000fb.root D5c/combined_D5c_300fb.root D5c/combined_D5c_20fb.root D5d/combined_D5d_3000fb.root D5d/combined_D5d_300fb.root D5d/combined_D5d_20fb.root
#python plot2EFTs.py D5c/combined_D5c_3000fb.root D5c/combined_D5c_300fb.root D5c/combined_D5c_20fb.root D5d/combined_D5d_3000fb.root D5d/combined_D5d_300fb.root D5d/combined_D5d_20fb.root
# D6
#python plot2EFTs.py D6a/combined_D6a_3000fb.root D6a/combined_D6a_300fb.root D6a/combined_D6a_20fb.root D6b/combined_D6b_3000fb.root D6b/combined_D6b_300fb.root D6b/combined_D6b_20fb.root
# D7
#python plot2EFTs.py D7a/combined_D7a_3000fb.root D7a/combined_D7a_300fb.root D7a/combined_D7a_20fb.root D7c/combined_D7c_3000fb.root D7c/combined_D7c_300fb.root D7c/combined_D7c_20fb.root
