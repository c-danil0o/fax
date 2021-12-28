#program Sabiranje dva broja u unesenim bazama i ispis u zadatoj bazi
#autor Cvijetic Danilo SV25/2021
.section .data
ulaz1:      .ascii "Unesite bazu broja:\0"
ulaz1_len = . - ulaz1
ulaz2:      .ascii "Unesite broj:\0"
ulaz2_len = . - ulaz2
ulaz3:      .ascii "Unesite bazu rezultata:\0"
ulaz3_len = . - ulaz3
izlaz1:     .ascii "Rezultat:\0"
izlaz1_len = . - izlaz1
greska1:    .ascii "Greska: pogresan znak!\0"
greska1_len = . - greska1
greska2:    .ascii "Greska: prekoracenje!\0"
greska2_len = . - greska2
input1_baza: .fill 3, 1, 0
input1_baza_len = . - input1_baza
input2_baza: .fill 3, 1, 0
input2_baza_len = . - input2_baza
result_baza: .fill 3, 1, 0
result_baza_len = . - result_baza
input1:     .fill 30, 1, 0
input1_len = 30
input2:     .fill 30, 1, 0
input2_len = 30
base1: .long 0
base2: .long 0
baser: .long 0
num1: .long 0
num2: .long 0
result: .long 0
greska: .long 0
result_string: .fill 30,1,0
string_len: .long 0
.section .text
.globl main
main:
    movl $4, %eax               #unesite bazu broja
    movl $1, %ebx
    movl $ulaz1, %ecx
    movl $ulaz1_len, %edx
    int $0x80

    movl $3, %eax
    movl $0, %ebx               #unos baze broja
    movl $input1_baza, %ecx
    movl $input1_baza_len, %edx
    int $0x80
    pushl $greska
    pushl $input1_baza
    call convert_base
    addl $8, %esp
    cmpl $1, greska
    je printgreska1
    cmpl $2, greska
    je printgreska2
    movl %eax, base1

    movl $4, %eax
    movl $1, %ebx
    movl $ulaz2, %ecx           #unos prvog broja
    movl $ulaz2_len, %edx
    int $0x80

    movl $3, %eax
    movl $0, %ebx
    movl $input1, %ecx
    movl $input1_len, %edx
    int $0x80

    pushl $greska
    pushl $input1
    pushl base1
    call convert_num
    addl $12, %esp
    cmpl $1, greska
    je printgreska1
    cmpl $2, greska
    je printgreska2
    movl %eax, num1


    movl $4, %eax
    movl $1, %ebx               #unesite bazu drugog broja
    movl $ulaz1, %ecx
    movl $ulaz1_len, %edx
    int $0x80
    
    movl $3, %eax
    movl $0, %ebx               #unos baze drugog broja
    movl $input2_baza, %ecx
    movl $input2_baza_len, %edx
    int $0x80

    pushl $greska
    pushl $input2_baza
    call convert_base
    addl $8, %esp
    cmpl $1, greska
    je printgreska1
    cmpl $2, greska
    je printgreska2
    movl %eax, base2

    movl $4, %eax
    movl $1, %ebx               #unos drugog broja
    movl $ulaz2, %ecx
    movl $ulaz2_len, %edx
    int $0x80

    movl $3, %eax
    movl $0, %ebx
    movl $input2, %ecx
    movl $input2_len, %edx
    int $0x80

    pushl $greska
    pushl $input2
    pushl base2
    call convert_num
    addl $12, %esp
    cmpl $1, greska
    je printgreska1
    cmpl $2, greska
    je printgreska2
    movl %eax, num2

    movl $4, %eax
    movl $1, %ebx
    movl $ulaz3, %ecx           #unesite bazu rezultata
    movl $ulaz3_len, %edx
    int $0x80

    movl $3, %eax
    movl $0, %ebx               #unos baze rezultata
    movl $result_baza, %ecx
    movl $result_baza_len, %edx
    int $0x80

    pushl $result_baza
    call convert_base
    addl $4, %esp
    movl %eax, baser

    movl num1, %eax
    addl num2, %eax
    jc printgreska2
    pushl $result_string
    pushl %eax
    pushl baser
    call convert_string
    addl $8, %esp
    movl %eax, string_len

    movl $4, %eax               #rezultat
    movl $1, %ebx
    movl $izlaz1, %ecx
    movl $izlaz1_len, %edx
    int $0x80
    movl $4, %eax               #rezultat
    movl $1, %ebx
    movl $result_string, %ecx
    movl string_len, %edx
    int $0x80
    jmp kraj
printgreska1:
    movl $4, %eax               #greska1
    movl $1, %ebx
    movl $greska1, %ecx
    movl $greska1_len, %edx
    int $0x80
    jmp kraj
printgreska2:
    movl $4, %eax               #greska1
    movl $1, %ebx
    movl $greska2, %ecx
    movl $greska2_len, %edx
    int $0x80

kraj:
    movl $1, %eax
    movl $0, %ebx
    int $0x80