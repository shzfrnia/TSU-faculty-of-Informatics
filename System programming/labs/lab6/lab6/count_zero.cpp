// lab6.cpp: определяет точку входа для консольного приложения.
//
#include "stdafx.h"
// НАЙТИ МИНИМУМ В МАССИВЕ
int main()
{
	int arr[] = { 3, 0, 5, -8, 1, 0 ,0};
	int len = 7;
	int count_zero = 0;
	_asm {
					mov		ebx, arr[0]
					mov		ecx, len
					xor		esi, esi
		cycl:		cmp		ecx, 0
					je		cycl_end
					mov		ebx, arr[esi]
					cmp		ebx, 0
					jne		cont
					inc		count_zero
		cont:		
					add		esi, 4
					dec		ecx
					jmp		cycl
		cycl_end:
		//		mov		ebx, arr[0]
		//		mov     min_of_arr, ebx
		//		mov     ecx, len
		//		xor     esi, esi
		//cycl:	cmp     ecx, 0
		//		je      cycl_end
		//		mov     eax, arr[esi]
		//		cmp     eax, min_of_arr
		//		jge     cont
		//		mov     min_of_arr, eax
		//cont:
		//		add     esi, 4
		//		dec     ecx
		//		jmp     cycl
		//cycl_end:
	}

	printf("%d \n", count_zero);
	return 0;
}