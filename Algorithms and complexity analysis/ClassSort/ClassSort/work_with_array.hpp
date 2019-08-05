//
//  work_with_array.hpp
//  ClassSort
//
//  Created by Михаил Уляков on 30.03.2018.
//  Copyright © 2018 Михаил Уляков. All rights reserved.
//

#ifndef work_with_array_hpp
#define work_with_array_hpp

#include <stdio.h>
#include <ctime>
#include <string>
#include <iostream>
#include "Sort.hpp"
using namespace std;

template<typename T>
void generate_int_array(T *arr, size_t n, int typeArr = 1, int left = 0, int right = 200);
int pars_input_to_int();

template<typename T>
void inderect_sort_shall(T *arr, int length, bool debug) {
    int *array_for_shall = new int[length];
    size_t *array_for_shall_ind = new size_t[length];
    generate_int_array(array_for_shall_ind, length, 4);
    copy(arr, arr+ length,array_for_shall);
    if (debug) { cout << "Given array is:" << endl; Sort::printArray(array_for_shall, length); }
    /*--------------------------*/
    /***********/
    if (Sort::check_sort(array_for_shall, length)) cout << "Array is sorted!" << endl;
    else  cout << "Array isn't sorted ;C" << endl;
    /***********/
    size_t start_time = clock();
    //Sort::shell_sort(array_for_shall, lenght_of_array);
    //Sort::shell_sort(array_for_shall, array_for_shall_Ind, lenght_of_array);
    Sort::shell_sort(array_for_shall_ind, array_for_shall_ind + length, [array_for_shall](size_t ind1, size_t ind2) { return array_for_shall[ind1] < array_for_shall[ind2]; });
    size_t end_time = clock();
    double search_time = end_time - start_time; // искомое время в тиках процессора
    //if (debug) { cout << "Sorted array is: " << endl; Sort::printArray(array_for_shall, lenght_of_array); }
    if (debug) { cout << "Sorted Ind is: " << endl; Sort::printArray(array_for_shall_ind, length); }
    /***********/
    if (Sort::check_sort_indirect(array_for_shall, array_for_shall_ind, length)) cout << "Indirect array is sorted!" << endl;
    else  cout << "Indirect array isn't sorted ;C" << endl;
    /***********/
    cout << "Shall_sort time is: \033[1;4m" << search_time / CLOCKS_PER_SEC << "\033[0m" << endl;
    cout << '}' << endl;
    delete[] array_for_shall;
    delete[] array_for_shall_ind;
}

template<typename T>
void merge_sort(T* arr, int lenght, bool debug) {
    int *array_for_merge = new int[lenght];
    copy(arr, arr + lenght, array_for_merge);
    cout << endl << '{' << "\033[1;20m--Merge--\033[0m" << endl;
    /*-----------PRINT ARRAY---------------*/
    if (debug) { cout << "Given array is:" << endl; Sort::printArray(array_for_merge, lenght); }
    /*--------------------------*/
    /***********/
    if (Sort::check_sort(array_for_merge, lenght)) cout << "Array is sorted!" << endl;
    else  cout << "Array isn't sorted ;C" << endl;
    /***********/
    size_t start_time = clock();
    Sort::merge_sort(array_for_merge, lenght);
    //Sort::merge_sort(array_for_merge, array_for_merge + lenght_of_array);
    size_t end_time = clock();
    double search_time = end_time - start_time;
    if (debug) { cout <<"Sorted array is:" << endl; Sort::printArray(array_for_merge, lenght); }
    /***********/
    if (Sort::check_sort(array_for_merge, lenght)) cout << "Array is sorted!" << endl;
    else  cout << "Array isn't sort ;C" << endl;
    /***********/
    cout << "Merge_sort time is: \033[1;4m" <<  search_time / CLOCKS_PER_SEC << "\033[0m" << endl;
    cout << '}' << endl;
    delete[] array_for_merge;
}

