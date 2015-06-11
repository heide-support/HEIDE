//    Copyright (C) 2015  Grant Frame
//
//    This program is free software: you can redistribute it and/or modify
//    it under the terms of the GNU General Public License as published by
//    the Free Software Foundation, either version 3 of the License, or
//    (at your option) any later version.
//
//    This program is distributed in the hope that it will be useful,
//    but WITHOUT ANY WARRANTY; without even the implied warranty of
//    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
//    GNU General Public License for more details.
//
//    You should have received a copy of the GNU General Public License
//    along with this program.  If not, see <http://www.gnu.org/licenses/>.

#include <cstdlib>
#include <iostream>
#include <time.h>
#include <boost/format.hpp>
#include <string>

#include "BGV_HE.h"

using namespace std;

/* destructive add test */
void test_add(BGV_HE he, long numSlots, vector<long> v1, vector<long> v2, 
        long mod, string c1, string c2) {
    
    string test_str = "testing destructive add ... ";
    cout << test_str << flush;
    
    int i;
    vector<long> p_add;
    for(i = 0; i < numSlots; i++) {
        p_add.push_back((((v1[i] + v2[i]) % mod) + mod) % mod);
    }

    string c_add = he.set(c1);
    he.addCtxt(c_add, c2, false);

    vector<long> decrypt_c_add = he.decrypt(c_add);

    for(i = 0; i < numSlots; i++) {
        if(decrypt_c_add[i] != p_add[i]) {
            cout << '\r' << boost::format("%1%%|55t|%2%\n") % test_str % "FAILED.";
            exit(EXIT_FAILURE);
        }
    }

    if(i == numSlots) {
        cout << '\r' << boost::format("%1%%|55t|%2%\n") % test_str % "PASSED.";
    }
}

/* destructive sub test */
void test_sub(BGV_HE he, long numSlots, vector<long> v1, vector<long> v2, 
        long mod, string c1, string c2) {
    
    string test_str = "testing destructive sub ... "; 
    cout <<  test_str << flush;
    
    int i;
    vector<long> p_sub;
    for(i = 0; i < numSlots; i++) {
        p_sub.push_back((((v1[i] - v2[i]) % mod + mod) % mod));
    }

    string c_sub = he.set(c1);
    he.addCtxt(c_sub, c2, true);

    vector<long> decrypt_c_sub = he.decrypt(c_sub);

    for(i = 0; i < numSlots; i++) {
        if(decrypt_c_sub[i] != p_sub[i]) {
            cout << '\r' << boost::format("%1%%|55t|%2%\n") % test_str % "FAILED.";
            cout << p_sub << endl << flush;
            cout << decrypt_c_sub << endl << flush;
            exit(EXIT_FAILURE);
        }
    }

    if(i == numSlots) {
        cout << '\r' << boost::format("%1%%|55t|%2%\n") % test_str % "PASSED.";
    }
}

/* destructive mul test */
void test_mul(BGV_HE he, long numSlots, vector<long> v1, vector<long> v2, 
        long mod, string c1, string c2) {
    
    string test_str = "testing destructive mul ... ";
    cout << test_str << flush;
    
    int i;
    vector<long> p_mul;
    for(i = 0; i < numSlots; i++) {
        p_mul.push_back((((v1[i] * v2[i]) % mod + mod) % mod));
    }

    string c_mul = he.set(c1);
    he.multiplyBy(c_mul, c2);

    vector<long> decrypt_c_mul = he.decrypt(c_mul);

    for(i = 0; i < numSlots; i++) {
        if(decrypt_c_mul[i] != p_mul[i]) {
            cout << '\r' << boost::format("%1%%|55t|%2%\n") % test_str % "FAILED.";
            exit(EXIT_FAILURE);
        }
    }

    if(i == numSlots) {
        cout << '\r' << boost::format("%1%%|55t|%2%\n") % test_str % "PASSED.";
    }
}

