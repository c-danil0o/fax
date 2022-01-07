.section .data
prompt1: .ascii "Unesi broj ocena 6: \0"
prompt2: .ascii "Unesi broj ocena 7: \0"
prompt3: .ascii "Unesi broj ocena 8: \0"
prompt4: .ascii "Unesi broj ocena 9: \0"
prompt5: .ascii "Unesi broj ocena 10: \0"
out1: .ascii "Procenat ocena 6 je: \0"
out2: .ascii "Procenat ocena 7 je: \0"
out3: .ascii "Procenat ocena 8 je: \0"
out4: .ascii "Procenat ocena 9 je: \0"
out5: .ascii "Procenat ocena 10 je: \0"
error: .ascii "Greska! \0"
out_num: .fill 20, 1, 0
in: .fill 10, 1, 0
int_values: .long 0, 0, 0, 0, 0
prompts: .long 0, 0, 0, 0, 0
out_prompts: .long 0, 0, 0, 0, 0
prompt: .long 0
hundred: .long 100
sum: .long 0
.section .text
.globl main
.macro print_str string
    movl $4, %eax
    movl $1, %ebx
    movl \string, %ecx
    movl $1, %edx
1: cmpb $0, (%ecx)
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
################
#fn za konverziju iz str u int
convert:
    pushl %ebp
    movl %esp, %ebp
    pushl $10
    pushl %esi
    movl 8(%ebp), %esi
    movl $0, %eax
convert_for:
    xorl %ecx, %ecx
    movb (%esi), %cl
    cmpb $0, %cl
    je convert_end
    subb $48, %cl
    cmpb $0, %cl
    jb err
    cmpb $9, %cl
    ja err
    mull -4(%ebp)
    addl %ecx, %eax
    incl %esi
    jmp convert_for
err:
    movl $-1, %eax
convert_end:
    popl %esi
    movl %ebp, %esp
    popl %ebp
    ret
###############################
#func za konverziju u str
convert_str:
    pushl %ebp
    movl %esp, %ebp
    pushl $10           #baza
    pushl %esi
    pushl %edi
    pushl %ebx
    movl 8(%ebp), %esi  #adresa stringa
    movl 12(%ebp), %eax #broj
    xorl %edx, %edx
    divl -4(%ebp)
    movl %eax, %ebx
    movl 12(%ebp), %eax
str_for:
    xorl %edx, %edx
    divl -4(%ebp)
    addb $48, %dl
    movb %dl, (%esi)
    incl %esi
    testl %eax, %eax
    jnz str_for
    movl %esi, %ecx
    decl %ecx
    movb $37, (%esi)
    movb $' ', 1(%esi)
    addl $2, %esi
    movl $0, %edx
add_hash:
    cmpl %edx, %ebx
    je swp
    movb $35, (%esi, %edx, 1)
    incl %edx
    jmp add_hash
swp:
    movb $10, (%esi, %edx, 1)
    movb $0, 1(%esi, %edx, 1)
    movl 8(%ebp), %edi
    movl %ecx, %esi
swap:
    cmpl %esi, %edi
    jae str_end
    movb (%esi), %al
    movb (%edi), %ah
    movb %al, (%edi)
    movb %ah, (%esi)
    incl %edi
    decl %esi
    jmp swap
str_end:
    popl %ebx
    popl %edi
    popl %esi
    movl %ebp, %esp
    popl %ebp
    ret

main:
    movl $0, %edi           #brojac
    movl $0, %ebx           #suma
    movl $prompts, %eax
    movl $out_prompts, %edx
init:   
    movl $prompt1, (%eax)
    movl $prompt2, 4(%eax)
    movl $prompt3, 8(%eax)
    movl $prompt4, 12(%eax)
    movl $prompt5, 16(%eax)
    movl $out1, (%edx)
    movl $out2, 4(%edx)
    movl $out3, 8(%edx)
    movl $out4, 12(%edx)
    movl $out5, 16(%edx)


for:
    movl prompts(,%edi, 4), %esi
    print_str %esi
    input_str $in, $10
    pushl $in
    call convert
    addl $4, %esp
    cmpl $-1, %eax
    je print_err
    movl %eax, int_values(, %edi,4)
    addl %eax, sum
    jc print_err
    incl %edi
    cmpl $5, %edi
    jne for
    movl $0, %edi
calculate:
    movl out_prompts(, %edi, 4), %esi
    print_str %esi
    movl int_values(, %edi, 4), %eax
    mull hundred
    xorl %edx, %edx
    divl sum
    pushl %eax
    pushl $out_num
    call convert_str
    addl $8, %esp
    print_str $out_num
    incl %edi
    cmpl $5, %edi
    jne calculate
    jmp kraj
print_err:
    print_str $error
kraj:
    movl $1, %eax
    movl $0, %ebx
    int $0x80