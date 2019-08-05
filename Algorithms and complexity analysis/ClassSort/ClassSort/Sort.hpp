//
//  Sort.hpp
//  ClassSort
//
//  Created by Михаил Уляков on 30.03.2018.
//  Copyright © 2018 Михаил Уляков. All rights reserved.
//

#ifndef Sort_hpp
#define Sort_hpp

#include <stdio.h>
#include <iostream>
using namespace std;


class Sort {
public:
    template<typename T>
    static bool check_sort(T *arr, size_t lenght) {
        for(int i = 0; i < lenght - 1; ++i)
            if(arr[i] > arr[i+1]) {
                return false;
            }
        return true;
    }
    
    template<typename T>
    static bool check_sort_indirect(T *arr, size_t *Ind, size_t lenght) {
        for(int i = 0; i < lenght - 1; ++i)
            if(arr[Ind[i]] > arr[Ind[i + 1]]) {
                return false;
            }
        return true;
    }
    
    template <class T>
    static void mergeAB(T *A, int b, int c, int e, T *D)
    {
        int i = b, j = c+1, k;
        for (k = b; k <= e; k++)
            if (j > e) D[k] = A[i++];
            else if (i > c) D[k] = A[j++];
            else if (A[i] <= A[j]) D[k]=A[i++];
            else D[k] = A[j++];
    }
    
    template<typename T>
    static void merge_sort(T *array, int lenght)
    {
        int step, begin, c, e;
        T *buf = new T[lenght];
        for (step = 1; step < lenght; step *= 2) {
            for (begin = 0; begin < lenght; begin += step * 2) {
                c = min(begin + step - 1, lenght - 1);
                e = min(c + step, lenght - 1);
                mergeAB(array, begin, c, e, buf) ;
            }
            for (begin = 0; begin < lenght; begin++) array[begin] = buf[begin];
        }
        delete [] buf;
    }
    
    template<typename T>
    static void printArray(T *arr, size_t size) {
        string output = "";
        for (int i = 0; i < size; i++)
            cout << arr[i] << " ";
        //output += arr[i] + " "; придумай как класть в переменуную и выводить ее один раз, а не обращаться к выводу каждый раз
        cout << output << endl;
    }
    
    
    
    template<typename RandomAccessIterator, typename Compare>
    static void shell_sort(RandomAccessIterator first, RandomAccessIterator last, Compare comp)
    {
        for(typename std::iterator_traits< RandomAccessIterator >::difference_type step = (last - first) / 2; step != 0; step /= 2)
            for(RandomAccessIterator i = first + step; i != last; ++i)
                for(RandomAccessIterator j = i; j - first >= step && comp(*j, *(j - step)); j -= step)
                    std::swap(*j, *(j - step));
    }
    
    template<typename T>
    static void heap_sort(T *array, int lenght)
    {
        int i, m;
        // построение пирамиды
        for (i = lenght/2; i >= 0; i--)
            sift(array, i, lenght-1);
        // сортировка массива
        for (m = lenght-1; m >= 1; m--)
        {
            swap(array[0], array[m]);
            sift(array, 0, m-1);
        }
    }
    
    template<typename T>
    static void sift(T *array, int i, int m)
    {
        int j = i, k = i*2+1;
        while (k <= m) //
        {
            if (k < m && array[k] < array[k+1]) k++;
            if (array[j] < array[k]) {
                swap(array[j], array[k]); j = k; k = k*2+1;
            }
            else break;
        }
    }
    

    
    
    
    
    
    
    template<typename T>
    static void quick_sort(T *array, size_t *ind, int begin, int end) {
        double x;
        int i, j, c = begin, d = end;
        while (c < d) {
            x = array[ind[(c + d) / 2]];
            i = c;
            j = d;
            while (i < j) {
                while (array[ind[i]] < x) i++;
                while (array[ind[j]] > x) j--;
                if (i <= j) {
                    swap(ind[i], ind[j]);
                    i++;
                    j--;
                }
            }
            if (j-c < d-i) {
                if (c < j) {
                    quick_sort(array,ind,c,j);
                }
                c = i;
            } else {
                if (i < d) {
                    quick_sort(array,ind,i,d);
                }
                d = j;
            }
        }
    }
};


#endif /* Sort_hpp */
