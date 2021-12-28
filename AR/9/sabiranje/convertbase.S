#potprogram za konverziju baze iz stringa u int
.section .text
.globl convert_base
convert_base:
    pushl %ebp
    movl %esp, %ebp
    pushl $10       #baza za konverziju
    pushl %ebx
    movl 8(%ebp), %ecx
    xorl %eax, %eax
for:
    movb (%ecx), %bl 
    cmpb $10, %bl
    je check
    subb $48, %bl
    cmpb $9, %bl
    ja error1
    cmpb $0, %bl
    jb error1
    mull -4(%ebp)
    addb %bl, %al
    incl %ecx
    jmp for
error1:
    movl 12(%ebp), %ebx
    movl $1, (%ebx)
    jmp end
check:
    cmpl $16, %eax
    jle end
    movl 12(%ebp), %ebx
    movl $2, (%ebx)
end:
    popl %ebx
    movl %ebp, %esp
    popl %ebp
    ret
