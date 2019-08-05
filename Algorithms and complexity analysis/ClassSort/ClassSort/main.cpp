//
//  main.cpp
//  lab1
//
//  Created by Михаил Уляков on 13.02.2018.
//  Copyright © 2018 Михаил Уляков. All rights reserved.
//
#include <iostream>
#include <string>
#include <ctime>
#include "work_with_array.hpp"
using namespace std;


int main(int argc, const char * argv[]) {
    bool show_array = false;
    char choosen = 'n';
    srand((unsigned int)time(nullptr));
    int lenght_of_array  = 10;
    unsigned short int type_of_arrays = 0;
    cout << "Input Lenght arrays: \033[1;20m";
    lenght_of_array = pars_input_to_int(); cout << "\033[0m" << "| Lenght is: \033[1;20m" << lenght_of_array << " \033[0m" << endl;
    if (lenght_of_array < 0) throw std::logic_error("\nLength musn't be less than ZERO");
    cout << "How type must be array? (1 - random, 2 - ascending, 3 - descendigly, 4 - ordered): \033[1;20m"; cin >> type_of_arrays; cout << "\033[0m";
    if (type_of_arrays < 1 || type_of_arrays > 4) throw std::logic_error("\nIncorrect type");
    cout << "Output arrays? (y - yes, n - no): \033[1;20m"; cin >> choosen; cout << "\033[0m";
    if (choosen == 'y') show_array = true; else if (choosen == 'n') show_array = false; else throw std::logic_error("Unkown command");
    cout << endl << '{' << "\033[1;20m--Inderect_Shall--\033[0m" << endl;
    int *array = new int[lenght_of_array];
    generate_int_array(array, lenght_of_array, type_of_arrays, 0, 200);
    
    inderect_sort_shall(array, lenght_of_array, show_array);
    merge_sort(array, lenght_of_array, show_array);
    pyramid_sort(array, lenght_of_array, show_array);
    inderect_quick_sort(array, lenght_of_array, show_array);
    std_sort(array, lenght_of_array, show_array);

    
    delete[] array;
    return 0;
}



