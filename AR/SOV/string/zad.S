.section .data
string: .ascii "ooOOoo \0"
length = . - string - 1
prompt1: .ascii "Unesite neki tekst: \0"
prompt1_len = . - prompt1
prompt2: .ascii "Tekst sa ubacenim stringom: \0"
prompt2_len = . - prompt2
INPUT_MAX = 1000
input: .fill INPUT_MAX, 1, 0
.section .text
.globl main
main:
    movl $4, %eax
    movl $1, %ebx
    movl $prompt1, %ecx
    movl $prompt1_len, %edx
    int $0x80

    movl $3, %eax
    movl $0, %ebx
    movl $input, %ecx
    movl $INPUT_MAX, %edx
    int $0x80           #ostavljamo \n char na kraju stringa
    movl %eax, %edx         #duzina unosa
    decl %edx       #jer je pokazivac vec prvi char  (%esi)
    xorl %ecx, %ecx     #brojac razmaka
    movl $input, %esi
    movl $input, %eax
    addl %edx, %eax
    decl %esi
    subl $length, %eax
for:
    incl %esi
    cmpb $0, (%esi)
    je print
    cmpb $' ', (%esi)
    jne for
    incl %ecx
    cmpl $3, %ecx
    je init
    jmp for
init:
    addl $length, %eax
    movl %eax, %edi
    xorl %ecx, %ecx
    movl %edi, %ebx
    addl $length, %ebx
swap:
    cmpl %esi, %edi
    je nxt
    movb (%edi), %dl
    movb %dl, (%ebx)
    decl %edi
    decl %ebx
    jmp swap
nxt:
    incl %esi
    movl $string, %edx
insert:
    cmpb $0, (%edx)
    je for
    movb (%edx), %bl
    movb %bl, (%esi)
    incl %esi
    incl %edx
    jmp insert
print:
    movl $4, %eax
    movl $1, %ebx
    movl $prompt2, %ecx
    movl $prompt2_len, %edx
    int $0x80
    
    movl $4, %eax
    movl $1, %ebx
    movl $input, %ecx
    movl $INPUT_MAX, %edx
    int $0x80

kraj:
    movl $1, %eax
    movl $0, %ebx
    int $0x80