#include <iostream>
#include <fstream>
#include <time.h>
#include <string>
#include <unordered_map>
#include <set>

using namespace std;

class Filtor{
	unordered_map <string, int> entities2index;
	unordered_map <int, string> index2entities;
	set <string> NNconnective;
	int ENT_NUM;
	void load(char *entity_list_path, char *schemaFiltPair_path, char *NN_connective_path, char *result_path){
		
		ofstream ResultFile(result_path);
		FILE *entFile, *schemaPairFile, *NNConnectiveFile;
		char str[500];
		char relation[500], head[500], tail[500];
		
		int headIndex, tailIndex;
		ENT_NUM = 0;
		entFile = fopen(entity_list_path, "r");
		while (fscanf(entFile, "%s", str) != EOF){
			entities2index[string(str)] = ENT_NUM;
			index2entities[ENT_NUM] = string(str);
			ENT_NUM++;
		}
		fclose(entFile);
		
		NNConnectiveFile = fopen(NN_connective_path, "r");
		while (fscanf(NNConnectiveFile, "%d %d", &headIndex, &tailIndex) != EOF){
			NNconnective.insert(index2entities[headIndex] + "\t" + index2entities[tailIndex]);
		}
		fclose(NNConnectiveFile);
		
		schemaPairFile = fopen(schemaFiltPair_path, "r");
		while (fscanf(schemaPairFile,"%s\t%s\t%s", relation, head, tail) != EOF){
			if (NNconnective.count(string(head) + "\t" + string(tail)) > 0){
				ResultFile << string(relation) << "\t" << string(head) << "\t" << string(tail) << endl;
			}
		}
		fclose(schemaPairFile);
	}
		
public:
	Filtor(char *entity_list_path, char *schemaFiltPair_path, char *NN_connective_path, char *result_path) {
		load(entity_list_path, schemaFiltPair_path, NN_connective_path, result_path);
	}
	
};

int main(int argc, char** argv){

	Filtor f = Filtor(argv[1], argv[2], argv[3],argv[4]);
}
