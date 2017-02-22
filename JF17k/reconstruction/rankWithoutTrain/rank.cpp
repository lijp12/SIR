//#define ARMA_DONT_USE_CXX11
#include <iostream>
#include <fstream>
#include <armadillo>
#include <time.h>
#include <string>
#include <unordered_map>
#include <unordered_set>
#include <vector>
#include <sstream>
#include <cstdlib>
#include <iomanip>
#include <boost/functional/hash.hpp>
#include <boost/random.hpp>
#include <boost/random/linear_congruential.hpp>
#include <boost/random/variate_generator.hpp>
#include <boost/generator_iterator.hpp>
#include <boost/random/uniform_int.hpp>
using namespace std;
using namespace arma;

float eta;
size_t uvecHash(const uvec &v){
	return boost::hash_range(v.begin(), v.end());
}
bool eqOp(const uvec &lhs, const uvec &rhs){
	return all((lhs == rhs) == 1);
}

class Evaluator{
	unordered_map <string, int> entities2index;
	unordered_map <int, string> index2entities;
	unordered_map <string, int> relation2index;
	unordered_map <int, string> index2relation;
	unordered_map <int, int> relation2mainRole;
	
	vector <int> schema;
	using uvec_set = unordered_set <uvec, decltype(uvecHash)*, decltype(eqOp)* >;
	unordered_map <int, uvec_set> testPositive;
	unordered_map <int, uvec_set> trainPositive;
	vector<pair<int, uvec> > testData;
	unordered_map <string, vector<double> > candidateInstance;
	int ENT_NUM, REL_NUM;
	int DIM;

	mat ENT, BR, NR;
	vector<vec> A;
	
