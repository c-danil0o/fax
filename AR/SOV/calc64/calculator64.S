
.section .data
poruka1: .ascii "Unesite izraz: \0"
poruka2: .ascii "Rezultat: \0"
err1: .ascii "Nepoznata operacija!\0"
err2: .ascii "Pogresan prvi operand!\0"
err3: .ascii "Pogresan drugi operand!\0"
err4: .ascii "Prekoracenje prvog operanda!\0"
err5: .ascii "Prekoracenje drugog operanda!\0"
INPUT_MAX = 100
input: .fill INPUT_MAX, 1, 0
substring: .fill 100, 1, 0
result: .fill 100,1,0
operand1: .quad 0
operand2: .quad 0
result_int: .quad 0
operator: .long 0
position: .long 0
err_code: .long 0
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
    movl $0, -1(%ecx, %edx, 1)
.endm
######################################
#potgrogram za mnozenje u dvostrukoj preciznosti sa 16
multiply:
    pushl %ebp
    movl %esp, %ebp
    pushl $16
    pushl %ebx
    movl 8(%ebp), %eax          #low
    movl 12(%ebp), %edx         #high
    movl $0, %ecx               #low
    movl $0, %ebx               #high
multiply_for:
    cmpl $0, -4(%ebp)
    je multiply_end
    addl %eax, %ecx
    adcl %edx, %ebx
    jc carry_error
    decl -4(%ebp)
    jmp multiply_for
carry_error:
    movl $-1, %eax
multiply_end:
    movl %ecx, 8(%ebp)
    movl %ebx, 12(%ebp)
    popl %ebx
    movl %ebp, %esp
    popl %ebp
    ret
#####################################
#potprogram za konverziju iz 64bit int u str
str_convert:
    pushl %ebp
    movl %esp, %ebp
    pushl %esi
    pushl %edi
    movl 8(%ebp), %esi          #pokazivac na rezultat
    movl 12(%ebp), %edi
str_for:
    pushl %edi
    call _Z6dividePx
    addl $4, %esp
    cmpl $10, %eax
    jb decimal_str
    addl $55, %eax
    movb %al, (%esi)
    incl %esi
    movl (%edi), %ecx
    testl %ecx, %ecx
    jnz str_convert
    movl 4(%edi), %ecx
    testl %ecx, %ecx
    jnz str_convert
    movl 8(%ebp), %edi
    movl $0, (%esi)
    decl %esi
    jmp swap
decimal_str:
    addl $48, %eax
    movb %al, (%esi)
    incl %esi
    movl (%edi), %ecx
    testl %ecx, %ecx
    jnz str_convert
    movl 4(%edi), %ecx
    testl %ecx, %ecx
    jnz str_convert
    movl 8(%ebp), %edi
    movl $0, (%esi)
    decl %esi
swap:
    cmpl %esi, %edi
    jae str_end
    movb (%esi), %cl
    movb (%edi), %ch
    movb %cl, (%edi)
    movb %ch, (%esi)
    decl %esi
    incl %edi
    jmp swap
str_end:
    popl %edi
    popl %esi
    movl %ebp, %esp
    popl %ebp
    ret
######################################
#potprogram za konverziju
convert:
    pushl %ebp
    movl %esp, %ebp
    pushl $16
    pushl %esi
    pushl %edi
    movl 8(%ebp), %esi      #adresa substringa   12 error code
    xorl %eax, %eax
    xorl %edx, %edx
convert_for:
    xorl %ecx, %ecx
    movb (%esi), %cl
    cmpb $0, %cl
    je convert_end
    cmpb $48, %cl
    jb error2
    cmpb $58, %cl
    jb decimal
    cmpb $65, %cl
    jb error2
    cmpb $71, %cl
    jb upper
    cmpb $97, %cl
    jb error2
    cmpb $103, %cl
    jb lower
    jmp error2
