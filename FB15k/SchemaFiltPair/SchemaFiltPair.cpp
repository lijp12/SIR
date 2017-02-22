#define ARMA_DONT_USE_CXX11
#include <iostream>
#include <fstream>
#include <armadillo>
#include <time.h>
#include <string>
#include <unordered_map>
#include <set>
#include <vector>
#include <boost/functional/hash.hpp>
#include <boost/random.hpp>
#include <boost/random/linear_congruential.hpp>
#include <boost/random/variate_generator.hpp>
#include <boost/generator_iterator.hpp>
#include <boost/random/uniform_int.hpp>

using namespace std;
using namespace arma;

class Filtor{
	unordered_map <string, int> entities2index;
	unordered_map <int, string> index2entities;
	unordered_map <string, int> type2index;
	unordered_map <int, string> index2type;
	unordered_map <string, int> relation2index;
	unordered_map <int ,string> index2relation;
	unordered_map<int, set<int> > entTypeDic;
	unordered_map<int, uvec> relationSchemaDic;
	vector <int> headList;
	vector <int> tailList;
	char triplet_result_out_path[100];
	char pair_result_out_path[100];
	int ENT_NUM, REL_NUM, TYPENUM;
	
	void load(char *head_entities_list_path, char *tail_entities_list_path, char *type_list_path, char *entity_type_list_path,
	char *relation_schema_list_path, char *triplet_result_path, char *pair_result_path){
		
		strcpy(triplet_result_out_path, triplet_result_path);
		strcpy(pair_result_out_path, pair_result_path);
		FILE *headEntFile, *tailEntFile, *typeFile, *entTypeFile, *relSchemaFile;
		char str[500];
		ENT_NUM = 0, REL_NUM = 0, TYPENUM = 0;
		int n;
		
		tailEntFile = fopen(tail_entities_list_path, "r");
		while (fscanf(tailEntFile, "%s", str) != EOF){
			entities2index[string(str)] = ENT_NUM;
			index2entities[ENT_NUM] = string(str);
			set<int> s;
			s.insert(-1);
			entTypeDic[ENT_NUM] = s;
			tailList.push_back(ENT_NUM);
			ENT_NUM++;
		}
		fclose(tailEntFile);
		cout << "load tailEntFile over" << endl;
		
		headEntFile = fopen(head_entities_list_path, "r");
		while (fscanf(headEntFile, "%s", str) != EOF){
			headList.push_back(entities2index[string(str)]);
		}
		fclose(headEntFile);
		
		typeFile = fopen(type_list_path, "r");
		while (fscanf(typeFile, "%s", str) != EOF){
			type2index[string(str)] = TYPENUM;
			index2type[TYPENUM] = string(str);
			TYPENUM++;
		}
		fclose(typeFile);
		cout << "load headEntFile over" << endl;
		
		entTypeFile = fopen(entity_type_list_path, "r");
		while (fscanf(entTypeFile,"%d\t%s", &n, str) != EOF){
			int entIndex = entities2index[string(str)];
			for(int i= 0; i < n; i++){
				fscanf(entTypeFile, "%s", str);
				entTypeDic[entIndex].insert(type2index[string(str)]);
			}
		}
		fclose(entTypeFile);
		cout << "load entTypeFile over" << endl;
		
		relSchemaFile = fopen(relation_schema_list_path, "r");
		while (fscanf(relSchemaFile, "%s", str) != EOF){
			relation2index[string(str)] = REL_NUM;
			index2relation[REL_NUM] = string(str);
			uvec typeIndices = zeros<uvec>(2);
			for(int i= 0; i < 2; i++){
				fscanf(relSchemaFile, "%s", str);
				typeIndices(i) = type2index[string(str)];
			}
			relationSchemaDic[REL_NUM] = typeIndices;
			REL_NUM++;
		}
		fclose(relSchemaFile);
		cout << "load relSchemaFile over" << endl;
		
		printf("Number of entities: %d, number of relations: %d, number of type: %d\n", ENT_NUM, REL_NUM, TYPENUM);
	}

public:
	Filtor(char *head_entities_list_path, char *tail_entities_list_path, char *type_list_path, char *entity_type_list_path,
	char *relation_schema_list_path, char *triplet_result_path, char *pair_result_path) {
		cout << "enter FILTOR" << endl;
		load(head_entities_list_path, tail_entities_list_path, type_list_path, entity_type_list_path, relation_schema_list_path, triplet_result_path, pair_result_path);
	}
	
	void filt();

};

void Filtor::filt(){
	cout << "enter filt" << endl;
	ofstream tripletResultFile(triplet_result_out_path);
	ofstream pairResultFile(pair_result_out_path);
	for (int i= 0; i < headList.size(); i++){
		int headIndex = headList[i];
		for (int j = 0; j < tailList.size(); j++){
			int tailIndex = tailList[j];
			int flag = 1;
			if (headIndex == tailIndex){
				continue;
			}
			else{
				for (int k = 0; k < REL_NUM; k++){
					uvec typeIndices = relationSchemaDic[k];
					if ((entTypeDic[headIndex].count(typeIndices(0)) > 0) && (entTypeDic[tailIndex].count(typeIndices(1)) > 0)){
						tripletResultFile << index2relation[k] << "\t" << index2entities[headIndex] << "\t" << index2entities[tailIndex] << endl;
						if (flag == 1){
							flag = 0;
							pairResultFile << index2entities[headIndex] << "\t" << index2entities[tailIndex] << endl;
						}
					}
				}
			}
		}
	}
	tripletResultFile.close();
	pairResultFile.close();
}

int main(int argc, char** argv){

	Filtor f = Filtor(argv[1], argv[2], argv[3], argv[4], argv[5], argv[6], argv[7]);
	f.filt();
}
