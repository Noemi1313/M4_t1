// Libreria para multiplicar dos numeros *100

#include <stdio.h>
#include <iostream>

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


