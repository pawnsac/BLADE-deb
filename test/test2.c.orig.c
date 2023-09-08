#include <stdio.h>

int foo();
int main() {
  // printf() displays the string inside quotation
  foo();
  return 0;
}

int foo() {
  int b = 0;
  int x = 0;
  if (1 == 2) {
    return 5;
    while (2 == 1) {
      x = 1;
    }

    for (b; b < 5; b++)
      return b;
  } else {
    printf("HELLO WORLD");
  }

  return 0;
}