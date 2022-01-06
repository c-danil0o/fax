#program sabiranja niza brojeva u inverznoj poljskoj notaciji IPN
#autor Cvijetic Danilo SV25/2021
.section .data
poruka1: .ascii "Unesite izraz: \0"
poruka2: .ascii "Rezultat je: \0"
poruka_greska1: .ascii "Ulazni izraz je prazan!\0"
poruka_greska2: .ascii "Nedozvoljen karatker!\0"
poruka_greska3: .ascii "Overflow ulaza!\0"
poruka_greska4: .ascii "Overflow u sabiranju!\0"
INPUT_MAX = 150
input: .fill INPUT_MAX, 1,0
substring: .fill 20,1,0
err_code: .long 0
result: .fill 20, 1, 0

.section .text
.globl main
.macro print_str string
    movl $4, %eax
    movl $1, %ebx
    movl \string, %ecx
    movl $0, %edx
1:  cmpb $0, (%ecx)
    je 2f
    incl %ecx
    incl %edx
    jmp 1b
2:  movl \string, %ecx
    int $0x80
.endm
.macro input_str string length
    movl $3, %eax
    movl $0, %ebx
    movl \string, %ecx
    movl \length, %edx
    int $0x80
    movb $0, -1(%ecx, %eax, 1)
.endm
#potrprogram za konverziju inta u decimalni#######################
convert:
    pushl %ebp
    movl %esp, %ebp
    pushl $10
    pushl %esi
    pushl %edi
    movl 8(%ebp), %esi         #adresa substringa za konverziju
    xorl %eax, %eax            #rezultat
convert_for:
    xorl %ecx, %ecx
    movb (%esi), %cl
    cmpb $0, %cl
    je convert_end
    subb $48, %cl
    cmpb $0, %cl
    jb err2
    cmpb $9, %cl
    ja err2
    mull -4(%ebp)
    jc err3
    addl %ecx, %eax
    jc err3
    incl %esi
    jmp convert_for
err1:
    movl 12(%ebp), %ecx
    movl $1, (%ecx)
    jmp convert_end
err2:
    movl 12(%ebp), %ecx
    movl $2, (%ecx)
    jmp convert_end
err3:
    movl 12(%ebp), %ecx
    movl $3, (%ecx)
convert_end:
    popl %edi
    popl %esi
    movl %ebp, %esp
    popl %ebp
    ret
############################
#potprogram konverzije rezultata iz int u str
convert_str:
    pushl %ebp
    movl %esp, %ebp
    pushl $10
    pushl %edi
    pushl %esi
    movl 8(%ebp), %esi
    movl 12(%ebp), %eax
str_for:
    xorl %edx, %edx
    divl -4(%ebp)
    addl $48, %edx
    movb %dl, (%esi)
    incl %esi
    testl %eax, %eax
    jnz str_for
    movb $0, (%esi)
    decl %esi           #h iterator
    movl 8(%ebp), %edi #l iterator
swap:
    cmpl %edi, %esi
    jbe str_end
    movb (%esi), %cl
    movb (%edi), %ch
    movb %cl, (%edi)
    movb %ch, (%esi)
    incl %edi
    decl %esi
    jmp swap
str_end:
    popl %esi
    popl %edi
    movl %ebp, %esp
    popl %ebp
    ret
###########################################
main:
    print_str $poruka1
    input_str $input, $INPUT_MAX
    movl $input, %esi
    movl $substring, %edi
    cmpb $0, (%esi)
    je print_err1
for:
    movb (%esi), %al
    cmpb $'+', %al
    je op
    cmpb $' ', %al
    je cnvrt
    cmpb $0, %al
    je end
    movb %al, (%edi)
    incl %esi
    incl %edi
    jmp for
cnvrt:
    movl $0, (%edi)
    pushl $err_code
    pushl $substring
    call convert
    addl $8, %esp
    cmpl $1, err_code
    je print_err1
    cmpl $2, err_code
    je print_err2
    cmpl $3, err_code
    je print_err3
    pushl %eax
    incl %esi
    movl $substring, %edi
    jmp for
op:
    popl %eax
    popl %ebx
    addl %ebx, %eax
    jc print_err4
    pushl %eax
    movl $substring, %edi
    addl $2, %esi
    jmp for
print_err1:
    print_str $poruka_greska1
    movl $1, %ebx
    jmp kraj
print_err2:
    print_str $poruka_greska2
    movl $2, %ebx
    jmp kraj
print_err3:
    print_str $poruka_greska3
    movl $3, %ebx
    jmp kraj
print_err4:
    print_str $poruka_greska4
    movl $4, %ebx
    jmp kraj
end:
    #na stacku je vec rezultat tako da ne treba push
    pushl $result
    call convert_str
    addl $8, %esp
    print_str $poruka2
    print_str $result
    movl $0, %ebx
kraj:
    movl $1, %eax
    int $0x80
