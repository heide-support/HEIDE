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

#include "BGV_HE.h"

using namespace std;

BGV_HE::BGV_HE() {
}

BGV_HE::~BGV_HE() {
}

/* -------------------------------------------------------------------------- */

void BGV_HE::keyGen(long p, long r, long L, long c, 
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

string BGV_HE::encrypt(vector<long> ptxt_vect) {   
    Ctxt ctxt(*publicKey, 0);
    
    ea->encrypt(ctxt, *publicKey, ptxt_vect);
    
    return store(&ctxt);
}

vector<long> BGV_HE::decrypt(string key) { 
    vector<long> ret_vect;
    
    ea->decrypt(ctxt_unord_map.at(key), *secretKey, ret_vect);
    
    return ret_vect;
}

/* -------------------------------------------------------------------------- */

string BGV_HE::set(string key) {
    Ctxt ctxt = ctxt_unord_map.at(key);
    
    return store(&ctxt);
}

void BGV_HE::addCtxt(string key, string other_key, bool negative) {
    ctxt_unord_map.at(key).addCtxt(ctxt_unord_map.at(other_key), negative);
}

void BGV_HE::multiplyBy(string key, string other_key) {
    ctxt_unord_map.at(key).multiplyBy(ctxt_unord_map.at(other_key));
}

void BGV_HE::multiplyBy2(   string key, 
                                    string other_key1, 
                                    string other_key2) {
    ctxt_unord_map.at(key).multiplyBy2( ctxt_unord_map.at(other_key1), 
                                        ctxt_unord_map.at(other_key2));
}
void BGV_HE::square(string key) {
    ctxt_unord_map.at(key).square();
}
void BGV_HE::cube(string key) {
    ctxt_unord_map.at(key).cube();
}

void BGV_HE::negate(string key) {
    ctxt_unord_map.at(key).negate();
}

bool BGV_HE::equalsTo(string key, string other_key, bool comparePkeys) {
    return ctxt_unord_map.at(key).equalsTo( ctxt_unord_map.at(other_key), 
                                            comparePkeys);
}

void BGV_HE::rotate(string key, long k) {
    ea->rotate(ctxt_unord_map.at(key), k);
}

void BGV_HE::shift(string key, long k) {
    ea->shift(ctxt_unord_map.at(key), k);
}

/* -------------------------------------------------------------------------- */

long BGV_HE::numSlots() {
    return ea->size();
}

void BGV_HE::replace(string key, Ctxt new_ctxt) {
    boost::unordered_map<string, Ctxt>::const_iterator got = ctxt_unord_map.find(key);
    if(got != ctxt_unord_map.end()) {
        ctxt_unord_map.at(key) = new_ctxt;
    }
}

Ctxt BGV_HE::retrieve(string key) {
    return ctxt_unord_map.at(key);
}

string BGV_HE::store(Ctxt* ctxt) {
    struct timeval tp;
    gettimeofday(&tp, NULL);
    long int ms = tp.tv_sec * 1000 + tp.tv_usec / 1000;
    string key = boost::lexical_cast<string>(ms);
    
    ctxt_unord_map.insert(make_pair(key, *ctxt));
    
    return key;
}

void BGV_HE::erase(string key) {
    if(ctxt_unord_map.find(key) != ctxt_unord_map.end()) {
        ctxt_unord_map.erase(key);
    }
}

/* -------------------------------------------------------------------------- */

void BGV_HE::timersOn() {
    setTimersOn();
}

void BGV_HE::timersOff() {
    setTimersOff();
}

void BGV_HE::resetTimers() {
    resetAllTimers();
}


void BGV_HE::printTimers() {
    printAllTimers(cout);
}

/* -------------------------------------------------------------------------- */

