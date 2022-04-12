#include <stdio.h>

unsigned int RUNPP_REG_ERR = 0;

int SaberiMnozi(int n, unsigned short *a, unsigned short *b,
                unsigned short *resenje);

void unesi_niz(char ime, unsigned short *niz, int n) {
  int i;
  printf("\nUnseite elemente niza '%c'\n", ime);
  for (i = 0; i < n; i++) {
    printf("%c[%d]=", ime, i);
    scanf("%hu", &niz[i]);
  }
}

void print_niz(char ime, unsigned short *niz, int n) {
  int i;
  printf("\nElementi niza '%c'\n", ime);
  for (i = 0; i < n; i++)
    printf("%c[%d]=%hu\n", ime, i, niz[i]);
}

int main() {
  int g, n;
  printf("Unesite N: ");
  scanf("%d", &n);
  unsigned short a[n];
  unsigned short b[n];
  unsigned short R[n];
  unesi_niz('a', a, n);
  unesi_niz('b', b, n);
  g = SaberiMnozi(n, a, b, R);
  print_niz('r', R, n);
  printf("Broj gresaka je: %d \n", g);
  return g;
}