decimal:
    subb $48, %cl
    pushl %edx
    pushl %eax
    call multiply
    cmpl $-1, %eax
    je error4
    popl %eax
    popl %edx
    addl %ecx, %eax
    adcl $0, %edx
    jc error4
    incl %esi
    jmp for
upper:  
    subb $55, %cl
    pushl %edx
    pushl %eax
    call multiply
    cmpl $-1, %eax
    je error4
    popl %eax
    popl %edx
    addl %ecx, %eax
    adcl $0, %edx
    jc error4
    incl %esi
    jmp for
lower:
    subb $87, %cl
    pushl %edx
    pushl %eax
    call multiply
    cmpl $-1, %eax
    je error4
    popl %eax
    popl %edx
    addl %ecx, %eax
    adcl $0, %edx
    jc error4
    incl %esi
    jmp for
error2:
    movl 12(%ebp), %ecx
    movl $1, (%ecx)
    jmp convert_terminate
error4:
    movl 12(%ebp), %ecx
    movl $2, (%ecx)
    jmp convert_terminate
convert_end:
    movl 16(%ebp), %ecx
    movl %eax, (%ecx)
    movl %edx, 4(%ecx)
convert_terminate:
    popl %edi
    popl %esi
    movl %ebp, %esp
    popl %ebp
    ret
################################################

main:
    print_str $poruka1
    input_str $input $INPUT_MAX
    movl $input, %esi
    movl $substring, %edi
skip_spaces:
    cmpb $' ', (%esi)
    jne for
    incl %esi
    jmp skip_spaces
for:
    cmpb $' ', (%esi)
    je check
    cmpb $0, (%esi)
    je check
    movb (%esi), %cl
    movb %cl, (%edi)
    incl %esi
    incl %edi
    jmp for
check:
    incl position
    movl $0, (%edi)
    cmpb $1, position
    je cnvrt1
    cmpb $2, position
    je checkop
    cmpb $3, position
    je cnvrt2
checkop:
    cmpb $'&', (%edi)
    je op1
    cmpb $'|', (%edi)
    je op2
    cmpb $'^', (%edi)
    je op3
    jmp error1

cnvrt1: 
    pushl $operand1
    pushl $err_code
    pushl $substring
    call convert
    addl $12, %esp
    cmpl $1, err_code
    je print_err2
    cmpl $2, err_code
    je print_err4
    jmp skip_spaces
cnvrt2:
    pushl $operand2
    pushl $err_code
    pushl $substring
    call convert
    addl $12, %esp
    cmpl $1, err_code
    je print_err3
    cmpl $2, err_code
    je print_err5
    jmp calculate
op1:
    movl $1, operator
    jmp skip_spaces
op2:
    movl $2, operator
    jmp skip_spaces
op3:
    movl $3, operator
    jmp skip_spaces
calculate:
    cmpl $1, operator
    je doand
    cmpl $2, operator
    je door
    cmpl $3, operator
    je doxor
doand:
    movl operand1, %eax
    movl operand1+4, %edx
    andl operand2, %eax
    andl operand2+4, %edx
    jmp convert_str
door:
    movl operand1, %eax
    movl operand1+4, %edx
    orl operand2, %eax
    orl operand2+4, %edx
    jmp convert_str
doxor:
    movl operand1, %eax
    movl operand1+4, %edx
    xorl operand2, %eax
    xorl operand2+4, %edx
    jmp convert_str
convert_str:
    movl %eax, result_int
    movl %edx, result_int+4
    pushl $result_int
    pushl $result
    call str_convert
    addl $12, %esp
    print_str $poruka2
    print_str $result
    jmp kraj
error1:
    print_str $err1
    jmp kraj
print_err2:
    print_str $err2
    jmp kraj
print_err3: 
    print_str $err3
    jmp kraj
print_err4:
    print_str $err4
    jmp kraj
print_err5:
    print_str $err5
kraj:
movl $1, %eax
movl $0, %ebx
int $0x80