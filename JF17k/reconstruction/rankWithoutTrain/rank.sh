lambdas=(0.0015)
batchsizes=(1000)
dims=(100)
etas=(1)
dataPrefix=../../JF17k-simple/version1/

resultPrefix=../../SIR/result
# mkdir $resultPrefix

for dim in ${dims[@]}; do
	for batchsize in ${batchsizes[@]}; do
		for lambda in ${lambdas[@]}; do
			for eta in ${etas[@]}; do
				time ./rank -dim $dim \
					-entitylist $dataPrefix/entity.txt \
					-rellist $dataPrefix/relation.txt \
					-mainRole ../../mainRole.txt \
					-trainM $dataPrefix/train.txt \
					-testM ../hitTest.txt \
					-candidateInstance ../candidateClique/candidateCliqueOther.txt \
					-bias_out $resultPrefix/bias2vec.dim${dim}.size${batchsize}.lambda${lambda}.eta${eta} \
					-entity_out $resultPrefix/embedding.txt \
					-normal_out $resultPrefix/normal2vec.dim${dim}.size${batchsize}.lambda${lambda}.eta${eta} \
					-a_out $resultPrefix/tranf2vec.dim${dim}.size${batchsize}.lambda${lambda}.eta${eta} \
					-eta $eta
			done
		done
	done
done

