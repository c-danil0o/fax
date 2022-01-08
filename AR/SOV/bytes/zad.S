.section .data
input: .fill 20, 1, 0
INPUT_MAX = 19
prompt1: .ascii "Unesite 64-bitni dekadni ceo broj: \0"
prompt2: .ascii "Broj se sastoji iz ovih bajtova (redosled od najnizeg): \0"
err1: .ascii "Pogresna cifra! \0"
err2: .ascii "Prekoracenje! \0"
input_int: .quad 0
err_code: .long 0
out_string: .fill 50, 1, 0
minus: .long 0
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
#potprogram za konverziju iz str u 64bit int
convert:
    pushl %ebp
    movl %esp, %ebp
    pushl $10       #baza za konverziju
    pushl %ebx
    pushl %esi
    pushl %edi
    movl 12(%ebp), %esi         # pointer na string
    xorl %eax, %eax             #nizi dio broja 
    xorl %edx, %edx             #visi dio broja
    xorl %ebx, %ebx             #pomocni registar za char
convert_for:
    movb (%esi), %bl
    cmpb $0, %bl
    je convert_end
    subb $48, %bl
    cmpb $0, %bl
    jb err_inv_char
    cmpb $9, %bl
    ja err_inv_char
    imull $10, %edx, %ecx    #visi dio broja pomnozen sa bazom privremeno u ecx
    jo err_overflow
    xorl %edx, %edx
    mull -4(%ebp)           #mnozimo nizi dio broja sa bazon
    addl %ecx, %edx         #ostatak prethodnog mnozenja je u edx i dodajemo ga na visi dio broja
    jo err_overflow         #prekoracenje u visem dijelu broja
    addl %ebx, %eax         #dodajemo char na nizi dio broja
    adcl $0, %edx
    jo err_overflow
    incl %esi
    jmp convert_for
convert_end:
    movl 8(%ebp), %ebx
    movl %eax, (%ebx)           #nizi dio broja 
    movl %edx, 4(%ebx)          #visi dio broja
    jmp convert_return
err_inv_char:
    movl 16(%ebp), %ebx
    movl $1, (%ebx)
    jmp convert_return
err_overflow:
    movl 16(%ebp), %ebx
    movl $2, (%ebx)
convert_return:
    popl %edi
    popl %esi
    popl %ebx
    movl %ebp, %esp
    popl %ebp
    ret
##########################
#potprogram za konverziju u segmente broja
convert_str:
    pushl %ebp
    movl %esp, %ebp
    pushl $0            #brojac cifara (ukupno 16 za prekid)
    pushl %esi
    pushl %edi
    pushl %ebx
    movl 8(%ebp), %esi
    movl 12(%ebp), %ecx
    movl (%ecx), %eax
    movl 4(%ecx), %edx
    movl $0, %ebx       #brojac cifara (za ispis po 2)
    jmp str_for
check:
    cmpl $16, -4(%ebp)
    je str_end
    cmpl $2, %ebx
    jne str_for
    movb $' ', (%esi)
    movb -1(%esi), %cl
    movb -2(%esi), %ch
    movb %cl, -2(%esi)
    movb %ch, -1(%esi)
    incl %esi
    movl $0, %ebx
str_for:
    movb %al, %cl
    andb $0xf, %cl
    incl -4(%ebp)
    cmpb $9, %cl
    ja letter
    addb $48, %cl
    movb %cl, (%esi)
    incl %esi
    incl %ebx
    movl $4, %ecx
    jmp shift
letter: 
    addb $55, %cl
    movb %cl, (%esi)
    incl %esi
    incl %ebx
    movl $4, %ecx
shift:
    cmpl $0, %ecx
    je check
    shrl $1, %edx           #shift desno (4 puta)
    rcrl $1, %eax
    decl %ecx
    jmp shift
str_end:
    movb $10, (%esi)
    popl %ebx
    popl %edi
    popl %esi
    movl %ebp, %esp
    popl %ebp
    ret
##########################
main:
    print_str $prompt1
    input_str $input $INPUT_MAX
    movl $input, %esi
    cmpb $'-', (%esi)
    jne cnvrt
    movl $1, minus
    incl %esi
cnvrt:
    pushl $err_code
    pushl %esi
    pushl $input_int
    call convert
    #posle poziva konvertovani broj je u input_int
    cmpl $1, err_code
    je print_err1
    cmpl $2, err_code
    je print_err2
    cmpl $1, minus
    jne separate
    negl input_int
    adcl $0, input_int+4
    negl input_int+4
separate:
    pushl $input_int
    pushl $out_string
    call convert_str
    addl $8, %esp
    print_str $prompt2
    print_str $out_string
    jmp end
print_err1:
    print_str $err1
    jmp end
print_err2:
    print_str $err2
end:
    movl $1, %eax
    movl $0, %ebx
    int $0x80


