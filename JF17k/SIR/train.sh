

lambdas=(0.0015)
batchsizes=(1000)
dims=(100)
etas=(1)
dataPrefix=../JF17k-simple/version1/

resultPrefix=result
# mkdir $resultPrefix

for dim in ${dims[@]}; do
	for batchsize in ${batchsizes[@]}; do
		for lambda in ${lambdas[@]}; do
			for eta in ${etas[@]}; do
				time ./mFold -dim $dim -epoch 100 -batch $batchsize -lr $lambda -margin 0.5 -epsilon 0.01 -beta 0.001 \
					-entity $dataPrefix/entity.txt \
					-rel $dataPrefix/relation.txt \
					-train $dataPrefix/train.txt \
					-bias_out $resultPrefix/bias2vec.dim${dim}.size${batchsize}.lambda${lambda}.eta${eta} \
					-entity_out $resultPrefix/embedding.txt \
					-normal_out $resultPrefix/normal2vec.dim${dim}.size${batchsize}.lambda${lambda}.eta${eta} \
					-a_out $resultPrefix/tranf2vec.dim${dim}.size${batchsize}.lambda${lambda}.eta${eta} \
					-eta $eta \
					-flag $1
				#echo dim:$dim, lambda:$lambda, batchsize:$batchsize, eta:$eta
				#bash arma_test/test_algo3_without.sh $dim $lambda $batchsize $eta >> result.algo3_without
			done
		done
	done
done
