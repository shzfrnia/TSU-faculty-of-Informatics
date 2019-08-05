// lab6.cpp: определяет точку входа для консольного приложения.
//
#include "stdafx.h"
#include <iostream>
using namespace std;

int main()
{
	int arr[] = { -20, 500, 8, 100, 5 };
	int len = 5;
	int min_of_arr;
	int index_min = 0;
	_asm {
					mov		ebx, arr[0]
					mov		edx, ebx
					mov		esi, 0
					mov		ecx, 0
		cycl:		cmp		ecx, len
					je		cycl_out
					mov		ebx, arr[esi]
					cmp		ebx, edx
					jg		cont
					mov		edx, ebx
					mov		index_min, ecx
		cont:
					add		esi, 4
					inc		ecx
					jmp		cycl
		cycl_out:
					mov		min_of_arr, edx
	}

	cout << "Array[" << index_min << "] = "  << min_of_arr << endl;
	return 0;
}