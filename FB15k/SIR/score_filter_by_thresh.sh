/usr/bin/g++ score_to_pair_with_threshold.cpp -std=c++11

entity_num_with_junk=$1
interval=$2

for((thresh=3; thresh <= 8; thresh+=1))
do
	echo 0.$thresh
	./a.out 0.$thresh $entity_num_with_junk $interval &
done
wait