	mat project(const mat &_X, const vec &nr){
		return _X - nr * nr.t() * _X;
	}
	void loadBase(char *entListPath, char *relListPath, char *mainRoleDataPath){
		FILE *entFile, * relFile, *mainRoleFile;
		char str[500];
		int n;
		ENT_NUM = 0;
		REL_NUM = 0;
		entFile = fopen(entListPath, "r");
		while (fscanf(entFile, "%s", str) != EOF){
			entities2index[string(str)] = ENT_NUM;
			index2entities[ENT_NUM] = string(str);
			ENT_NUM++;
		}
		fclose(entFile);
		
		schema.clear();
		relFile = fopen(relListPath, "r");
		while (fscanf(relFile, "%s\t%d", str, &n) != EOF){
			schema.push_back(n == 0 ? 2 : n);
			relation2index[string(str)] = REL_NUM;
			index2relation[REL_NUM] = string(str);
			REL_NUM++;
		}
		fclose(relFile);
		
		mainRoleFile = fopen(mainRoleDataPath, "r");
		while (fscanf(mainRoleFile, "%s\t%d", str, &n) != EOF){
			relation2mainRole[relation2index[string(str)]] = n - 1;
		}
		fclose(mainRoleFile);
		
	}
	void loadTest(char *testDataPath, char *trainDataPath, char *candidateInstancePath){
		FILE *candidateInstanceFile, *testDataFile, *trainDataFile;
		char str[500];
		char mainEntity[500];
		char instance[500];
		int n;
		
		testDataFile = fopen(testDataPath, "r");
		while (fscanf(testDataFile, "%s\t%s", instance, str) != EOF){
			int relIndex = relation2index[string(str)];
			int cnt = schema[relIndex];
			uvec indices = zeros<uvec>(cnt);
			for (int i = 0; i < cnt; i++){
				fscanf(testDataFile, "%s", str);
				indices(i) = entities2index[string(str)];
			}
			testData.push_back(pair<int, uvec>(relIndex, indices));
			if (testPositive.count(relIndex) == 0){
				testPositive[relIndex] = uvec_set(500, uvecHash, eqOp);
			}
			testPositive[relIndex].insert(indices);
		}
		fclose(testDataFile);
		cout << "over test" << endl;
		
		trainDataFile = fopen(trainDataPath, "r");
		while (fscanf(trainDataFile, "%s", str) != EOF){
			int relIndex = relation2index[string(str)];
			int cnt = schema[relIndex];
			uvec indices = zeros<uvec>(cnt);
			for (int i = 0; i < cnt; i++){
				fscanf(testDataFile, "%s", str);
				indices(i) = entities2index[string(str)];
			}
			if (trainPositive.count(relIndex) == 0){
				trainPositive[relIndex] = uvec_set(500, uvecHash, eqOp);
			}
			trainPositive[relIndex].insert(indices);
		}
		fclose(trainDataFile);
		
		candidateInstanceFile = fopen(candidateInstancePath,"r");
		int count = 0;
		while (fscanf(candidateInstanceFile, "%s\t%s", str, mainEntity) != EOF){
			int relIndex = relation2index[string(str)];
			fscanf(candidateInstanceFile, "%d", &n);
			for (int k = 0; k < n; k++){
				count++;
				int cnt = schema[relIndex];
				uvec indices = zeros<uvec>(cnt);
				for (int i = 0; i < cnt; i++){
					fscanf(candidateInstanceFile, "%s", str);
					indices(i) = entities2index[string(str)];
				}
				if (testPositive.count(relIndex) == 0){
					if (trainPositive.count(relIndex) == 0){
						double score = lossFn(relIndex, indices);
						//double score = 0;
						candidateInstance[index2relation[relIndex] + "\t" + string(mainEntity)].push_back(score);
					}
					else{
						if (trainPositive[relIndex].count(indices) == 0){
							double score = lossFn(relIndex, indices);
							//double score = 0;
							candidateInstance[index2relation[relIndex] + "\t" + string(mainEntity)].push_back(score);
						}
					}
				}
				else{
					if (testPositive[relIndex].count(indices) == 0){
						if (trainPositive.count(relIndex) == 0){
							double score = lossFn(relIndex, indices);
							//double score = 0;
							candidateInstance[index2relation[relIndex] + "\t" + string(mainEntity)].push_back(score);
						}
						else{
							if (trainPositive[relIndex].count(indices) == 0){
								double score = lossFn(relIndex, indices);
								//double score = 0;
								candidateInstance[index2relation[relIndex] + "\t" + string(mainEntity)].push_back(score);
							}
						}
					}
				}
			}
		}
		fclose(candidateInstanceFile);
		cout << "count = " << count << endl;
		
	}
	void loadMat(int dim, char * bias_out, char *entity_out, char *normal_out, char *a_out){
		BR.load(bias_out);
		NR.load(normal_out);
		cout << "over Br,Nr" << endl;
		DIM = dim;
		ENT = zeros<mat>(DIM, ENT_NUM);
            
        ifstream in(entity_out);
            
        for(int i = 0; i < ENT.n_cols; i++)
        {
            for(int j = 0; j < ENT.n_rows; j++)
                in >> ENT(j, i);
        }
		cout << "over entity" << endl;
		
		cout << a_out << endl;
		FILE *f_transf = fopen(a_out, "rb");
		for (int i = 0; i < REL_NUM; i++){
			vec a = zeros<vec>(schema[i]);
			for (int j = 0; j < schema[i]; j++){
				double tmp;
				fscanf(f_transf, "%lf", &a(j));
			}
			A.push_back(a);
		}	
		fclose(f_transf);
		cout << "over Ar" << endl;
		
	}
	double lossFn(int rel, const uvec &indices){
		mat X = ENT.cols(indices);
		vec ar = A[rel];
		vec br = BR.col(rel);
		vec nr = NR.col(rel);
		mat Xr = project(X, nr);
		vec tmp = Xr * ar + br;
		return dot(tmp, tmp);
	}
	
	
public:
	Evaluator(int dim, char *entListPath, char *relListPath, char *mainRoleDataPath, char *testDataPath, char *trainDataPath ,char *candidateInstancePath,
		char * bias_out, char *entity_out, char *normal_out, char *a_out){
		loadBase(entListPath, relListPath, mainRoleDataPath);
		loadMat(dim, bias_out, entity_out, normal_out, a_out);
		loadTest(testDataPath, trainDataPath, candidateInstancePath);
		
	}
	void evaluate();
	
};

