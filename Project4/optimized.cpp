#pragma warning(disable:4996)
#include<iostream>
#include<bitset>
#include<sstream>
#include <windows.h>
#include<fstream>
#include<intrin.h>
using namespace std;

int LeftShift(int x, int n)
{
    return (x << n) | ((unsigned int)x >> (32 - n));
}
int FF(int x, int y, int z, int j) {
    if (j >= 0 && j <= 15) return (x ^ y ^ z);
    else  return (x & y) | (x & z) | (y & z);
}
int GG(int x, int y, int z, int j) {
    if (j >= 0 && j <= 15) return x ^ y ^ z;
    else  return (x & y) | ((~x) & z);
}

int Reverse(int x)
{
    return (x & 0x000000FFU) << 24 | (x & 0x0000FF00U) << 8 | (x & 0x00FF0000U) >> 8 | (x & 0xFF000000U) >> 24;
}

__m128i tranleft(__m128i x, int n)
{
    __m128i num = _mm_set_epi32(0xFFFFFFFF, 0xFFFFFFFF, 0xFFFFFFFF, 0xFFFFFFFF);  
    __m128i y = _mm_or_si128(_mm_and_si128(num, _mm_slli_epi32(x, n % 32)), _mm_srli_epi32(_mm_and_si128(num, x), 32 - n % 32));
    return y;
}
__m128i P1(__m128i x)
{
    __m128i y = _mm_xor_si128(_mm_xor_si128(x, tranleft(x, 15)), tranleft(x, 23));
    return y;
}

void CF(int* V, int* BB) 
{
    int w[68];int h[64];
    __m128i v12, v6, v9, v3, v0, s;
    for (int i = 0; i < 16; i++) w[i] = Reverse(BB[i]);
    for (int k = 4; k < 17; k++)
    {
        int x = w[k * 4 - 16] ^ w[k * 4 - 9] ^ (LeftShift(w[k * 4 - 3], 15));
        w[k * 4] = (x ^ LeftShift(x, 15) ^ LeftShift(x, 23)) ^ LeftShift(w[4 * k - 13], 7) ^ w[4 * k - 6];
        v0 = _mm_setr_epi32(w[4 * k - 3], w[4 * k - 2], w[4 * k - 1], w[4 * k]);
        v3 = _mm_setr_epi32(w[4 * k - 6], w[4 * k - 5], w[4 * k - 4], w[4 * k - 3]);
        v6 = _mm_setr_epi32(w[4 * k - 9], w[4 * k - 8], w[4 * k - 7], w[4 * k - 6]);
        v9 = _mm_setr_epi32(w[4 * k - 13], w[4 * k - 12], w[4 * k - 11], w[4 * k - 10]);
        v12 = _mm_setr_epi32(w[4 * k - 16], w[4 * k - 15], w[4 * k - 14], w[4 * k - 13]);
        s = _mm_xor_si128(P1(_mm_xor_si128(tranleft(v9, 7), v3)), _mm_xor_si128(_mm_xor_si128(v12,v6), tranleft(v0, 15)));
        memcpy(&w[k * 4], (int*)&s, 16);        
    }
    for (int i = 0; i < 64; i++)  h[i] = w[i] ^ w[i + 4];
    int A = V[0], B = V[1], C = V[2], D = V[3], E = V[4], F = V[5], G = V[6], H = V[7];
    for (int i = 0; i < 64; i++) {
        int T[2] = { 0x7a879d8a ,0x79cc4519 };
        int t;
        if (i < 0 || i >15)t = T[0];
        else t=T[1];
        int SS1 = LeftShift(LeftShift(A, 12) ^ E ^ LeftShift(t, i % 32), 7);
        int SS2 = SS1 ^ LeftShift(A, 12);
        int TT1 = FF(A, B, C, i) ^ D ^ SS2 ^h[i];
        int TT2 = GG(E, F, G, i) ^ H ^ SS1 ^ w[i];
        D = C;
        C = LeftShift(B, 9);
        B = A;
        A = TT1;
        H = G;
        G = LeftShift(F, 19);
        F = E;
        E = TT2^ LeftShift(TT2, 9) ^ LeftShift(TT2, 17);

    }
    V[0] = A ^ V[0]; V[1] = B ^ V[1]; V[2] = C ^ V[2]; V[3] = D ^ V[3]; V[4] = E ^ V[4]; V[5] = F ^ V[5]; V[6] = G ^ V[6]; V[7] = H ^ V[7];
}

char* m;
int partition(char p[])
{
    long long length = strlen(p) * 8;
    int pad;
    if ((length) % 512 < 448) pad = (strlen(p) / 64 + 1) * 64;
    else if ((length) % 512 >= 448)
        pad = (strlen(p) / 64 + 2) * 64;
    m = new char[pad];
    m[strlen(p)] = 0x80;
    strcpy(m, p);
    for (int i = strlen(p) + 1; i < pad - 8; i++)
        m[i] = 0;
    for (int j = pad - 8, k = 0; j < pad; k++, j++)
        m[j] = ((char*)&length)[7 - k];
    return pad / 64;
}

void sm3_simd(char p[]) 
{
    int hash[8];
    int IV[8] = { 0x7380166f, 0x4914b2b9, 0x172442d7, 0xda8a0600, 0xa96f30bc, 0x163138aa, 0xe38dee4d ,0xb0fb0e4e };
    for (int i = 0; i < 8; i++) 
        hash[i] = Reverse(IV[i]);
    int num = partition(p);
    for (int i = 0; i < num; i++)
    {
        int* BB = (int*)&m[i * 64];
        CF(IV,BB);
    }
    memcpy(IV, IV, 64);
}

int main() 
{
    DWORD start, end;
    char p[] = "deadline0804";
    start = GetTickCount();
    for (int i = 0; i < 100000; i++) {
        sm3_simd(p);
    }
    end = GetTickCount() - start;
    cout << "已优化SM3加密100000次耗时：" << end << "ms" << endl;
}