#pragma once
#include "key_gen.h"

Vec <ZZ> EncryptGGH(Mat<ZZ> Public_key, Vec<ZZ> plain_text, unsigned int delta);
Vec <ZZ> DecryptGGH(Mat<ZZ> Priv_key, Mat<ZZ> Public_key, Vec<ZZ> cipher_text);

