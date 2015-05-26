#include <string.h>

#include "HElib_Ext.h"

using namespace std;

HElib_Ext::HElib_Ext() {
}

HElib_Ext::~HElib_Ext() {
}

/* -------------------------------------------------------------------------- */

void HElib_Ext::keyGen(long p, long r, long L, long c, 
        long w, long d, long security, long m,  
        const vector<long>& gens, const vector<long>& ords) {
    
    ZZX G;
    if(m == -1) {
        m = FindM(security, L, c, p, d, 0, 0);
    }
    
    // initialize context
    context = new FHEcontext(m, p, r, gens, ords); 
    
    // modify the context, adding primes to the modulus chain
    buildModChain(*context, L, c);
    
    // construct a secret key structure
    secretKey = new FHESecKey(*context); 
    
    // an "upcast": FHESecKey is a subclass of FHEPubKey
    publicKey = secretKey; 
    
    if(d == 0) {
        G = context->alMod.getFactorsOverZZ()[0];
    } else {
        G = makeIrredPoly(p, d);
    }

    // actually generate a secret key with Hamming weight w
    secretKey->GenSecKey(w); 

    addSome1DMatrices(*secretKey);
    
    // construct an Encrypted array object ea that is
    // associated with the given context and the polynomial G
    ea = new EncryptedArray(*context, G);
   
}

string HElib_Ext::encrypt(vector<long> ptxt_vect) {   
    Ctxt ctxt(*publicKey, 0);
    
    ea->encrypt(ctxt, *publicKey, ptxt_vect);
    
    return store(&ctxt);
}

vector<long> HElib_Ext::decrypt(string key) { 
    vector<long> ret_vect;
    
    ea->decrypt(ctxt_unord_map.at(key), *secretKey, ret_vect);
    
    return ret_vect;
}

/* -------------------------------------------------------------------------- */

string HElib_Ext::set(string key) {
    Ctxt ctxt = ctxt_unord_map.at(key);
    
    return store(&ctxt);
}

void HElib_Ext::addCtxt(string key, string other_key, bool negative) {
    ctxt_unord_map.at(key).addCtxt(ctxt_unord_map.at(other_key), negative);
}

void HElib_Ext::multiplyBy(string key, string other_key) {
    ctxt_unord_map.at(key).multiplyBy(ctxt_unord_map.at(other_key));
}

void HElib_Ext::multiplyBy2(   string key, 
                                    string other_key1, 
                                    string other_key2) {
    ctxt_unord_map.at(key).multiplyBy2( ctxt_unord_map.at(other_key1), 
                                        ctxt_unord_map.at(other_key2));
}
void HElib_Ext::square(string key) {
    ctxt_unord_map.at(key).square();
}
void HElib_Ext::cube(string key) {
    ctxt_unord_map.at(key).cube();
}

void HElib_Ext::negate(string key) {
    ctxt_unord_map.at(key).negate();
}

bool HElib_Ext::equalsTo(  string key, 
                                string other_key, 
                                bool comparePkeys) {
    return ctxt_unord_map.at(key).equalsTo( ctxt_unord_map.at(other_key), 
                                            comparePkeys);
}

void HElib_Ext::rotate(string key, long k) {
    ea->rotate(ctxt_unord_map.at(key), k);
}

void HElib_Ext::shift(string key, long k) {
    ea->shift(ctxt_unord_map.at(key), k);
}

/* -------------------------------------------------------------------------- */

long HElib_Ext::numSlots() {
    return ea->size();
}

string HElib_Ext::store(Ctxt* ctxt) {
    struct timeval tp;
    gettimeofday(&tp, NULL);
    long int ms = tp.tv_sec * 1000 + tp.tv_usec / 1000;
    string key = boost::lexical_cast<string>(ms);
    
    ctxt_unord_map.insert(make_pair(key, *ctxt));
    
    return key;
}

void HElib_Ext::erase(string key) {
    if(ctxt_unord_map.find(key) != ctxt_unord_map.end()) {
        ctxt_unord_map.erase(key);
    }
}

/* -------------------------------------------------------------------------- */

void HElib_Ext::timersOn() {
    setTimersOn();
}

void HElib_Ext::timersOff() {
    setTimersOff();
}

void HElib_Ext::resetTimers() {
    resetAllTimers();
}


void HElib_Ext::printTimers() {
    printAllTimers(cout);
}

/* -------------------------------------------------------------------------- */

