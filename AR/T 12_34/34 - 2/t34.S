#program <potprogram T34 sabiranje dva niza >
#autor SV25/2021 Cvijetic Danilo 08/12/21
#int SaberiMnozi(int n, unsigned short *a, unsigned short *b, unsigned short *resenje);
.section .text
.globl SaberiMnozi
SaberiMnozi:
    pushl %ebp
    movl %esp, %ebp
    pushl $0    #broj gresaka
    pushl %esi
    pushl %edi
    pushl %ebx
    movl 12(%ebp), %esi
    movl 16(%ebp), %edi
    movl 20(%ebp), %ecx
    movl $0, %ebx       #brojac

for:
    cmpl %ebx, 8(%ebp)              #petlja za parne brojeve krece od nule, increment je 2
    jle next
    movw (%esi,%ebx,2), %ax             
    mulw (%edi,%ebx,2)              #mnozenje drugog sa prvim
    jc greska1
    movw %ax, (%ecx, %ebx,2)        #rez u treci niz
    addl $2, %ebx
    jmp for
next:
    movl $1, %ebx               #init petlje za neparne
for2:
    cmpl %ebx, 8(%ebp)
    jle end
    movw (%esi, %ebx,2), %ax
    movw %ax, (%ecx,%ebx,2)
    movw (%edi, %ebx,2), %ax
    addw %ax,(%ecx,%ebx,2)          #sabiranje dva broja u treci niz
    jc greska2                      #carry daje gresu i 11111 se stavlja u rez
    addl $2, %ebx
    jmp for2
greska1:
    movw $11111, (%ecx,%ebx,2)
    addl $2, %ebx               #11111
    incl -4(%ebp)
    jmp for                     #nastavlja se iteracija
greska2:
    movw $11111, (%ecx,%ebx,2)
    addl $2, %ebx
    incl -4(%ebp)
    jmp for2
end:
    movl -4(%ebp),%eax              #broj gresaka
    popl %ebx
    popl %edi
    popl %esi
    movl %ebp, %esp
    popl %ebp
    ret
