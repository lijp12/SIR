#define ARMA_DONT_USE_CXX11
#include <iostream>
#include <armadillo>
#include <vector>
#include <unordered_map>
#include <unordered_set>
#include <time.h>
#include <fstream>
#include <sstream>
#include <iomanip>
#include <string>
#include <boost/functional/hash.hpp>
#include <boost/random.hpp>
#include <boost/random/linear_congruential.hpp>
#include <boost/random/variate_generator.hpp>
#include <boost/generator_iterator.hpp>
#include <boost/random/uniform_int.hpp>
using namespace std;
using namespace arma;

float eta;

typedef boost::minstd_rand  generator_type;

size_t uvecHash(const uvec &v){
	return boost::hash_range(v.begin(), v.end());
}
bool eqOp(const uvec &lhs, const uvec &rhs){
	return all((lhs == rhs) == 1);
}
class MFoldEmbedding{
	int DIM, REL_NUM, ENT_NUM, BATCH_SIZE, TRAIN_NUM;
	int is_first;
	double alpha, epsilon, gamma, beta;
	vector <int> schema;
	//pair<int, uvec> *trainData;
	vector<pair<int, uvec> > trainData;

	using uvec_set = unordered_set <uvec, decltype(uvecHash)*, decltype(eqOp)* >;
	unordered_map<int, uvec_set> positive;
	//vec *A;
	vector<vec> A, At;
	mat BR, NR, ENT;
	mat Bt, Nt, Et;
	
	char *bias_out, *entity_out, *normal_out, *a_out;


	mat project(const mat &_X, const vec &nr){
		return _X - nr * nr.t() * _X;
	}
	double scoreFn(const mat &Xr, const vec &ar, const vec &br){
		return norm(Xr * ar + br, 2);
	}

	void save(char * out, mat &M){
		FILE *file;
		file = fopen(out, "w");
		for (int i = 0; i < M.n_cols; i++){
			for (int j = 0; j < M.n_rows; j++)
				fprintf(file, "%f\t", M(j, i));
			fprintf(file, "\n");
		}
		fflush(file);
		fclose(file);
	}
public:
	MFoldEmbedding(vector <int> &_schema, vector<pair<int, uvec> > &_trainData,
		int trainNum, int dim, int relNum, int entNum, int batchSize,
		double learning_rate, double _epsilon, double margin_gamma, double _beta, int flag,
		char *_bias_out, char *_entity_out, char *_normal_out, char *_a_out)
		:bias_out(_bias_out), entity_out(_entity_out), normal_out(_normal_out), a_out(_a_out),
		alpha(learning_rate), epsilon(_epsilon), gamma(margin_gamma), beta(_beta){
		is_first = flag;
		DIM = dim;
		REL_NUM = relNum;
		ENT_NUM = entNum;
		BATCH_SIZE = batchSize;
		TRAIN_NUM = trainNum;
		schema = _schema;
		trainData = _trainData;

		if (is_first == 0){
			A = vector <vec>(REL_NUM);
			for (int i = 0; i < REL_NUM; i++) {
				//A[i] = randu<vec>(schema[i]);
				int one_size = schema[i];
				A[i] = (randu<vec>(one_size));
				
			}
			BR = normalise(randu<mat>(DIM, REL_NUM));
			NR = normalise(randu<mat>(DIM, REL_NUM));
			ENT = normalise(randu<mat>(DIM, ENT_NUM));
		}
		else{
			BR.load(bias_out);
			NR.load(normal_out);
			
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
			
			ENT = zeros<mat>(DIM, ENT_NUM);
			ifstream in(entity_out);

			for(int i = 0; i < ENT.n_cols; i++)
			{
				for(int j = 0; j < ENT.n_rows; j++)
					in >> ENT(j, i);			
			}
		}
		
		Nt = NR;
		Bt = BR;
		Et = ENT;
		At = A;
		//ENT = randu<mat>(DIM, ENT_NUM);
		//cout <<"length "<< dot(ENT.col(0), ENT.col(0)) << endl;
		for (int i = 0; i < TRAIN_NUM; i++){
			int rel = trainData[i].first;
			uvec indices = trainData[i].second;
			if (positive.count(rel) == 0){
				positive[rel] = uvec_set(500, uvecHash, eqOp);
			}
			positive[rel].insert(indices);
		}
	}
	~MFoldEmbedding(){
		//delete[] A;
	}
	void saveEmbeddingArma(char *bias_out, char *entity_out, char *normal_out, char *a_out){
		
		ofstream out(entity_out);
		out << fixed << showpoint;
		out << setprecision(15);
    
		for(int i = 0; i < ENT.n_cols; i++)
		{
			for(int j = 0; j < ENT.n_rows; j++)
				out << ENT(j, i) << " ";
			out << endl;
		}

		string path1(entity_out);
        string path2 = to_string(is_first);
        path1 += path2;

		ofstream out_backup(path1);
        out_backup << fixed << showpoint;
        out_backup << setprecision(15);
        
        for(int i = 0; i < ENT.n_cols; i++)
        {
            for(int j = 0; j < ENT.n_rows; j++)
                out_backup << ENT(j, i) << " ";
            out_backup << endl;
        }
		
		BR.save(bias_out);
		NR.save(normal_out);
		FILE * file = fopen(a_out, "w");
		for (int i = 0; i < REL_NUM; i++){
			for (int j = 0; j < A[i].n_elem; j++){
				fprintf(file, "%f\t", A[i](j));
			}
			fprintf(file, "\n");
		}
		fflush(file);
		fclose(file);

	}
	void saveEmbedding(char *bias_out, char *entity_out, char *normal_out, char *a_out){
		save(entity_out, ENT);
		save(bias_out, BR);
		save(normal_out, NR);
		FILE * file = fopen(a_out, "w");
		for (int i = 0; i < REL_NUM; i++){
			for (int j = 0; j < A[i].n_elem; j++){
				fprintf(file, "%f\t", A[i](j));
			}
			fprintf(file, "\n");
		}
		fflush(file);
		fclose(file);
	}

