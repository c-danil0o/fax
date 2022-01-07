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
operator: .long 0
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
    movb $0, -1(%ecx, %eax, 1)
.endm
###################
convert:
    pushl %ebp
    movl %esp, %ebp
    pushl %esi
    pushl %edi
    movl 8(%ebp), %esi
    movl $0, %eax               #nizi dio broja
    movl $0, %edx               #visi dio broja
convert_for:
    movb (%esi), %cl
    cmpb $0, %cl
    je convert_end
    testl $0xf0000000,%edx
    jnz err_overflow
    movl $4, %edi
shift:
    shll $1, %eax
    rcll $1, %edx
    decl %edi
    cmpl $0, %edi
    jne shift
check:
    cmpb $48, %cl
    jb err_invalidchar
    cmpb $58, %cl
    jb decimal
    cmpb $65, %cl
    jb err_invalidchar
    cmpb $71, %cl
    jb upper
    cmpb $97, %cl
    jb err_invalidchar
    cmpb $103, %cl
    jb lower
    jmp err_invalidchar
decimal:
    subb $48, %cl
    jmp put
upper:
    subb $55, %cl
    jmp put
lower:
    subb $87, %cl
put:
    orb %cl, %al
    incl %esi
    jmp convert_for
err_invalidchar:
    movl 12(%ebp), %ecx
    movl $1, (%ecx)
    jmp convert_end
err_overflow:
    movl 12(%ebp), %ecx
    movl $2, (%ecx)
convert_end:
    popl %edi
    popl %esi
    movl %ebp, %esp
    popl %ebp
    ret    
#####################################
string_convert:
    pushl %ebp
    movl %esp, %ebp
    pushl %esi
    pushl %edi
    movl 8(%ebp), %eax
    movl 12(%ebp), %edx
    movl 16(%ebp), %esi
sc_for:
    testl %eax, %eax
    jnz sc_conv
    testl %edx, %edx
    jnz sc_conv
    jmp sc_next
sc_conv:
    movb %al, %cl       #kopija najnizih 4 bita
    andb $0xf, %cl
    cmpb $9, %cl
    ja letter
    addb $48, %cl
    movb %cl, (%esi)
    incl %esi
    movl $4, %edi
    jmp shift2
letter: 
    addb $55, %cl
    movb %cl, (%esi)
    incl %esi
    movl $4, %edi
    jmp shift2
shift2:
    cmpl $0, %edi
    je sc_for
    shrl $1, %edx
    rcrl $1, %eax
    decl %edi
    jmp shift2
sc_next:
    movl $0, (%esi)
    movl 16(%ebp), %edi
    decl %esi
sc_swap:
    cmpl %esi, %edi
    jae sc_end
    movb (%esi), %cl
    movb (%edi), %ch
    movb %ch, (%esi)
    movb %cl, (%edi)
    incl %edi
    decl %esi
    jmp sc_swap
sc_end:
    popl %edi
    popl %esi
    movl %ebp, %esp
    popl %ebp
    ret
#####################33
main:
    print_str $poruka1
    input_str $input $INPUT_MAX
    movl $input, %esi
    movl $substring, %edi
for:
    movb (%esi), %cl
    cmpb $' ', %cl
    je next
    cmpb $0, %cl
    je next
    movb %cl, (%edi)
    incl %esi
    incl %edi
    jmp for
next:
    movl $0, (%edi)
    pushl $err_code
    pushl $substring
    call convert
    addl $8, %esp
    cmpl $1, err_code
    je print_err2
    cmpl $2, err_code
    je print_err4
    movl %eax, operand1
    movl %edx, operand1+4
    movl $substring, %edi
skip_spaces:
    cmpb $' ', (%esi)
    jne checkop
    incl %esi
    jmp skip_spaces
checkop:
    cmpb $'&', (%esi)
    je op1
    cmpb $'|', (%esi)
    je op2
    cmpb $'^', (%esi)
    je op3
    jmp print_err1
op1:
    movl $1, operator
    incl %esi
    jmp skip2
op2:
    movl $2, operator
    incl %esi
    jmp skip2
op3:    
    movl $3, operator
    incl %esi
skip2:
    cmpb $' ', (%esi)       #skipping spaces after operator
    jne for2
    incl %esi
    jmp skip2
for2:
    movb (%esi), %cl
    cmpb $' ', %cl
    je next2
    cmpb $0, %cl
    je next2
    movb %cl, (%edi)
    incl %esi
    incl %edi
    jmp for2
next2:
    movl $0, (%edi)
    pushl $err_code
    pushl $substring
    call convert
    addl $8, %esp
    cmpl $1, err_code
    je print_err3
    cmpl $2, err_code
    je print_err5
    movl %eax, operand2
    movl %edx, operand2+4
determine_op:
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
    jmp to_str
door:
    movl operand1, %eax
    movl operand1+4, %edx
    orl operand2, %eax
    orl operand2+4, %edx
    jmp to_str
doxor:  
    movl operand1, %eax
    movl operand1+4, %edx
    xorl operand2, %eax
    xorl operand2+4, %edx
to_str:
    pushl $result
    pushl %edx
    pushl %eax
    call string_convert
    addl $12, %esp
    print_str $poruka2
    print_str $result
    jmp kraj
print_err1:
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