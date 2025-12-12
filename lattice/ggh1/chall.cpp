#include "key_gen.h"
#include "GGH_cryptosystem.h"
#include <iomanip>
#include <fstream>
#include <sstream>
#include <bits/stdc++.h>

void WriteMatrixCSV(Mat<ZZ>& M, const string& path){
    ofstream out(path);
    if(!out) return;
    long n = M.NumRows(), m = M.NumCols();
    for(long i = 0; i < n; i++){
        for(long j = 0; j < m; j++){
            out << M[i][j];
            if(j < m - 1) out << ",";
        }
        out << "\n";
    }
    out.close();
}

void WriteVectorCSV(Vec<ZZ>& v, const string& path){
    ofstream out(path);
    if(!out) return;
    long n = v.length();
    for(long i = 0; i < n; i++){
        out << v[i];
        if(i < n - 1) out << ",";
    }
    out << "\n";
    out.close();
}

Vec<ZZ> ReadVectorStdinCSV(long expect=-1){
    Vec<ZZ> v;
    string line;
    if(!getline(cin, line)) return v;
    for(char& c: line) if(c==',') c=' ';
    stringstream ss(line);
    vector<ZZ> tmp; ZZ x;
    string tok;
    while(ss >> tok){ conv(x, tok.c_str()); tmp.push_back(x); }
    v.SetLength((long)tmp.size());
    for(long i=0;i<v.length();i++) v[i]=tmp[i];
    if(expect>=0 && v.length()!=expect) v.SetLength(0);
    return v;
}

int chall(){

	unsigned int lattice_dimension 	= 20; //Should be large enough
	unsigned int coefficient_range 	= 1000;
	float desired_ratio		= 0.70;
	
	Mat<ZZ> Priv_key;
	Mat<ZZ> Public_key;

	Vec<ZZ> pt;
	Vec<ZZ> ct;
	
	Priv_key.SetDims(lattice_dimension, lattice_dimension); // sqaures are so much easier to work with :p

	Priv_key   = GetPrivKey(lattice_dimension, coefficient_range, desired_ratio);
	
	Public_key = GetPublicKey(Priv_key);

	pt = GetRandVec(Public_key.NumCols(), 100);
	ct = EncryptGGH(Public_key, pt, 5);

	WriteMatrixCSV(Public_key, "/challenge/public_key.csv");
	WriteVectorCSV(ct, "/challenge/cipher_text.csv");

	printf("Wrote Public key to public_key.csv\n");
	printf("Wrote Cipher Text to cipher_text.csv\n\n");
	
	printf("Can you guess the random vector?\n");
	Vec<ZZ> user_vec = ReadVectorStdinCSV(pt.length());

	if(user_vec == pt){
		printf("Amazing!!!\n");
		printf("Here is a flag for your troubles:\n");
		ifstream f("/flag", ios::in | ios::binary);
		if (!f) { perror("open /flag"); return 1; }
		cout << f.rdbuf();
	}
	else{
		printf("\nno... ˙◠˙\n");
	}

	return 0;
}



int main(){

	printf("\n\nThis challenge is a *crude* implementation of the GGH Public Key Cryptosystem.\n");
	printf("Its gotta be secure enough right?\n\n");
	chall();
	return 0;
}

