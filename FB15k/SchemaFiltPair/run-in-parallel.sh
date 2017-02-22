
init(){
	splitDir=$1
	midDir=$2
	
	if [ ! -d $midDir ]; then
		#Tip: The bracket expression here is equivalent to "test -d" command, which checks if
		#	the corresponding directory exists. Type "man test" to see more info. 
		mkdir $midDir
	fi
	
	if [ ! -d $splitDir ]; then
		mkdir $splitDir
	fi
	
	rm $splitDir/* $midDir/*
}

splitTest(){
	testFile=$1
	splitNum=$2
	splitDir=$3
	
	totalSize=$(cat $testFile | wc -l)
	splitSize=$(($totalSize / $splitNum))
	echo Split the test file into $splitNum portions, with $splitSize instances in each split. 

	split -l $splitSize $testFile  $splitDir/split-
}

launchThreads(){
	dataDir=$1
	splitDir=$2
	midDir=$3 

	inputSps=$(ls -1 $splitDir)
	
	for split in $inputSps
	do
		bash run.sh $splitDir/$split $dataDir/entity.txt $dataDir/Type/type.txt $dataDir/Type/entityTypeSimple.txt $dataDir/Type/relation-schema-simple.txt tripletFinal/$split.txt pairFinal/$split.txt > $midDir/$split &
	done
	wait
}

#Arguments:
splitNum=10
dataDir=../FB15k-simple
splitDir=inputSplits
midDir=mid


cd $(dirname $0)
init $splitDir $midDir
splitTest $dataDir/entity.txt $splitNum $splitDir
launchThreads $dataDir $splitDir $midDir
