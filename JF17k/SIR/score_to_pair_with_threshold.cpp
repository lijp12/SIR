#include <iostream>
#include <map>
#include <fstream>
#include <string>
#include <sstream>
#include <algorithm>
#include <cstring>
#include <cmath>
#include <vector>
#include <cstdio>

using namespace std;


int main(int argc, char **argv)
{
    /*
     argv[1] = threshold
     argv[2] = embedding.dim
     argv[3] = interval
     */
    
    double threshold = atof(argv[1]);   

    int entity_num;
    {
        stringstream str_stream;
        str_stream << argv[2];
        str_stream >> entity_num;
    } 
    
    int step = atoi(argv[3]);

    printf("entity_num: %d\ninterval: %d\n", entity_num, step);

    
    stringstream str_stream;
    str_stream << "filtered/connected_pairs" << argv[1] << ".txt";

    ofstream out_file(str_stream.str());
    
    for(int i = 0; i < entity_num; i += step)
    {
        int end = 0;
        if(i + step > entity_num)
            end = entity_num;
        else end = i + step;
        
        stringstream str_stream;
        str_stream << "raw/prediction_" << i << ".txt";
        string path = str_stream.str();
        cout << "parsing file: " << path << endl;
        
        ifstream current_file(path);
        
        for(int head = i; head < end; head++)
        {
            for(int tail = 0; tail < entity_num; tail++)
                if(head != tail)
                {
                    double out0, out1;
                    if(current_file >> out0 >> out1)
                    {
                        if(out1 > threshold)
                            out_file << head << " " << tail << endl;
                    }
                    else
                    {
                        cout << "something is wrong here...\n";
                        exit(0);
                    }
                }
        }
        
        double temp_for_eof_test;
        current_file >> temp_for_eof_test;
        if(current_file)
        {
            cout << "error: additional data remains...\n";
            exit(0);
        }
    }
}