	double updateGradient(int rel, uvec &posIndices, uvec &negIndices){
		mat Xp = ENT.cols(posIndices);
		mat Xn = ENT.cols(negIndices);
	
		vec ar = A[rel];
		vec br = BR.col(rel);
		vec nr = NR.col(rel);
		mat Xp_r = project(Xp, nr);
		mat Xn_r = project(Xn, nr);
		vec posTmp = Xp_r * ar + br;
		double posLoss = dot(posTmp, posTmp);
		vec negTmp = Xn_r * ar + br;
		double negLoss = dot(negTmp, negTmp);
		if (negLoss - posLoss >= gamma) return 0;

		// compute gradient of relation plane bias vector
		Bt.col(rel) = normalise(Bt.col(rel) -  2 * alpha * (posTmp - negTmp));
		
		// compute gradient of relation plane normal vector
		vec gn = (-2 * dot(posTmp, nr) * Xp * ar - 2 * posTmp * nr.t() * Xp * ar);
		gn -= (-2 * dot(negTmp, nr) * Xn * ar - 2 * negTmp * nr.t() * Xn * ar);
		Nt.col(rel) = normalise(Nt.col(rel) - alpha * gn);
		

		// compute gradient of relation weight vector
		vec ga = 2 * Xp_r.t() * posTmp;
		ga -= 2 * Xn_r.t() * negTmp;
		At[rel] =normalise((At[rel] - alpha*ga));

		// compute gradient of entity vectors
		int len = posIndices.n_rows;
		for (int l = 0; l < len; l++){
			vec gp = 2 * ar(l) * (eye<mat>(DIM, DIM) - nr * nr.t()) * posTmp;
			Et.col(posIndices[l]) -= alpha * gp;
			vec gn = 2 * ar(l) * (eye<mat>(DIM, DIM) - nr * nr.t()) * negTmp;
			Et.col(negIndices[l]) += alpha * gn;
		}
		/*
		for (int l = 0; l < len; l++){
			Et.col(posIndices[l]) = normalise(Et.col(posIndices[l]));
			Et.col(negIndices[l]) = normalise(Et.col(negIndices[l]));
		}
		*/
		return - negLoss +  posLoss + gamma;
	}