/* destructive mulBy2 test */
void test_mul2(BGV_HE he, long numSlots, vector<long> v1, vector<long> v2, 
        long mod, string c1, string c2) {
    
    string test_str = "testing destructive mulBy2 ... ";
    cout << test_str << flush;
    
    int i;
    vector<long> p_mul2;
    for(i = 0; i < numSlots; i++) {
        p_mul2.push_back((((v1[i] * v2[i] * v2[i]) % mod + mod) % mod));
    }

    string c_mul2 = he.set(c1);
    he.multiplyBy2(c_mul2, c2, c2);

    vector<long> decrypt_c_mul2 = he.decrypt(c_mul2);

    for(i = 0; i < numSlots; i++) {
        if(decrypt_c_mul2[i] != p_mul2[i]) {
            cout << '\r' << boost::format("%1%%|55t|%2%\n") % test_str % "FAILED.";
            exit(EXIT_FAILURE);
        }
    }

    if(i == numSlots) {
        cout << '\r' << boost::format("%1%%|55t|%2%\n") % test_str % "PASSED.";
    }
}

/* square test */
void test_square(BGV_HE he, long numSlots, vector<long> v1, long mod, string c1) {
    
    string test_str = "testing square ... ";
    cout << test_str << flush;
    
    int i;
    vector<long> p_square;
    for(i = 0; i < numSlots; i++) {
        p_square.push_back((((v1[i] * v1[i]) % mod + mod) % mod));
    }

    string c_square = he.set(c1);
    he.square(c_square);

    vector<long> decrypt_c_square = he.decrypt(c_square);

    for(i = 0; i < numSlots; i++) {
        if(decrypt_c_square[i] != p_square[i]) {
            cout << '\r' << boost::format("%1%%|55t|%2%\n") % test_str % "FAILED.";
            exit(EXIT_FAILURE);
        }
    }

    if(i == numSlots) {
        cout << '\r' << boost::format("%1%%|55t|%2%\n") % test_str % "PASSED.";
    }
}

/* cube test */
void test_cube(BGV_HE he, long numSlots, vector<long> v1, long mod, string c1) {
    
    string test_str = "testing cube ... "; 
    cout << test_str << flush;
    
    int i;
    vector<long> p_cube;
    for(i = 0; i < numSlots; i++) {
        p_cube.push_back((((v1[i] * v1[i] * v1[i]) % mod + mod) % mod));
    }

    string c_cube = he.set(c1);
    he.cube(c_cube);

    vector<long> decrypt_c_cube = he.decrypt(c_cube);

    for(i = 0; i < numSlots; i++) {
        if(decrypt_c_cube[i] != p_cube[i]) {
            cout << '\r' << boost::format("%1%%|55t|%2%\n") % test_str % "FAILED.";
            exit(EXIT_FAILURE);
        }
    }

    if(i == numSlots) {
        cout << '\r' << boost::format("%1%%|55t|%2%\n") % test_str % "PASSED.";
    }
}

/* neg test */
void test_neg(BGV_HE he, long numSlots, vector<long> v1, long mod, string c1) {
    
    
    string test_str = "testing neg ... ";
    cout << test_str << flush;
    
    int i;
    vector<long> p_neg;
    for(i = 0; i < numSlots; i++) {
        p_neg.push_back((((-1 * v1[i]) % mod + mod) % mod));
    }

    string c_neg = he.set(c1);
    he.negate(c_neg);

    vector<long> decrypt_c_neg = he.decrypt(c_neg);

    for(i = 0; i < numSlots; i++) {
        if(decrypt_c_neg[i] != p_neg[i]) {
            cout << '\r' << boost::format("%1%%|55t|%2%\n") % test_str % "FAILED.";
            exit(EXIT_FAILURE);
        }
    }

    if(i == numSlots) {
        cout << '\r' << boost::format("%1%%|55t|%2%\n") % test_str % "PASSED.";
    }
}

/* eq test */
void test_eq(BGV_HE he, long numSlots, vector<long> v1, vector<long> v2, 
        string c1, string c2) {
    
    string test_str = "testing eq ... ";
    cout << test_str << flush;
    
    int i;
    bool p_eq = true;
    for(i = 0; i < numSlots; i++) {
        if(v1[i] != v2[i]) {
            p_eq = false;
            break;
        }
    }

    bool decrypt_c_eq = he.equalsTo(c1, c2);

    if(decrypt_c_eq != p_eq) {
        cout << '\r' << boost::format("%1%%|55t|%2%\n") % test_str % "FAILED.";
    } else{
        cout << '\r' << boost::format("%1%%|55t|%2%\n") % test_str % "PASSED.";
    }
}

