#potprogram za konverziju broja iz stringa u zadatoj bazi u integer
.section .text
.globl convert_num
convert_num:   
    pushl %ebp
    movl %esp, %ebp
    pushl %ebx
    pushl %esi
    movl 8(%ebp), %ebx      #baza broja
    movl 12(%ebp), %esi     #string 
    xorl %eax, %eax         #rezultat
for:   
    xorl %ecx, %ecx
    movb (%esi), %cl
    cmpb $10, %cl
    je end
    cmpb $48, %cl
    jb error                #greska u nedozvoljenom karatkeru
    cmpb $58, %cl
    jb cnvrtasdecimal
    cmpb $65, %cl
    jb error
    cmpb $71, %cl
    jb cnvrtasletterup
    cmpb $97, %cl
    jb error
    cmpb $103, %cl
    jb cnvrtasletterlow
    jmp error
cnvrtasdecimal:
    subb $48, %cl
    cmpl %ecx, %ebx
    jle error           #greska u nedozvoljenom karatkeru
    mull %ebx
    jc error2           #carry greska
    addl %ecx, %eax
    jc error2
    incl %esi
    jmp for
cnvrtasletterlow:
    subb $87, %cl
    cmpl %ecx, %ebx
    jb error
    mull %ebx
    jc error2
    addl %ecx, %eax
    jc error2
    incl %esi
    jmp for
cnvrtasletterup:
    subb $55, %cl
    cmpl %ecx, %ebx
    jb error
    mull %ebx
    jc error2
    addl %ecx, %eax
    jc error2
    incl %esi
    jmp for
error:
    movl 16(%ebp), %eax
    movl $1, (%eax)
    jmp end
error2:
    movl 16(%ebp), %eax
    movl $2, (%eax)
end:
    popl %esi
    popl %ebx
    movl %ebp, %esp
    popl %ebp
    ret