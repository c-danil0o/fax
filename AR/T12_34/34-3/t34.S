#program <shiftovanje dvostruke preciznosti>
#autor SV25/2021 Cvijetic Danilo 09/12/21
#void shiftujDvostruko(unsigned long long *a, unsigned char *b, unsigned n);
.section .text
.globl shiftujDvostruko
shiftujDvostruko:
    pushl %ebp
    movl %esp, %ebp
    pushl %esi
    pushl %edi
    pushl %ebx
    movl 8(%ebp), %esi                  #pokazivac na niz 
    movl 12(%ebp), %edi                 #pokazivac na niz b
    movl $0, %ebx                       #brojac
shft:
    cmpl %ebx, 16(%ebp)                 #kraj petlje
    jle end
    movb (%edi,%ebx,1), %cl             #broj shiftovanja
    testl $1, %ebx
    jnz shiftujr                        #neparni    
    jz shiftujl                         #parni
shiftujr:
    shrl $1, 4(%esi,%ebx,8)         #shift desno 64bit
    rcrl $1, (%esi,%ebx,8)
    decb %cl                        #broj shift -1
    cmpb $0, %cl
    je next
    jmp shiftujr
shiftujl:
    shll $1, (%esi,%ebx,8)          #shift lijevo 64bit
    rcll $1, 4(%esi,%ebx,8)
    decb %cl
    cmpb $0, %cl
    je next
    jmp shiftujl
next:
    incl %ebx               #sledeci broj iz niza a
    jmp shft
end:
    popl %ebx
    popl %edi
    popl %esi
    movl %ebp, %esp
    popl %ebp
    ret
