#include "stdafx.h"
#include <iostream>

using namespace std;

int main()
{
	setlocale(LC_ALL, "rus");

	int i = 0, K = 0, Q;

	cout << "¬ведите число: " << endl;
	cin >> Q;
	//Q = 5;

	/*for (int i = 0; i*i < Q; i++)
	{
	K++;
	}*/

	_asm
	{
		mov edx, 0
		mov ecx, 0
		cycl:
				mov eax, ecx
				mov ebx, ecx
				mul ebx
				cmp eax, Q
				jg cycl_end
				inc K
				inc ecx
				jmp cycl
		cycl_end:

	}
	cout << K << endl;

	return 0;
}