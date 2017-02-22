lambdas=(0.0015)
batchsizes=(1000)
dims=(100)
etas=(1)
dataPrefix=../../FB15k-simple/

resultPrefix=../../TransH-dim100-lr0.0015-margin0.5-br-nr/result
# mkdir $resultPrefix

for dim in ${dims[@]}; do
	for batchsize in ${batchsizes[@]}; do
		for lambda in ${lambdas[@]}; do
			for eta in ${etas[@]}; do
				time ./rank -dim $dim \
					-entitylist $dataPrefix/entity.txt \
					-rellist $dataPrefix/relation.txt \
					-mainRole ../../genMainRole/mainRole.txt \
					-trainM $dataPrefix/train.txt \
					-testM $dataPrefix/test.txt \
					-candidateInstance ../OgenCandidate/candidateTriplet.txt \
					-bias_out $resultPrefix/bias2vec.dim${dim}.size${batchsize}.lambda${lambda}.eta${eta} \
					-entity_out $resultPrefix/entity2vec.dim${dim}.size${batchsize}.lambda${lambda}.eta${eta} \
					-normal_out $resultPrefix/normal2vec.dim${dim}.size${batchsize}.lambda${lambda}.eta${eta} \
					-a_out $resultPrefix/tranf2vec.dim${dim}.size${batchsize}.lambda${lambda}.eta${eta} \
					-eta $eta
			done
		done
	done
done

