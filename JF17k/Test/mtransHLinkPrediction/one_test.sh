dirname $0
cd `dirname $0`


dataPrefix=$1
resultPrefix=$2
splitTest=$3
dim=100
lambda=0.0015
batchsize=1000
eta=1


echo $workPath
echo dim:$dim, lambda:$lambda, batchsize:$batchsize, eta:$eta
./evaluate_direct_without_detail \
		$dataPrefix/entity.txt \
		$dataPrefix/relation.txt \
		$resultPrefix/entity2vec.dim${dim}.size${batchsize}.lambda${lambda}.eta${eta} \
		$resultPrefix/bias2vec.dim${dim}.size${batchsize}.lambda${lambda}.eta${eta} \
		$resultPrefix/normal2vec.dim${dim}.size${batchsize}.lambda${lambda}.eta${eta} \
		$resultPrefix/tranf2vec.dim${dim}.size${batchsize}.lambda${lambda}.eta${eta} \
		$splitTest \
		splited_relation \
		$dataPrefix/entity.txt \
		$4
echo "" 
