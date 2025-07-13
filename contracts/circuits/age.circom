pragma circom 2.0.0; 

include "../node_modules/circomlib/circuits/comparators.circom";

template AgeChecker() {
    signal input dobYear;         
    signal input referenceYear;   
    signal input challenge;      

    signal output out;            // 1 if age >= 18, 0 otherwise
    signal output outChallenge;   
    signal output outReferenceYear;

    signal age;
    age <== referenceYear - dobYear;

    component lessThan = LessThan(8);
    lessThan.in[0] <== age;
    lessThan.in[1] <== 18;

    out <== 1 - lessThan.out; 

    outChallenge <== challenge;
    outReferenceYear <== referenceYear;
}

component main = AgeChecker();