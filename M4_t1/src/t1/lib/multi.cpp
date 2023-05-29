// Libreria para multiplicar dos numeros *100
// Noemi Carolina Guerra Montiel - A00826944

#include <stdio.h>
#include <iostream>

extern "C"{
    /**
     * @brief Función para multiplicar dos números enteros por 100.
     * @param x Primer número entero.
     * @param y Segundo número entero.
     * @return Puntero a un arreglo dinámico de enteros que contiene los resultados de la multiplicación.
     *         El primer elemento del arreglo es el resultado de x * 100 y el segundo elemento es el resultado de y * 100.
     */
    int* multi(int x, int y){
        // Crear un arreglo dinamico de ints para guardar los resultados
        int*c = new int[2];
        // Multiplicar los valores y guardar los resultados en el arreglo
        c[0] = x*100;
        c[1] = y*100;
        return c;
    }
    
    /**
     * @brief Función para borrar un arreglo dinámico de enteros.
     * @param ptr Puntero al arreglo dinámico de enteros que se desea borrar.
     */
    void delete_arr(int* ptr){
        delete[] ptr;
    }
}


