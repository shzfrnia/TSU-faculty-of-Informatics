.386p	
dseg	segment para public use16
arr	dw 0, 2, 3, 2, 1, 6, 7, 2, 2, 3
len dw 10
max dw 0
dseg	ends
cseg	segment  use16
	assume cs:cseg,ds:dseg
start	proc far
    mov	ax,dseg
	mov	ds,ax
	

				mov		bx, arr[0]
				mov		max, bx
				mov		cx, len
				xor		si, si
		cycl:	cmp		cx, 0
				je		cycl_end
				mov		bx, arr[si]
				cmp		bx, max
				jle		cont
				mov		max, bx
		cont:
				add		si, 2
				dec		cx
				jmp		cycl
		cycl_end:
				mov ax, max
	ret
start endp
cseg	ends
end start




