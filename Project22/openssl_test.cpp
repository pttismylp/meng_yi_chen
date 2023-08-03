#pragma comment(lib,"libssl.lib")
#pragma comment(lib,"libcrypto.lib")
#include <iostream>
#include <string>
#include <sstream>
#include <openssl/rand.h>
#include <openssl/evp.h>
#include <time.h>
using namespace std;

string tohex1(uint8_t* array)
{
	stringstream ss;
	string s2;
	for (int i = 0; i < 32; i++) {
		ss << hex << int(array[i]);
	}
	s2 = ss.str();
	return s2;
}

int tohex2(char r)
{
	stringstream ss1;
	ss1 << r;
	stringstream ss2;
	int d2;
	string str2(ss1.str());
	ss2 << hex << str2;
	ss2 >> d2;
	return d2;
}

int nodehash(uint8_t* array, const void* infm, size_t length) {
	int t = 0;
	const EVP_MD* r = EVP_get_digestbyname("sm3");
	EVP_MD_CTX* s = EVP_MD_CTX_new();
	if (!s)
	{
		EVP_MD_CTX_free(s);
		return t;
	}
	else
	{
		EVP_DigestInit_ex(s, r, NULL);
		EVP_DigestUpdate(s, infm, length);
		t = EVP_DigestFinal_ex(s, array, NULL);
		return t;
	}
}

class Node 
{
public:
	string nodename;
	Node* child[16];
	int value;
	int leaf;
	int dirtyflag;
	int hash;
	time_t timep;
	Node() 
	{
		for (int i = 0; i < 16; i++)
		{
			child[i] = NULL;
		}
		leaf = 0;
		dirtyflag = 0;
		hash = 0;
		time(&timep);
	}
};

class MPT {
public:
	Node root;
	//插入
	void Insert(int value ,string node)
	{
		Node* midst = &root;
		int len = node.length() ;
		uint8_t array[32];
		char* node_ = new char(len+1);
		node_[len+1] = '0';
		for (int i = 0; i < len; i++) 
		{
			node_[i] = node[1];
		}
		int h = nodehash(array, node_, len);
		string ch = tohex1(array);
		int i = 0;
		while (midst->child[tohex2(ch[i])]) 
		{
			if (midst->child[tohex2(ch[i])]->leaf != 0) 
			{
				midst = midst->child[tohex2(ch[i])];
				char mid = midst->nodename[i + 1];
				string midname = midst->nodename;
				int midvalue = midst->value;
				midst->nodename = "";midst->value = 0;midst->leaf = 0;midst->dirtyflag = 0;midst->hash = 0; time(&(midst->timep));
				i++;
				Node* nenode1 = new Node();
				nenode1->value = value; nenode1->nodename = ch; nenode1->leaf = 1; nenode1->dirtyflag = 1; nenode1->hash = h; time(&(nenode1->timep));
				Node* nenode2 = new Node();
				nenode2->value = midvalue;nenode2->nodename = midname;nenode2->leaf = 1;nenode2->dirtyflag = 1; time(&(nenode2->timep));
			}
			i++;
		}
		Node* n = new Node();
		n->value = value;n->nodename = ch;n->leaf = 1;
		midst->child[tohex2(ch[i])] = n;
	}
	//删除
	bool Delete(string node)
	{
		Node* midst = &root;
		uint8_t array[32];
		int len = node.length() + 1;
		char* node_ = new char(len);
		node_[len] = '0';
		for (int i = 0; i < node.length(); i++)
		{
			node_[i] = node[1];
		}
		int h = nodehash(array, node_, node.length());
		string ch = tohex1(array);
		int i = 0;
		while (midst)
		{
			if (midst->leaf == 1)
			{
				midst->nodename = ""; midst->value = 0; midst->leaf = 0; 
				midst->dirtyflag = 1; //脏标志置为true
				midst->hash = 0;//hash标志置空
				time(&(midst->timep));//更新时间
				return true;
			}
			else
			{
				Delete(midst->child[tohex2(ch[i])]->nodename);
			}
		}
		return false;
	}
	//查找
	int Get(string node)
	{
		Node* midst = &root;
		uint8_t array[32];
		int len = node.length();
		char* node_ = new char(len+1);
		node_[len+1] = '0';
		for (int i = 0; i < len; i++) 
		{
			node_[i] = node[1];
		}
		int h = nodehash(array, node_, len);
		string ch = tohex1(array);
		int i = 0;
		while (midst) 
		{
			if (midst->leaf == 1) return midst->value;
			else 
			{
				midst = midst->child[tohex2(ch[i])];
				i++;
			}
		}
	}
	//更新
	bool Update(int value, string node)
	{
		Node* midst = &root;
		uint8_t array[32];
		int len = node.length() + 1;
		char* node_ = new char(len);
		node_[len] = '0';
		for (int i = 0; i < node.length(); i++)
		{
			node_[i] = node[1];
		}
		int h = nodehash(array, node_, node.length());
		string ch = tohex1(array);
		int i = 0;
		while (midst)
		{
			if (midst->value != 0)
			{
				Insert(value, node);
				return true;
			}
			else
			{
				Delete(node);
				return false;
			}
		}
	}

};


int main() {
	MPT tree;
	tree.Insert(23333,"node1");
	tree.Insert(11111,"sbdsaboewf");
	tree.Insert(1111, "adef");
	tree.Insert(111, "tndbg");
	tree.Insert(11, "aetrf");
	cout << tree.Get("node1") << endl << tree.Get("sbdsaboewf") << endl << tree.Get("adef") << endl;
	cout<< tree.Get("tndbg") << endl << tree.Get("aetrf")  <<endl;

}