template<typename T>
void pyramid_sort(T* arr, size_t length, bool debug) {
    int *array_for_pyramid = new int[length];
    copy(arr, arr + length, array_for_pyramid);
    cout << endl << '{' << "\033[1;20m--Pyramid--\033[0m" << endl;
    if (debug) { cout << "Given array is:" << endl; Sort::printArray(array_for_pyramid, length); }
    /*--------------------------*/
    /***********/
    if (Sort::check_sort(array_for_pyramid, length)) cout << "Array is sorted!" << endl;
    else  cout << "Array isn't sort ;C" << endl;
    /***********/
    size_t start_time = clock();
    Sort::heap_sort(array_for_pyramid, (unsigned int)length);
    size_t end_time = clock();
    double search_time = end_time - start_time;
    if (debug) { cout <<"Sorted array is:" << endl; Sort::printArray(array_for_pyramid, length); }
    /***********/
    if (Sort::check_sort(array_for_pyramid, length)) cout << "Array is sorted!" << endl;
    else  cout << "Array isn't sort ;C" << endl;
    /***********/
    cout << "Heap_sort time is: \033[1;4m" << search_time / CLOCKS_PER_SEC << "\033[0m" << endl;
    cout << '}' << endl;
    delete[] array_for_pyramid;
}

template<typename T>
void inderect_quick_sort(T *arr, size_t length, bool debug) {
    int *array_for_quick_sort = new int[length];
    size_t *array_for_quick_sort_ind = new size_t[length];
    generate_int_array(array_for_quick_sort_ind, length, 4);
    cout << endl << '{' << "\033[1;20m--Inderect_Quick_Sort--\033[0m" << endl;
    if (debug) { cout << "Given array is:" << endl; Sort::printArray(array_for_quick_sort, length); }
    /***********/
    if (Sort::check_sort(array_for_quick_sort, length)) cout << "Array is sorted!" << endl;
    else  cout << "Array isn't sort ;C" << endl;
    /***********/
    size_t start_time = clock();
    Sort::quick_sort(array_for_quick_sort, array_for_quick_sort_ind, 0, (int)length - 1);
    size_t end_time = clock();
    double search_time = end_time - start_time;
    //if (debug) { cout <<"Sorted array is:" << endl; Sort::printArray(array_for_merge, lenght_of_array); }
    if (debug) { cout << "Sorted Ind is: " << endl; Sort::printArray(array_for_quick_sort_ind, length); }
    /***********/
    if (Sort::check_sort_indirect(array_for_quick_sort, array_for_quick_sort_ind, length)) cout << "Indirect array is sorted!" << endl;
    else  cout << "Indirect array isn't sorted ;C" << endl;
    /***********/
    cout << "Quick_sort time is: \033[1;4m" << search_time / CLOCKS_PER_SEC << "\033[0m" << endl;
    cout << '}' << endl;
    delete[] array_for_quick_sort;
    delete[] array_for_quick_sort_ind;
}

template<typename T>
void std_sort(T *arr, size_t lenght, bool debug) {
    int *array_for_std_sort = new int[lenght];
    copy(arr, arr + lenght, array_for_std_sort);
    cout << endl << '{' << "\033[1;20m--STD::SORT--\033[0m" << endl;
    if (debug) { cout << "Given array is:" << endl; Sort::printArray(array_for_std_sort, lenght); }
    /*--------------------------*/
    /***********/
    if (Sort::check_sort(array_for_std_sort, lenght)) cout << "Array is sorted!" << endl;
    else  cout << "Array isn't sort ;C" << endl;
    /***********/
    size_t start_time = clock();
    std::sort(array_for_std_sort, array_for_std_sort + lenght);
    size_t end_time = clock();
    double search_time = end_time - start_time;
    if (debug) { cout <<"Sorted array is:" << endl; Sort::printArray(array_for_std_sort, lenght); }
    /***********/
    if (Sort::check_sort(array_for_std_sort, lenght)) cout << "Array is sorted!" << endl;
    else  cout << "Array isn't sort ;C" << endl;
    /***********/
    cout << "STD::SORT time is: \033[1;4m" << search_time / CLOCKS_PER_SEC << "\033[0m" << endl;
    cout << '}' << endl;
    delete[] array_for_std_sort;
}


template<typename T>
void generate_int_array(T *arr, size_t n, int typeArr, int left, int right) {
    enum array_type {random = 1, ascending = 2, descendingly = 3, ordered = 4};
    if (typeArr == array_type::random) {
        for (int i = 0; i < n; i++) arr[i] = left + rand() % right;
    } else if (typeArr == array_type::ascending) {
        for (int i = 0; i < n; i++) arr[i] = left + rand() % right;
        std::sort(arr, arr + n);
    } else if (typeArr == array_type::descendingly) {
        for (int i = 0; i < n; i++) arr[i] = left + rand() % right;
        std::sort(arr, arr + n);
        std::reverse(arr, arr + n);
    } else if (typeArr == array_type::ordered) {
        for(int i = 0; i < n; i++) arr[i] = i;
    }
}

#endif /* work_with_array_hpp */
