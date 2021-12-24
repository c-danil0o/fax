#program <prebrojavanje samoglasnika>
#autor SV25/2021 Cvijetic Danilo 09/12/21
.section .data
ispis: .ascii "Unesite string: \0"
ispis_len = . - ispis
string: .fill 40,1,0
.section .text
.globl main
main:
    movl $4, %eax
    movl $1, %ebx
    movl $ispis, %ecx
    movl $ispis_len, %edx
    int $0x80

    movl $3, %eax
    movl $1, %ebx
    movl $string, %ecx          #unos stringa
    movl $40, %edx
    int $0x80
    movl $string, %esi
    xorl %ebx,%ebx
count:
    cmpb $0, (%esi)
    je kraj
    cmpb $'a', (%esi)
    je samogl
    cmpb $'A', (%esi)           #broje se i lCase i upCase
    je samogl
    cmpb $'e', (%esi)
    je samogl
    cmpb $'E', (%esi)
    je samogl
    cmpb $'i', (%esi)
    je samogl
    cmpb $'I', (%esi)
    je samogl
    cmpb $'o', (%esi)
    je samogl
    cmpb $'O', (%esi)
    je samogl
    cmpb $'u', (%esi)
    je samogl
    cmpb $'U', (%esi)
    je samogl
    incl %esi
    jmp count
samogl:
    incl %ebx               #povecava se brojac samoglasnika
    incl %esi
    jmp count
kraj:
movl $1, %eax
int $0x80