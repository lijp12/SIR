
launchThreads(){
	dataDir=$1
	splitDir=$2
	midDir=$3

	inputSps=$(ls -1 $splitDir)
	
	for split in $inputSps
	do
		bash run.sh $dataDir/entity.txt $splitDir/$split ./connected_pairs0.5.txt  NNTripletFinal0.5/$split > $midDir/$split &
	done
	wait
}

#Arguments:
dataDir=../FB15k-simple
splitDir=../SchemaFiltPair/tripletFinal
midDir=mid


cd $(dirname $0)
launchThreads $dataDir $splitDir $midDir
