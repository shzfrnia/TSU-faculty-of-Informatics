// lab6.cpp: определяет точку входа для консольного приложения.
//
#include "stdafx.h"
#include <iostream>
using namespace std;

int main()
{
	int arr[] = { 20, 6, 8, 10, 5 };
	int len = 5;
	int min_of_arr;
	_asm {
				mov		ebx, arr[0]
				mov 	edx, ebx
				mov 	ecx, len
				mov     esi, 0
				jcxz 	L2
		cycl:	
				mov		ebx, arr[esi]
				cmp 	ebx, edx
 				jg		L1
			    mov 	edx, ebx
		L1:		
				add 	esi, 4
				loop	cycl
		L2:		
				mov		min_of_arr, edx
	}

	cout << min_of_arr << endl;
	return 0;
}