void Evaluator::evaluate(){
	ofstream result("../rank/rankResult.txt");
	cout << testData.size() << endl;
	for (int i = 0; i < testData.size(); i++){
		int relIndex = testData[i].first;
		uvec indices = testData[i].second;
		int mainEntityIndex = indices(relation2mainRole[relIndex]);
		int rank = 1;
		double score = lossFn(relIndex, indices);
		if (candidateInstance.count(index2relation[relIndex] + "\t" + index2entities[mainEntityIndex]) > 0){
			for (int k = 0; k < candidateInstance[index2relation[relIndex] + "\t" + index2entities[mainEntityIndex]].size(); k++){
				if (score >= candidateInstance[index2relation[relIndex] + "\t" + index2entities[mainEntityIndex]][k]){
					rank ++;
				}
			}
			result << index2relation[relIndex];
			for (int k = 0; k < indices.n_rows; k++){
				result << "\t" << index2entities[indices[k]];
			}
			result << "\t"  << candidateInstance[index2relation[relIndex] + "\t" + index2entities[mainEntityIndex]].size() << "\t" << rank <<endl;
		}
	}
	result.close();
}
	

int ArgPos(char *str, int argc, char **argv) {
	int a;
	for (a = 1; a < argc; a++) if (!strcmp(str, argv[a])) {
		if (a == argc - 1) {
			printf("Argument missing for %s\n", str);
			exit(1);
		}
		return a;
	}
	return -1;
}

int main(int argc, char ** argv){
	char *entListPath, *relListPath, *testDataPath, *mainRoleDataPath, *trainDataPath, *candidateInstancePath;
	char *bias_out, *entity_out, *normal_out, *a_out;
	int i, dim;
	
	if ((i = ArgPos((char *)"-dim", argc, argv)) > 0) dim = atoi(argv[i + 1]);
	if ((i = ArgPos((char *)"-entitylist", argc, argv)) > 0) entListPath = argv[i + 1];
	if ((i = ArgPos((char *)"-rellist", argc, argv)) > 0) relListPath = argv[i + 1];
	if ((i = ArgPos((char *)"-mainRole", argc, argv)) > 0) mainRoleDataPath = argv[i + 1];
	if ((i = ArgPos((char *)"-trainM", argc, argv)) > 0) trainDataPath = argv[i + 1];
	if ((i = ArgPos((char *)"-testM", argc, argv)) > 0) testDataPath = argv[i + 1];
	if ((i = ArgPos((char *)"-candidateInstance", argc, argv)) > 0) candidateInstancePath = argv[i + 1];
	
	if ((i = ArgPos((char *)"-bias_out", argc, argv)) > 0) bias_out = argv[i + 1];
	if ((i = ArgPos((char *)"-entity_out", argc, argv)) > 0) entity_out = argv[i + 1];
	if ((i = ArgPos((char *)"-normal_out", argc, argv)) > 0) normal_out = argv[i + 1];
	if ((i = ArgPos((char *)"-a_out", argc, argv)) > 0) a_out = argv[i + 1];
	if ((i = ArgPos((char *)"-eta", argc, argv)) > 0) eta = atof(argv[i + 1]);
	
	Evaluator eva = Evaluator(dim, entListPath, relListPath, mainRoleDataPath, testDataPath, trainDataPath, candidateInstancePath, bias_out, entity_out, normal_out, a_out);
	eva.evaluate();
	return 0;
}