/* rotate test */
void test_rotate(BGV_HE he, long numSlots, vector<long> v1, long mod, 
        string c1, long k) {
    
    string test_str = "testing rotate ... ";
    cout << test_str << flush;
    
    int i;
    vector<long> p_rotate;
    for (i = 0; i < numSlots; i++) {
        p_rotate.push_back(v1[i] % mod);
    }
    rotate(p_rotate.rbegin(), p_rotate.rbegin() + k, p_rotate.rend());

    string c_rotate = he.set(c1);
    he.rotate(c_rotate, k);

    vector<long> decrypt_c_rotate = he.decrypt(c_rotate);

    for(i = 0; i < numSlots; i++) {
        if(decrypt_c_rotate[i] != p_rotate[i]) {
            cout << '\r' << boost::format("%1%%|55t|%2%\n") % test_str % "FAILED.";
            exit(EXIT_FAILURE);
        }
    }

    if(i == numSlots) {
        cout << '\r' << boost::format("%1%%|55t|%2%\n") % test_str % "PASSED.";
    }
}

/* shift test */
void test_shift(BGV_HE he, long numSlots, vector<long> v1, long mod, 
        string c1, long k) {
    
    string test_str = "testing shift ... ";
    cout << test_str << flush;
    
    int i;
    vector<long> p_shift;
    for(i = 0; i < numSlots; i++) {
        p_shift.push_back(v1[i] % mod);
    }
    rotate(p_shift.rbegin(), p_shift.rbegin() + k, p_shift.rend());
    for(i = 0; i < k; i++) {
        p_shift[i] = 0;
    }

    string c_shift = he.set(c1);
    he.shift(c_shift, k);

    vector<long> decrypt_c_shift = he.decrypt(c_shift);

    for(i = 0; i < numSlots; i++) {
        if(decrypt_c_shift[i] != p_shift[i]) {
            cout << '\r' << boost::format("%1%%|55t|%2%\n") % test_str % "FAILED.";
            exit(EXIT_FAILURE);
        }
    }

    if(i == numSlots) {
        cout << '\r' << boost::format("%1%%|55t|%2%\n") % test_str % "PASSED.";
    }
}


/*
 * validation tests
 */
int main(int argc, char** argv) {
    
    cout << "/************************************************************/" << endl << flush;
    cout << "BEGINNING VALIDATION TESTS" << endl << endl << flush;
    
    /* init random seed */
    srand(time(NULL));
    
    try {
        BGV_HE he;
       
        long mod = 65537;
        
        cout << "generating keys ... " << flush;
        
        he.keyGen(mod, 1, 15, 2, 64, 0, 128);
        
        cout << '\r' << boost::format("generating keys ... %|53t|%1%\n\n") 
                % "FINISHED.";
        
        long numSlots = he.numSlots();

        vector<long> v1;
        int i;
        for(i = 0; i < numSlots; i++) {
            v1.push_back(rand() % 100000);
        }

        string c1 = he.encrypt(v1); 
        
        vector<long> v2;
        for(i = 0; i < numSlots; i++) {
            v2.push_back(rand() % 100000);
        }
        string c2 = he.encrypt(v2);
        
        test_add(he, numSlots, v1, v2, mod, c1, c2);
        test_sub(he, numSlots, v1, v2, mod, c1, c2);
        test_mul(he, numSlots, v1, v2, mod, c1, c2);
        test_mul2(he, numSlots, v1, v2, mod, c1, c2);
        test_square(he, numSlots, v1, mod, c1);
        test_cube(he, numSlots, v1, mod, c1);
        test_neg(he, numSlots, v1, mod, c1);
        test_eq(he, numSlots, v1, v2, c1, c2);
        test_rotate(he, numSlots, v1, mod, c1, 
                (((rand() % numSlots) + numSlots) % numSlots));
        test_shift(he, numSlots, v1, mod, c1, 
                (((rand() % numSlots) + numSlots) % numSlots));
        
        
    } catch(exception& e) {
        cout << e.what() << endl << flush;
    }
    
    cout << endl << "VALIDATION TESTS COMPLETE" << endl << flush;
    cout << "/************************************************************/" << endl << cout;

    return 0;
}

