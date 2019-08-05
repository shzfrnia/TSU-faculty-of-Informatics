//
//  work_with_array.cpp
//  ClassSort
//
//  Created by Михаил Уляков on 30.03.2018.
//  Copyright © 2018 Михаил Уляков. All rights reserved.
//

#include "work_with_array.hpp"



int pars_input_to_int() {
    size_t n = 500;
    char *text = new char[n];
    string s;
    getline(cin,s);
    if (s.length() > n) throw std::logic_error("Owerflow");
    for(int i = 0, j = 0; i < s.length(); i++) {
        if (isdigit(s[i])) {
            text[j] = s[i];
            j++;
        }
    }
    int result = atoi(text);
    delete [] text;
    return result;
}


