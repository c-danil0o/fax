.section .text
.globl oct_str_to_inter
#unsigned int oct_str_to_inter(char* str, unsigned int* greska);
oct_str_to_inter:
    pushl %ebp
    movl %esp, %ebp
    pushl $0
    pushl $8
    pushl %esi
    movl 8(%ebp), %esi
    xorl %eax, %eax
    cmpb $'-', (%esi)
    jne for
    movl $1, -4(%ebp)
    incl %esi
for:
    xorl %ecx, %ecx
    movb (%esi), %cl
    cmpb $0, %cl
    je negative
    cmpb $48, %cl
    jb err1
    cmpb $55, %cl
    ja err1
    subb $48, %cl
    mull -8(%ebp)
    jo err2
    addl %ecx, %eax
    jo err2
    incl %esi
    jmp for
negative:
    cmpl $1, -4(%ebp)
    jne convert_end
    negl %eax
   # jo err2
    jmp convert_end
err1:
    movl 12(%ebp), %ecx
    movl $1, (%ecx)
    jmp end
err2:
    movl 12(%ebp), %ecx
    movl $2, (%ecx)
    jmp end

convert_end:
    movl 12(%ebp), %ecx
    movl $0, (%ecx)
end:
    popl %esi
    movl %ebp, %esp
    popl %ebp
    ret

