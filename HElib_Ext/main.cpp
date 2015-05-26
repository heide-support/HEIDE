#include <cstdlib>
#include <iostream>

#include "HElib_Ext.h"

using namespace std;

/*
 * 
 */
int main(int argc, char** argv) {
    
    try {
        HElib_Ext he;
        
        he.timersOn();
        
        he.keyGen(65537, 1, 15, 2, 64, 0, 128);

        vector<long> v1;
        int i;
        for(i = 0; i < he.numSlots(); i++) {
            v1.push_back(i);
        }

        string c1 = he.encrypt(v1); 
        
        vector<long> v2;
        for(i = 0; i < he.numSlots(); i++) {
            v2.push_back(i);
        }
        string c2 = he.encrypt(v2);
        
        c1 += c2;

        vector<long> ret_vect = he.decrypt(c1);
        
        he.timersOff();
        he.printTimers();
        
        for(i = 0; i < he.numSlots(); i++) {
            cout << ret_vect[i] << endl << flush;
        }
        
    } catch(exception& e) {
        cout << e.what() << endl << flush;
    }

    return 0;
}

