#include <stdio.h>

extern "C"{
    int* multi(int x, int y){
        int*c = new int[2];
        c[0] = x*100;
        c[1] = y*100;
        return c;
    }

    void delete_arr(int* ptr){
        delete[] ptr;
    }
}


