#include "key_gen.h"

random_device rand_dev;
mt19937       generator(rand_dev());

Mat<ZZ> GetIdentityMatrix(unsigned int n){
	
	Mat<ZZ> I_M;

	I_M.SetDims(n, n);

	for(int i=0; i < n; i++){
		I_M[i][i] = ZZ(1);
	}
	
	return I_M;
}

Vec<ZZ> GetAllOnesVec(unsigned int n){
	
	Vec<ZZ> v;
	v.SetLength(n);
	
	for(int i = 0; i < n; i++){
		v[i] = ZZ(1);
	}
	
	return v;
}

list<ZZ> GetRandValueByRange(unsigned int n, unsigned int d){

	list<ZZ> values;
	uniform_int_distribution<int> distr(-d, d);
	ZZ val;

	for (int i = 0; i < n; i++){
		val = ZZ(distr(generator)); 
		values.push_back(val);
	}

	return values;
}

Vec<ZZ> GetRandVec(unsigned int n, unsigned int d){	
	
	Vec<ZZ>  random_vec    = GetAllOnesVec(n);
	list<ZZ> random_values = GetRandValueByRange(n, d);
	
	int i = 0;
	for (ZZ val : random_values){
		random_vec[i] *= val;
		i++;
	}
	
	return random_vec;
}

Mat<ZZ> GetRandVectors(unsigned int amount, unsigned int dimension, unsigned int range){
	
	Mat<ZZ> rand_matrix;
	Vec<ZZ> rand_vec;

	rand_matrix.SetDims(amount, dimension);
	

	for(int i = 0; i < amount; i++){
		rand_vec = GetRandVec(dimension, range);
		rand_matrix[i] = rand_vec;
	}

	return rand_matrix;
}

RR GetVecNorm(Vec<ZZ>& vec){
 	
	RR sum = to_RR(0);
	RR norm;

	for(ZZ coord : vec){
		RR coordinate = conv<RR>(coord);
		sum += coordinate * coordinate;
	}	
	
	norm = sqrt(sum);
	return norm;
}

RR GetHadamardRatio(Mat<ZZ>& matrix){
	
	RR ratio;
	RR temp;
	RR n;
	RR det = conv<RR>(determinant(matrix));
	RR prod = to_RR(1);
	unsigned int dim = matrix.NumCols();

	for (int i=0; i < dim; i++){
		prod *= GetVecNorm(matrix[i]);
	}
	
	temp = abs(det/prod);
	n = to_RR(1)/to_RR(dim);
	
	ratio = pow(temp, n);
	return ratio;
}

Mat<ZZ> GetBadMatrix(unsigned int n){
	Mat<ZZ> bad; 
	bad = GetIdentityMatrix(n);
	uniform_int_distribution<int> op(0, 2);
	uniform_int_distribution<int> idx(0, n - 1);
	uniform_int_distribution<int> factor(-17, 17);

	for(int t = 0; t < 20 * n; t++){
	
	int c = op(generator);
	int i = idx(generator);
	int j = idx(generator);
	
	if(i == j) continue;
	
	if(c == 0){
	    for(int k = 0; k < (int)n; k++) swap(bad[i][k], bad[j][k]);
	}

	else if(c == 1){
	    for(int k = 0; k < (int)n; k++) bad[i][k] = -bad[i][k];
		
	}	 

	else {
	    int kf = factor(generator);
	    if(kf == 0) continue;
	    for(int k = 0; k < (int)n; k++) bad[i][k] += bad[j][k] * kf;
	}

	}

	ZZ d = determinant(bad);
	if(!(d == 1 || d == -1)) return GetBadMatrix(n);

	return bad;
}

Mat<ZZ> GetPrivKey(unsigned int dimension, unsigned int range,  float ratio){
	
	Mat<ZZ> random_M;
	RR computed_ratio;
	RR pre_lll_ratio;
	float improv;

	random_M.SetDims(dimension, dimension);
	
	while (computed_ratio < ratio){
		random_M =  GetRandVectors(dimension, dimension, range);
		//BKZ_FP(random_M, 0.99, 30); // Sadly i must reduce if I want a higher ratio
		computed_ratio = GetHadamardRatio(random_M);
	}

	return random_M;	
}

Mat<ZZ> GetPublicKey(Mat<ZZ>& Priv_key){
	
	Mat<ZZ> Public_key;
	Mat<ZZ> M;
	unsigned int dimension = Priv_key.NumCols(); 
	
	M = GetBadMatrix(dimension);
	mul(Public_key, M, Priv_key); 

	return Public_key;
}

