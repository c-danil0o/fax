#include <stdint.h>
#include <stdio.h>
int divide(int64_t* num)
{
    int remainder = *num % 16;
     *num = *num / 16;
    return remainder;
}