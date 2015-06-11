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
void test_add(BGV_HE he, string c1, string c2) {
    he.addCtxt(c1, c2, false);
    
    he.decrypt(c1);
    
    he.printTimers();
    he.timersOff();
}

/* destructive sub test */
void test_sub(BGV_HE he, string c1, string c2) {
    he.addCtxt(c1, c2, true);
    
    he.decrypt(c1);
    
    he.printTimers();
    he.timersOff();
}

/* destructive mul test */
void test_mul(BGV_HE he, string c1, string c2) {
    he.multiplyBy(c1, c2);
    
    he.decrypt(c1);

    he.printTimers();
    he.timersOff();
}

/* destructive mulBy2 test */
void test_mul2(BGV_HE he, string c1, string c2) {
    he.multiplyBy2(c1, c2, c2);
    
    he.decrypt(c1);

    he.printTimers();
    he.timersOff();
}

/* square test */
void test_square(BGV_HE he, string c1) {
    he.square(c1);
    
    he.decrypt(c1);

    he.printTimers();
    he.timersOff();
}

/* cube test */
void test_cube(BGV_HE he, string c1) {
    he.cube(c1);
    
    he.decrypt(c1);

    he.printTimers();
    he.timersOff();
}

/* neg test */
void test_neg(BGV_HE he, string c1) {
    he.negate(c1);
    
    he.decrypt(c1);

    he.printTimers();
    he.timersOff();
}

/* eq test */
void test_eq(BGV_HE he, string c1, string c2) {
    he.equalsTo(c1, c2);
    
    he.decrypt(c1);
    he.decrypt(c2);

    he.printTimers();
    he.timersOff();
}

/* rotate test */
void test_rotate(BGV_HE he, string c1, long k) {
    he.rotate(c1, k);
    
    he.decrypt(c1);

    he.printTimers();
    he.timersOff();
}

/* shift test */
void test_shift(BGV_HE he, string c1, long k) {
    he.shift(c1, k);
    
    he.decrypt(c1);

    he.printTimers();
    he.timersOff();
}


/*
 * timing tests
 */
int main(int argc, char** argv) {
    
    if(argc != 2) {
        cout << "which test is to be run must be provided." << endl << flush;
        exit(EXIT_FAILURE);
    }
    
    string test_arg = argv[1];
    
    cout << "/************************************************************/" << endl << flush;
    cout << "BEGINNING BGV_HE " << argv[1] << " TEST" << endl << endl << flush;
    
    /* init random seed */
    srand(time(NULL));
    
    try {
        BGV_HE he;
        
        he.timersOn();
       
        long mod = 65537;
        
        he.keyGen(mod, 1, 15, 2, 64, 0, 128);
        
        long numSlots = he.numSlots();

        vector<long> v1;
        int i;
        for(i = 0; i < numSlots; i++) {
            v1.push_back(rand() % 100000);
        }

        string c1 = he.encrypt(v1); 
        
        
        string c2;
        if(!((test_arg.compare("square") == 0) || 
                (test_arg.compare("cube") == 0) || 
                (test_arg.compare("neg") == 0) ||
                (test_arg.compare("rotate") == 0) ||
                (test_arg.compare("shift") == 0))) {
            vector<long> v2;
            for(i = 0; i < numSlots; i++) {
                v2.push_back(rand() % 100000);
            }
            c2 = he.encrypt(v2);
        }
        
        
        
        if(test_arg.compare("add") == 0) {
            test_add(he, c1, c2);
        } else if (test_arg.compare("sub") == 0) {
            test_sub(he, c1, c2);
        } else if (test_arg.compare("mul") == 0) {
            test_mul(he, c1, c2);
        } else if (test_arg.compare("mul2") == 0) {
            test_mul2(he, c1, c2);
        } else if (test_arg.compare("square") == 0) {
            test_square(he, c1);
        } else if (test_arg.compare("cube") == 0) {
            test_cube(he, c1);
        } else if (test_arg.compare("neg") == 0) {
            test_neg(he, c1);
        } else if (test_arg.compare("eq") == 0) {
            test_eq(he, c1, c2);
        } else if (test_arg.compare("rotate") == 0) {
            test_rotate(he, c1, (((rand() % numSlots) + numSlots) % numSlots));
        } else if (test_arg.compare("shift") == 0) {
            test_shift(he, c1, (((rand() % numSlots) + numSlots) % numSlots));
        } else {
                cout << "improper test option provided." << endl << flush;
                exit(EXIT_FAILURE);
        }      
        
    } catch(exception& e) {
        cout << e.what() << endl << flush;
    }
    
    cout << endl << "BGV_HE " << argv[1] << " TIMING TEST COMPLETE" << endl << flush;
    cout << "/************************************************************/" << endl << cout;

    return 0;
}