	double orthConstraint(int rel_index){
		double penalty = 0.0;
		vec nr = NR.col(rel_index);
		vec br = BR.col(rel_index);
		vec ar = A[(rel_index)];
		double d = dot(nr, br);
		int r_size = schema[rel_index];
		vec all_one = ones<vec>(r_size);
		int dar = dot(ar, all_one);
		At[rel_index] = normalise(At[rel_index] - 2*alpha * all_one * eta  * dar);
		if (d * d > epsilon) {
			Bt.col(rel_index) = normalise(Bt.col(rel_index) - 2 * alpha * beta * d * nr);
			Nt.col(rel_index) = normalise(Nt.col(rel_index) - 2 * alpha * beta * d * br);
			penalty += beta * (d * d - epsilon);
		}
		return penalty;
	}
	void updateEmbedding(){
		ENT = Et;
		NR = Nt;
		BR = Bt;
		A = At;
	}
	uvec negativeSampling(int rel, uvec pos, boost::minstd_rand rng){
		uvec neg = pos;
		boost::random::uniform_int_distribution<> pick_entity(0, ENT_NUM - 1);
		//boost::random::uniform_int_distribution<> pick_dim(0, neg.n_cols-1);

		neg(rand() % neg.n_rows) = pick_entity(rng);
		while (positive[rel].count(neg) > 0)
			neg(rand() % neg.n_rows) = pick_entity(rng);
		return neg;
	}
	void train(int num_epoch){
		boost::uniform_int<> uni_dist(0, TRAIN_NUM - 1);
		generator_type generator(time(0));
		boost::variate_generator<generator_type&, boost::uniform_int<> > pick_data(generator, uni_dist);

		double loss = 0;
		int num_batch = TRAIN_NUM / BATCH_SIZE + (TRAIN_NUM % BATCH_SIZE ? 1 : 0);
		for (int epoch_index = 1; epoch_index <= num_epoch; epoch_index++){
			printf("# %d epoch, loss = %f\n", epoch_index, loss);
			fflush(stdout);
			//saveEmbedding(bias_out, entity_out, normal_out, a_out);
			saveEmbeddingArma(bias_out, entity_out, normal_out, a_out);

			loss = 0;
			int total_train = 0;
			for (int batch_index = 0; batch_index < num_batch; batch_index++){
				for (int i = 0; i < BATCH_SIZE; i++){
					int k = pick_data();
					int rel = trainData[k].first;
					uvec posIndices = trainData[k].second;
					for(int n_num = 0; n_num < posIndices.n_rows; n_num++){
						uvec negIndices = negativeSampling(rel, posIndices, generator);
						loss += updateGradient(rel, posIndices, negIndices);
						loss += orthConstraint(rel);
					}
					total_train++;
				}

				updateEmbedding();
			}
			//cout << "Total sample is:\t" << total_train << endl;
		}
		saveEmbeddingArma(bias_out, entity_out, normal_out, a_out);
		//saveEmbedding(bias_out, entity_out, normal_out, a_out);
	}
};
class DataMgr{

public:
	unordered_map <string, int> entities2index;
	unordered_map <string, int> relation2index;
	vector<int> schema;
	vector<pair<int, uvec>> trainData;
	int ENT_NUM, REL_NUM;
	DataMgr(char *entities_list_path, char *relation_list_path, char *training_data_path){
		FILE *entFile, *relFile, *trainFile;
		char str[500];
		ENT_NUM = 0, REL_NUM = 0;
		int n;
		entFile = fopen(entities_list_path, "r");
		while (fscanf(entFile, "%s", str) != EOF){
			entities2index[string(str)] = ENT_NUM;
			ENT_NUM++;
		}
		fclose(entFile);

		schema.clear();
		relFile = fopen(relation_list_path, "r");
		while (fscanf(relFile, "%s\t%d", str, &n) != EOF){
			schema.push_back(n == 0 ? 2 : n);
			relation2index[string(str)] = REL_NUM;
			REL_NUM++;
		}
		fclose(relFile);

		trainFile = fopen(training_data_path, "r");
		while (fscanf(trainFile, "%s", str) != EOF){
			int index = relation2index[string(str)];
			int cnt = schema[index];
			uvec ent_indices = zeros<uvec>(cnt);
			for (int i = 0; i < cnt; i++){
				fscanf(trainFile, "%s", str);
				ent_indices(i) = entities2index[string(str)];
			}
			trainData.push_back(pair<int, uvec>(index, ent_indices));
		}
		fclose(trainFile);
		printf("Number of entities: %d, number of relations: %d, number of training data: %d\n", ENT_NUM, REL_NUM, trainData.size());
		fflush(stdout);
	}
};
int ArgPos(char *str, int argc, char **argv) {
	int a;
	for (a = 1; a < argc; a++) if (!strcmp(str, argv[a])) {
		if (a == argc - 1) {
			printf("Argument missing for %s\n", str);
			fflush(stdout);
			exit(1);
		}
		return a;
	}
	return -1;
}
int main(int argc, char** argv)
{
	int i, dim, num_epoch, batch_size, flag;
	double learning_rate, margin_gamma, epsilon, beta;


	char *entities_list_path, *relation_list_path, *training_data_path, schema_path;
	char *bias_out, *entity_out, *normal_out, *a_out, *split_list;
	if ((i = ArgPos((char *)"-dim", argc, argv)) > 0) dim = atoi(argv[i + 1]);
	if ((i = ArgPos((char *)"-epoch", argc, argv)) > 0) num_epoch = atoi(argv[i + 1]);
	if ((i = ArgPos((char *)"-batch", argc, argv)) > 0) batch_size = atoi(argv[i + 1]);
	if ((i = ArgPos((char *)"-lr", argc, argv)) > 0) learning_rate = atof(argv[i + 1]);
	if ((i = ArgPos((char *)"-margin", argc, argv)) > 0) margin_gamma = atof(argv[i + 1]);
	if ((i = ArgPos((char *)"-epsilon", argc, argv)) > 0) epsilon = atof(argv[i + 1]);
	if ((i = ArgPos((char *)"-beta", argc, argv)) > 0) beta = atof(argv[i + 1]);
	if ((i = ArgPos((char *)"-flag", argc, argv)) > 0) flag = atoi(argv[i + 1]);
	
	if ((i = ArgPos((char *)"-entity", argc, argv)) > 0) entities_list_path = argv[i + 1];
	if ((i = ArgPos((char *)"-rel", argc, argv)) > 0) relation_list_path = argv[i + 1];
	if ((i = ArgPos((char *)"-train", argc, argv)) > 0) training_data_path = argv[i + 1];

	if ((i = ArgPos((char *)"-bias_out", argc, argv)) > 0) bias_out = argv[i + 1];
	if ((i = ArgPos((char *)"-entity_out", argc, argv)) > 0) entity_out = argv[i + 1];
	if ((i = ArgPos((char *)"-normal_out", argc, argv)) > 0) normal_out = argv[i + 1];
	if ((i = ArgPos((char *)"-a_out", argc, argv)) > 0) a_out = argv[i + 1];
	if ((i = ArgPos((char *)"-eta", argc, argv)) > 0) eta = atof(argv[i + 1]);
	
	printf("dim = %d num_epoch = %d batch= %d lr = %f margin = %f epsilon = %f beta = %f\n",
		dim, num_epoch, batch_size, learning_rate, margin_gamma, epsilon, beta);
	fflush(stdout);
	DataMgr dm = DataMgr(entities_list_path, relation_list_path, training_data_path);
	MFoldEmbedding model = MFoldEmbedding(dm.schema, dm.trainData,
		dm.trainData.size(), dim, dm.REL_NUM, dm.ENT_NUM, batch_size,
		learning_rate, epsilon, margin_gamma, beta, flag,
		bias_out, entity_out, normal_out, a_out);
	model.train(num_epoch);

	//model.saveEmbedding(bias_out, entity_out, normal_out, a_out);
	return 0;
}
