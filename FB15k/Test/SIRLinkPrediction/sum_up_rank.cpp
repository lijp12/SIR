#include <iostream>
#include <cstdio>
using namespace std;

void sumup(string path){
    FILE* fin = fopen(path.c_str(),"r");
    float rank=0, hit=0, size=0;
    float split_rank, split_hit, split_size;
    while (fscanf(fin,"%f",&split_size)==1)
    {
        fscanf(fin,"%f %f", &split_hit, &split_rank);
        size += split_size;
        rank += split_size * split_rank;
        hit += split_size * split_hit;
    }
    rank /= size;
    hit /= size;
    cout << "hit: " << hit << endl;
    cout << "rank: " << rank << endl; 
}

int main(int argc,char**argv)
{
    string path = argv[1];
    sumup(path);
}

