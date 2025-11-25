#include "GGH_cryptosystem.h"

static inline RR DotRow(const Vec<RR>& a, const Vec<RR>& b){
	long n=a.length(); RR s=to_RR(0);
	for(long i=0;i<n;i++) s+=a[i]*b[i];
	return s;
}

static inline ZZ RoundRR(const RR& x){
	RR h=to_RR(0.5);
	return (x>=0? to_ZZ(floor(x+h)) : to_ZZ(ceil(x-h)));
}

static void GramSchmidtRows(const Mat<RR>& B, Mat<RR>& Bstar, Mat<RR>& mu, Vec<RR>& norm2){
	long n=B.NumRows(), m=B.NumCols();
	Bstar.SetDims(n,m); mu.SetDims(n,n); norm2.SetLength(n);
	for(long i=0;i<n;i++){
		Bstar[i]=B[i];
		for(long j=0;j<i;j++){
			mu[i][j]=DotRow(B[i],Bstar[j])/norm2[j];
			for(long k=0;k<m;k++) Bstar[i][k]-=mu[i][j]*Bstar[j][k];
		}
		norm2[i]=DotRow(Bstar[i],Bstar[i]);
	}
}

static Vec<ZZ> BabaiRows(const Mat<ZZ>& Bz, const Vec<ZZ>& e){
	Mat<RR> B; conv(B,Bz);
	Vec<RR> y; conv(y,e);
	long n=B.NumRows(), m=B.NumCols();
	Mat<RR> Bstar, mu; Vec<RR> n2;
	GramSchmidtRows(B,Bstar,mu,n2);
	Vec<ZZ> a; a.SetLength(n);
	for(long i=n-1;i>=0;i--){
		RR c=DotRow(y,Bstar[i])/n2[i];
		a[i]=RoundRR(c);
		for(long k=0;k<m;k++) y[k]-=to_RR(a[i])*B[i][k];
	}
	Vec<ZZ> v=a*Bz;
	return v;
}

Vec<ZZ> EncryptGGH(Mat<ZZ> Public_key, Vec<ZZ> plain_text, unsigned int delta){
	Vec<ZZ> cipher_text;
	Vec<ZZ> ephemeral_key;
	ZZ 	dim;

	dim = conv<int>(Public_key.NumCols());

	ephemeral_key = GetRandVec(conv<int>(dim), delta);
	
	cipher_text = (plain_text * Public_key) + ephemeral_key;

	return cipher_text;
	
}

Vec<ZZ> DecryptGGH(Mat<ZZ> Priv_key, Mat<ZZ> Public_key, Vec<ZZ> cipher_text){
	Vec<ZZ> v=BabaiRows(Priv_key,cipher_text);
	Mat<RR> W; 
	conv(W,Public_key);
	Mat<RR> Winv; 
	inv(Winv,W);
	Vec<RR> vr; 
	conv(vr,v);
	Vec<RR> mr=vr*Winv;
	Vec<ZZ> m; 
	m.SetLength(mr.length());
	for(long i=0;i<m.length();i++) m[i]=RoundRR(mr[i]);
	return m;
}
