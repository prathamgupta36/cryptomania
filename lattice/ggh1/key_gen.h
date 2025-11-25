#pragma once
#include <NTL/ZZ.h>
#include <NTL/vector.h>
#include <NTL/matrix.h>
#include <NTL/mat_ZZ.h>
#include <NTL/mat_RR.h>
#include <NTL/vec_RR.h>
#include <NTL/RR.h>
#include <NTL/LLL.h>
#include <cmath>
#include <iostream>
#include <cstdio>
#include <random>
#include <list>
using namespace std;
using namespace NTL;


Mat<ZZ> GetIdentityMatrix(unsigned int n);

Vec<ZZ> GetRandVec(unsigned int n, unsigned int d);

Mat<ZZ> GetRandVectors(unsigned int amount, unsigned int dimension, unsigned int range);

RR GetHadamardRatio(Mat<ZZ>& matrix);

Mat<ZZ> GetPrivKey(unsigned int dimension, unsigned int range,  float ratio);

Mat<ZZ> GetPublicKey(Mat<ZZ>& Priv_key);

Mat<ZZ> GetBadMatrix(unsigned int n);
