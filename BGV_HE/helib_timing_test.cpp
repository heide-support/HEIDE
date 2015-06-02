#include <cstdlib>
#include <iostream>
#include <time.h>
#include <boost/format.hpp>
#include <string>

#include <FHE.h>
#include <EncryptedArray.h>
#include <PAlgebra.h>

using namespace std;

/* destructive add test */
void test_add(EncryptedArray ea, FHESecKey secretKey, Ctxt c1, Ctxt c2) {
    c1.addCtxt(c2, false);
    
    vector<long> ptxt;
    ea.decrypt(c1, secretKey, ptxt);
    
    printAllTimers(cout);
    setTimersOff();
}

/* destructive sub test */
void test_sub(EncryptedArray ea, FHESecKey secretKey, Ctxt c1, Ctxt c2) {
    c1.addCtxt(c2, true);
    
    vector<long> ptxt;
    ea.decrypt(c1, secretKey, ptxt);
    
    printAllTimers(cout);
    setTimersOff();
}

/* destructive mul test */
void test_mul(EncryptedArray ea, FHESecKey secretKey, Ctxt c1, Ctxt c2) {
    c1.multiplyBy(c2);
    
    vector<long> ptxt;
    ea.decrypt(c1, secretKey, ptxt);

    printAllTimers(cout);
    setTimersOff();
}

/* destructive mulBy2 test */
void test_mul2(EncryptedArray ea, FHESecKey secretKey, Ctxt c1, Ctxt c2) {
    c1.multiplyBy2(c2, c2);
    
    vector<long> ptxt;
    ea.decrypt(c1, secretKey, ptxt);

    printAllTimers(cout);
    setTimersOff();
}

/* square test */
void test_square(EncryptedArray ea, FHESecKey secretKey, Ctxt c1) {
    c1.square();
    
    vector<long> ptxt;
    ea.decrypt(c1, secretKey, ptxt);

    printAllTimers(cout);
    setTimersOff();
}

/* cube test */
void test_cube(EncryptedArray ea, FHESecKey secretKey, Ctxt c1) {
    c1.cube();
    
    vector<long> ptxt;
    ea.decrypt(c1, secretKey, ptxt);

    printAllTimers(cout);
    setTimersOff();
}

/* neg test */
void test_neg(EncryptedArray ea, FHESecKey secretKey, Ctxt c1) {
    c1.negate();
    
    vector<long> ptxt;
    ea.decrypt(c1, secretKey, ptxt);

    printAllTimers(cout);
    setTimersOff();
}

/* eq test */
void test_eq(EncryptedArray ea, FHESecKey secretKey, Ctxt c1, Ctxt c2) {
    c1.equalsTo(c2);
    
    vector<long> ptxt1;
    ea.decrypt(c1, secretKey, ptxt1);
    
    vector<long> ptxt2;
    ea.decrypt(c2, secretKey, ptxt2);
    

    printAllTimers(cout);
    setTimersOff();
}

/* rotate test */
void test_rotate(EncryptedArray ea, FHESecKey secretKey, Ctxt c1, long k) {
    ea.rotate(c1, k);
    
    vector<long> ptxt;
    ea.decrypt(c1, secretKey, ptxt);

    printAllTimers(cout);
    setTimersOff();
}

/* shift test */
void test_shift(EncryptedArray ea, FHESecKey secretKey, Ctxt c1, long k) {
    ea.shift(c1, k);
    
    vector<long> ptxt;
    ea.decrypt(c1, secretKey, ptxt);

    printAllTimers(cout);
    setTimersOff();
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
    cout << "BEGINNING HELIB " << argv[1] << " TEST" << endl << endl << flush;
    
    /* init random seed */
    srand(time(NULL));
    
    try {
        setTimersOn();
       
        long p = 65537;
        long r = 1;
        long L = 15;
        long c = 2; 
        long w = 64; 
        long d = 0;
        long m = -1;
        long security = 128;
        
        ZZX G;
    
        if(m == -1) {
            m = FindM(security, L, c, p, d, 0, 0);
        }

        // initialize context
        FHEcontext context(m, p, r); 

        // modify the context, adding primes to the modulus chain
        buildModChain(context, L, c);

        // construct a secret key structure
        FHESecKey secretKey(context); 

        // an "upcast": FHESecKey is a subclass of FHEPubKey
        const FHEPubKey& publicKey = secretKey; 

        if(d == 0) {
            G = context.alMod.getFactorsOverZZ()[0];
        } else {
            G = makeIrredPoly(p, d);
        }

        // actually generate a secret key with Hamming weight w
        secretKey.GenSecKey(w); 

        addSome1DMatrices(secretKey);

        // construct an Encrypted array object ea that is
        // associated with the given context and the polynomial G
        EncryptedArray ea(context, G);
        
        long numSlots = ea.size();
        
        vector<long> v1;
        int i;
        for(i = 0; i < numSlots; i++) {
            v1.push_back(rand() % 100000);
        }
            
        Ctxt c1(publicKey);
        ea.encrypt(c1, publicKey, v1); 
        
        Ctxt c2(publicKey);
        if(!((test_arg.compare("square") == 0) || 
                (test_arg.compare("cube") == 0) || 
                (test_arg.compare("neg") == 0) ||
                (test_arg.compare("rotate") == 0) ||
                (test_arg.compare("shift") == 0))) {
            vector<long> v2;
            for(i = 0; i < numSlots; i++) {
                v2.push_back(rand() % 100000);
            }
            ea.encrypt(c2, publicKey, v2);
        }
        
        if(test_arg.compare("add") == 0) {
            test_add(ea, secretKey, c1, c2);
        } else if (test_arg.compare("sub") == 0) {
            test_sub(ea, secretKey, c1, c2);
        } else if (test_arg.compare("mul") == 0) {
            test_mul(ea, secretKey, c1, c2);
        } else if (test_arg.compare("mul2") == 0) {
            test_mul2(ea, secretKey, c1, c2);
        } else if (test_arg.compare("square") == 0) {
            test_square(ea, secretKey, c1);
        } else if (test_arg.compare("cube") == 0) {
            test_cube(ea, secretKey, c1);
        } else if (test_arg.compare("neg") == 0) {
            test_neg(ea, secretKey, c1);
        } else if (test_arg.compare("eq") == 0) {
            test_eq(ea, secretKey, c1, c2);
        } else if (test_arg.compare("rotate") == 0) {
            test_rotate(ea, secretKey, c1, (((rand() % numSlots) + numSlots) % numSlots));
        } else if (test_arg.compare("shift") == 0) {
            test_shift(ea, secretKey, c1, (((rand() % numSlots) + numSlots) % numSlots));
        } else {
                cout << "improper test option provided." << endl << flush;
                exit(EXIT_FAILURE);
        }      
        
    } catch(exception& e) {
        cout << e.what() << endl << flush;
    }
    
    cout << endl << "HELIB " << argv[1] << " TIMING TEST COMPLETE" << endl << flush;
    cout << "/************************************************************/" << endl << cout;

    return 0;
}