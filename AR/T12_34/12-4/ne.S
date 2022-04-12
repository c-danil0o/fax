#T12 sa E2
#autor Danilo Cvijetic 12.04.2022

.section .data
unos: .fill 100, 1, 0           #rezervisanje mjesta za unos stringa
unos_len = 100
poruka1: .ascii "Unesite string: \0"
poruka1_len = .- poruka1
poruka2: .ascii "Novi string je: \0"
poruka2_len = .- poruka2
novi_string: .fill 100, 1, 0        #rezervisanje mjesta za novi string
novi_string_len = 100
.section .text
.globl main
main:
    movl $4, %eax
    movl $1, %ebx               #ispis prve poruuke
    movl $poruka1, %ecx
    movl $poruka1_len, %edx
    int $0x80

    movl $3, %eax
    movl $0, %ebx           #unos stringa
    movl $unos, %ecx
    movl $unos_len, %edx
    int $0x80

    movl $unos, %esi            #pokazivac na pocetak unesenog stringa
    movl $novi_string, %edi     #pokazivac na pocetak novog praznog stringa

for:
    cmpb $10, (%esi)            #da li smo dosli do kraja unesenog stringa
    je gotovo
    cmpb $'n', (%esi)           #da li je trenutno slovo 'n' ili 'N'
    je check
    cmpb $'N', (%esi)
    je check
next:                           #ako nije 'n' ili 'N' / ili ako posle njih nije 'e' ili 'E'
    movb (%esi), %al
    movb %al, (%edi)            #prebacivanje u novi string
    incl %esi
    incl %edi                   #prelazimo na sledece karaktere
    jmp for
check:
    cmpb $'e', 1(%esi)          #provjera da li je 'e' ili 'E' posle 'n/N'
    je delete
    cmpb $'E', 1(%esi)
    je delete
    jmp next                    #ako nije prebacujemo u novi string preko labele next
delete:
    addl $2, %esi               #ako je 'ne/Ne/nE/NE' onda taj dio stringa preskacemo
    jmp for
gotovo:
    movb $0, (%edi)             #dodajemo \0 na kraj novog stringa

    movl $4, %eax
    movl $1, %ebx
    movl $poruka2, %ecx          #ispis poruke 
    movl $poruka2_len, %edx
    int $0x80

    movl $4, %eax
    movl $1, %ebx
    movl $novi_string, %ecx         #ispis novog stringa
    movl $novi_string_len, %edx
    int $0x80

kraj:
    movl $1, %eax
    movl $0, %ebx
    int $0x80
