#ifndef BGV_HE_H
#define	BGV_HE_H

#include <fstream>
#include <sstream>
#include <cstdlib>
#include <boost/unordered_map.hpp>
#include <boost/lexical_cast.hpp>
#include <sys/time.h>
#include <string.h>

#include <FHE.h>
#include <EncryptedArray.h>
#include <PAlgebra.h>

class BGV_HE {
public:
    BGV_HE();
    virtual ~BGV_HE();
    
    /**
     * @brief Performs Key Generation using HElib functions
     * @param p plaintext base
     * @param r lifting 
     * @param L # of levels in modulus chain
     * @param c # of columns in key switching matrix
     * @param w Hamming weight of secret key
     * @param d degree of field extension
     * @param security security parameter
     * @param m (optional parameter) use m'th cyclotomic polynomial
     * @param gens (optional parameter) vector of generators
     * @param ords (optional parameter) vector of orders
     */
    void keyGen(long p, long r, long L, long c, 
                    long w, long d, long security, long m = -1,
                    const vector<long>& gens = vector<long>(), 
                    const vector<long>& ords = vector<long>());
    /**
     * @brief Calls HElib encrypt function for provided plaintext vector and
     * then stores the ciphertext in the unordered map and returns the key
     * @param ptxt_vect plaintext vector to encrypt
     * @return key where ciphertext stored in unordered map
     */
    string encrypt(vector<long> ptxt_vect);
    /**
     * @brief Calls HElib decrypt function for ciphertext that is found in
     * unordered map at key
     * @param key the key which corresponds to the ciphertext to decrypt
     * @return the decrypted ciphertext
     */
    vector<long> decrypt(string key);
    
    /**
     * @brief Create a new ciphertext and set it equal to the ciphertext 
     * stored in unordered map under key
     * @param key ciphertext key in unordered map
     * @return key corresponding to new ciphertext
     */
    string set(string key);
    /**
     * @brief Add ciphertext at key to ciphertext at other_key and store result
     * back in unordered map at key
     * @param key key in unordered map
     * @param other_key key in unordered map
     * @param negative if True then perform subtraction
     */
    void addCtxt(string key, string other_key, bool negative);
    /**
     * @breif Multiply ciphertext at key by ciphertext at other_key and store
     * result in unordered map at key
     * @param key key in unordered map
     * @param other_key key in unordered map
     */
    void multiplyBy(string key, string other_key);
    /**
     * @brief Multiply ciphertext at key by ciphertext at other_key1 and 
     * other_key2
     * @param key key in unordered map
     * @param other_key1 key in unordered map
     * @param other_key2 key in unordered map
     */
    void multiplyBy2(string key, string other_key1, string other_key2);
    /**
     * @brief Square ciphertext at key
     * @param key key in unordered map
     */
    void square(string key);
    /**
     * @brief Cube ciphertext at key
     * @param key key in unordered map
     */
    void cube(string key);
    /**
     * @brief Multiply ciphertext at key by -1
     * @param key
     */
    void negate(string key);
    /**
     * @brief Return true if the ciphertext at key and ciphertext at other_key
     * are equal
     * @param key key in unordered map
     * @param other_key key in unordered map
     * @param comparePkeys if true then pkeys will be compared
     * @return True if ciphertexts are equal
     */
    bool equalsTo(string key, string other_key, bool comparePkeys=true);
    /**
     * @brief Rotate ciphertext at key by k spaces
     * @param key key in unordered map
     * @param k number of spaces to rotate by
     */
    void rotate(string key, long k);
    /**
     * @brief Shift ciphertext at key by k spaces
     * @param key key in unordered map 
     * @param k number of spaces to shift by
     */
    void shift(string key, long k);
    
    /**
     * @brief Number of plaintext slots 
     * @return number of plaintext slots
     */
    long numSlots();
    /**
     * @brief Retrieve the ciphertext object from the unordered map
     * @param key key in unordered map
     * @return the ciphertext corresponding to the passed in key
     */
    Ctxt retrieve(string key);
    /**
     * Replace the ciphertext at key with the new one provided
     * @param key key in unordered map
     * @param new_ctxt new Ctxt object to store in the unordered map
     */
    void replace(string key, Ctxt new_ctxt);
    /**
     * @brief Delete from the unordered map the entry at key
     * @param key key in unordered map
     */
    void erase(string key);
    
    /**
     * @brief Call HElib timers on method
     */
    void timersOn();
    /**
     * @brief Call HElib timers off method
     */
    void timersOff();
    /**
     * @brief Call HElib timers reset method
     */
    void resetTimers();
    /**
     * @brief Call HElib timers print method 
     */
    void printTimers();
private:
    EncryptedArray* ea;
    FHEcontext* context;
    FHESecKey* secretKey;
    const FHEPubKey* publicKey;
    
    /**
     * Unordered map which stores the ciphertexts
     */
    boost::unordered_map<string, Ctxt> ctxt_unord_map;
    
    /**
     * @brief Store the ciphertext in the unordered map and return key where 
     * it was stored
     * @param ctxt Ciphertext to store in unordered map
     * @return the key used to locate this ciphertext in the unordered map
     */
    string store(Ctxt* ctxt);
};

#endif	/* BGV_HE_H */

