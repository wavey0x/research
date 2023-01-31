// SPDX-License-Identifier: GPL-3.0

pragma solidity >=0.7.0 <0.9.0;

/**
 * @title Storage
 * @dev Sample contract used to work with storage slots
 */

contract Storage {
    
    // This struct features no packing. Each member takes up a full slot.
    struct ExampleStruct {
        address user;
        uint startTime;
        uint endTime;
        bool isActive;
    }

    // This struct features packing. All members are packed into single slot.
    struct ExampleStructPacked {
        uint32 startTime;
        uint32 endTime;
        bool isActive;
        address user;
    }

    uint64 a = 100; // slot:0
    uint64 b = 200; // slot:0
    uint64 c = 300; // slot:0
    uint d = 400;   // slot:1
    address e = 0xFEB4acf3df3cDEA7399794D0869ef76A6EfAff52; // slot:2

    mapping(uint => uint) public exampleMap;                // slot:3
    mapping(uint => ExampleStruct) public structMap;        // slot:4
    mapping(uint => ExampleStructPacked) public structMap2; // slot:5
    
    address[] exampleArray;             // slot:6
    ExampleStruct[] structArray;        // slot:7
    ExampleStructPacked[] structArray2; // slot:8

    constructor() {
        exampleMap[0] = 1;
        exampleMap[1] = 2;
        exampleMap[10] = 3;

        exampleArray.push(0xFEB4acf3df3cDEA7399794D0869ef76A6EfAff52);

        _setupPackedStructs();
        _setupUnpackedStructs();
    }

    function _setupUnpackedStructs() internal {
        ExampleStruct memory s = ExampleStruct(
            0xFEB4acf3df3cDEA7399794D0869ef76A6EfAff52, // User
            1,      // startTime
            2,      // endTime
            true    // isActive
        );

        structMap[0] = s;
        structArray.push(s);

        s.isActive = false;
        s.startTime = 3;
        s.endTime = 4;
        
        structMap[1] = s;
        structArray.push(s);
    }

    function _setupPackedStructs() internal {
        ExampleStructPacked memory s = ExampleStructPacked(
            1,      // startTime
            2,      // endTime
            true,   // isActive
            0xFEB4acf3df3cDEA7399794D0869ef76A6EfAff52 // User
        );

        structMap2[0] = s;
        structArray2.push(s);

        s.isActive = false;
        s.startTime = 3;
        s.endTime = 4;
        
        structMap2[1] = s;
        structArray2.push(s);
    }
}