#program <zamjena dva susjedna karaktera u stringu>
#autor SV25/2021 Cvijetic Danilo 08/12/21
.section .data
string: .fill 21,1,0
#string: .ascii "danilo1"
poruka1: .ascii "Unesite tekst: \0"
poruka1_len = . - poruka1
poruka2: .ascii "Promenjen string: \0"
poruka2_len = . - poruka2
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
    movl $string, %ecx
    movl $20, %edx
    int $0x80                       #unos stringa
    movl $string, %esi
    movl %eax, %edi
for:
    movb (%esi), %cl            #iteracija po dva susjedna karaktera sve dok jedan od njih nije 0
    cmpb $0, %cl                #zbog slucaja za unos len = 20
    je end
    cmpb $10, %cl
    je end
    movb 1(%esi), %dl
    cmpb $10, %dl             #ukoliko je poslednji karakter \n prekida se petlja 
    je end
    movb %cl, 1(%esi)           #zamjena karaktera
    movb %dl, (%esi)
    addl $2, %esi
    jmp for
end:
    movl $4, %eax
    movl $1, %ebx
    movl $poruka2, %ecx
    movl $poruka2_len, %edx         #ispis
    int $0x80
    movl $4, %eax
    movl $1, %ebx
    movl $string, %ecx
    movl %edi, %edx
    int $0x80

kraj:
movl $1, %eax
movl $0, %ebx
int $0x80