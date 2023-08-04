#pragma warning(disable:4996)
#include<iostream>
#include<bitset>
#include<sstream>
#include <windows.h>
#include<fstream>
#include<intrin.h>
using namespace std;   

int T(int j) 
{
    int T[2] = { 0x7a879d8a ,0x79cc4519 };
    if (j< 0 || j >15)  return T[0];
    else return T[1];
}
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
int P0(int x)
{
    return x ^ LeftShift(x, 9) ^ LeftShift(x, 17);
}
int P1(int x)
{
    return x ^ LeftShift(x, 15) ^ LeftShift(x, 23);
}
int Reverse(int x)      
{
    return (x & 0x000000FFU) << 24 | (x & 0x0000FF00U) << 8 |(x & 0x00FF0000U) >> 8 | (x & 0xFF000000U) >> 24;
}

void CF(int* V, int* BB) {
    int w[68];int h[64];
    for (int i = 16; i < 68; i++)
        w[i] = P1(w[i - 16] ^ w[i - 9] ^ (LeftShift(w[i - 3], 15))) ^ LeftShift(w[i - 13], 7) ^ w[i - 6];
    for (int i = 0; i < 16; i++) w[i] = Reverse(BB[i]);
    for (int i = 0; i < 64; i++) h[i] = w[i] ^ w[i + 4];
    int A = V[0], B = V[1], C = V[2], D = V[3], E = V[4], F = V[5], G = V[6], H = V[7];
    for (int i = 0; i < 64; i++) 
    {
        int SS1 = LeftShift(LeftShift(A, 12) ^ E ^ LeftShift(T(i), i % 32), 7);
        int SS2 = SS1 ^ LeftShift(A, 12);
        int TT1 = FF(A, B, C, i) ^ D ^ SS2 ^ h[i];
        int TT2 = GG(E, F, G, i) ^ H ^ SS1 ^ w[i];
        D = C;
        C = LeftShift(B, 9);
        B = A;
        A = TT1;
        H = G;
        G = LeftShift(F, 19);
        F = E;
        E =P0(TT2);
    }
    V[0] = A ^ V[0];V[1] = B ^ V[1];V[2] = C ^ V[2];V[3] = D ^ V[3];V[4] = E ^ V[4];V[5] = F ^ V[5];V[6] = G ^ V[6];V[7] = H ^ V[7];
}

char* m;
int partition(char p[]) {
    long long length = strlen(p) * 8;
    int pad;
    if ((length) % 512 < 448)
    {                
        pad = (strlen(p) / 64 + 1) * 64;
    }
    else if ((length) % 512 >= 448)
    {
        pad = (strlen(p) / 64 + 2) * 64;
    }
    m = new char[pad];
    m[strlen(p)] = 0x80;
    strcpy(m, p);
    for (int i = strlen(p) + 1; i < pad - 8; i++)
    {
        m[i] = 0;
    }
    for (int j = pad - 8, k= 0; j < pad; k++, j++) 
    {
        m[j] = ((char*)&length)[7 - k];
    }
    return pad / 64;
}

void sm3(char p[])
{
    int hash[8];
    int IV[8] = { 0x7380166f, 0x4914b2b9, 0x172442d7, 0xda8a0600, 0xa96f30bc, 0x163138aa, 0xe38dee4d ,0xb0fb0e4e };
    for (int i = 0; i < 8; i++)
    {
        hash[i] = Reverse(IV[i]);
    }
    int num = partition(p);
    for (int i = 0; i < num; i++)
    {
        int* BB =(int*)&m[i * 64];
        CF(IV,BB);
    }
    memcpy(IV, IV, 64);
}


int main()
{
    DWORD start, end;
    char p[] = "deadline0804";
    start = GetTickCount();
    for (int i = 0; i < 100000; i++) 
    {
        sm3(p);
    }
    end = GetTickCount() - start;
    cout << "未优化SM3加密100000次耗时：" << end <<"ms" << endl;
}
