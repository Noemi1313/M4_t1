// Libreria para multiplicar dos numeros *100

#include <stdio.h>
#include <iostream>

extern "C"{
    // Funcion para multiplicar 2 numeros *100
    int* multi(int x, int y){
        // Crear un arreglo dinamico de ints para guardar los resultados
        int*c = new int[2];
        // Multiplicar los valores y guardar los resultados en el arreglo
        c[0] = x*100;
        c[1] = y*100;
        return c;
    }
    
    // Funcion para borrar el arreglo
    void delete_arr(int* ptr){
        delete[] ptr;
    }
}


