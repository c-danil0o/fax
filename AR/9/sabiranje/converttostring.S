#potprogram za konverziju iz integera u string za zadatu bazu
.section .text
.globl convert_string
convert_string:
    pushl %ebp
    movl %esp, %ebp
    pushl %esi
    pushl %ebx
    movl 8(%ebp), %ecx         #baza 
    movl 12(%ebp), %eax        #broj
    movl 16(%ebp), %esi        #pokazivac na rezultat
    movl $0, %ebx       #brojac duzine
cnvrt:
    xorl %edx, %edx
    divl %ecx
    cmpl $10, %edx
    jb decstr
    addl $55, %edx
    movb %dl, (%esi)
    incl %esi
    incl %ebx
    testl %eax, %eax
    jnz cnvrt
    movl 16(%ebp), %ecx
    jmp next
decstr:
    addl $48, %edx
    movb %dl, (%esi)
    incl %ebx
    incl %esi
    testl %eax, %eax
    jnz cnvrt
    movl 16(%ebp), %ecx

next:
    movl $0, (%esi)
    decl %esi
swap:   
    cmpl %ecx, %esi
    jle end
    movb (%ecx), %dl
    movb (%esi), %dh
    movb %dh, (%ecx)
    movb %dl, (%esi)
    incl %ecx
    decl %esi
    jmp swap
end:
    movl %ebx, %eax
    popl %ebx
    popl %esi
    movl %ebp, %esp
    popl %ebp
    ret