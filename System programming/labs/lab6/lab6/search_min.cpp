// lab6.cpp: определяет точку входа для консольного приложения.
//
#include "stdafx.h"
// НАЙТИ МИНИМУМ В МАССИВЕ
int main()
{
	int arr[] = { 3, 5, -8, 1, 0 };
	int len = 5;
	int min_of_arr;
	_asm {
				mov		ebx, arr[0]
				mov     min_of_arr, ebx
				mov     ecx, len
				xor     esi, esi
		cycl:	cmp     ecx, 0
			    je      cycl_end
				mov     eax, arr[esi]
				cmp     eax, min_of_arr
				jge     cont
				mov     min_of_arr, eax
		cont:
				add     esi, 4
				dec     ecx
				jmp     cycl
		cycl_end:
	}

	printf("%d \n", min_of_arr);
	return 0;
}