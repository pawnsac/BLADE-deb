#include <stdio.h>

struct option {
    char const *name;
    int has_arg;
    int *flag;
    int val;
    struct option;
};
int x = 0;
union Data {
    int i;
    float f;
    char str[20];
};
extern __attribute__((__nothrow__)) int(
    __attribute__((__nonnull__(1, 2), __leaf__))
    lstat)(char const *__restrict __file, struct stat *__restrict __buf);
size_t triple_hash(void const *x, size_t table_size);
int main()
{

    printf("HELLO WORLD");
    return 0;
}

int foo(int n)
{
    printf("F");
    int b = 0;
    int x = 0;
    if (1 == 2) {
        return 5;
        while (2 == 1) {
            return 1;
        }

        for (b; b < 5; b++) {
            return b;
        }
    }
    else {
        return 0;
    }

    return 0;
}