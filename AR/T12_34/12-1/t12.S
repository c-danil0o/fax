#program <t12  prebrojavanje pluseva i minusa>
#autor SV25/2021 Cvijetic Danilo 08/12/21
.section .data
string1: .fill 20,1,0
string2: .fill 20,1,0
poruka1: .ascii "Unesite S1: \0"
poruka1_len = . - poruka1
poruka2: .ascii "Unesite S2: \0"
poruka2_len = . - poruka2
R: .byte 0
.section .text
.globl main
main:
    movl $4, %eax
    movl $1, %ebx
    movl $poruka1, %ecx
    movl $poruka1_len, %edx
    int $0x80

    movl $3, %eax
    movl $1, %ebx
    movl $string1, %ecx
    movl $20, %edx
    int $0x80
    movl $string1, %esi

    movl $4, %eax
    movl $1, %ebx
    movl $poruka2, %ecx
    movl $poruka2_len, %edx             #komande za stdin i stdout
    int $0x80

    movl $3, %eax
    movl $1, %ebx
    movl $string2, %ecx
    movl $20, %edx
    int $0x80
    movl $string2, %edi

    xorl %ecx, %ecx         #broj znakova +
    xorl %edx, %edx         #broj znakova -
    decl %esi
    decl %edi
count:
    incl %esi
    cmpb $0, (%esi)
    je count2
    cmpb $'+',(%esi)        #prebrojavanje pluseva
    jne count
    incl %ecx 
    jmp count
count2:
    incl %edi
    cmpb $0, (%edi)
    je compare
    cmpb $'-', (%edi)
    jne count2              #prebrojavanje minusa
    incl %edx
    jmp count2
compare:
    cmpl %ecx, %edx
    jl set1
    jg set2                 #poredjenje i postavljanje izlazne varijable R
    movl $3, R
    jmp kraj
set1:
    movl $1, R
    jmp kraj
set2:
    movl $2, R
kraj:
movl $1, %eax
movl R, %ebx
int $0x80