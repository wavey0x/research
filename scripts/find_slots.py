from ape import project, chain, accounts, networks
from web3 import Web3, HTTPProvider
from hexbytes import HexBytes
from eth_utils import encode_hex, keccak, to_hex

w3 = Web3(HTTPProvider("http://127.0.0.1:8545"))

def main():
    dev = accounts.test_accounts[0]
    contract = dev.deploy(project.Storage)
    addr = contract.address

    """
    Slot 0:
        uint64 a = 100
        uint64 b = 200
        uint64 c = 300
    """
    slot_num = 0
    slot0 = get_storage_at(addr, slot_num).hex()
    string = slot0[2:]
    size = int(len(string) / 4)
    value1 = w3.toInt(HexBytes(string[size:size*2]))
    value2 = w3.toInt(HexBytes(string[size*2:size*3]))
    value3 = w3.toInt(HexBytes(string[size*3:size*4]))
    print(f'--- SLOT {slot_num} --- ')
    print_slot_data(HexBytes(slot0), ','.join(str(x) for x in [value1, value2, value3]))

    """
    Slot 1:
        uint256 d = 400
    """
    slot_num = 1
    slot1 = get_storage_at(addr, slot_num).hex()
    string = slot1[2:]
    size = int(len(string))
    value1 = w3.toInt(HexBytes(string))
    print(f'--- SLOT {slot_num} --- ')
    print_slot_data(HexBytes(slot1), value1)

    """
    Slot 2:
        address e = 0xFEB4acf3df3cDEA7399794D0869ef76A6EfAff52
    """
    slot_num = 2
    slot2 = get_storage_at(addr, slot_num).hex()
    string = slot2[2:]
    value1 = w3.toChecksumAddress(slot2[len(slot2)-40:])
    print(f'--- SLOT {slot_num} --- ')
    print_slot_data(HexBytes(slot2), value1)

    """
    Slot 3:
         mapping(uint => uint) public exampleMap
    """
    slot_num = 3
    print(f'--- SLOT {slot_num} --- ')
    for i in [0,1,10]:
        encoded_slot_num = HexBytes(w3.toBytes(slot_num).rjust(32,b'\0'))
        encoded_key_num = HexBytes(w3.toBytes(i).rjust(32,b'\0'))
        key = keccak(encoded_key_num + encoded_slot_num)
        slot3 = get_storage_at(addr, key)
        value1 = w3.toInt(slot3)
        print_slot_data(slot3, value1)

    """
    Slot 4:
         mapping(uint => Struct) public structMap
    """
    slot_num = 4
    print(f'--- SLOT {slot_num} --- ')
    for i in [0,1]:
        print(f'checking mapping index {i}')
        for x in [0,1,2,3]: # Offset required to access members
            encoded_slot_num = HexBytes(w3.toBytes(slot_num).rjust(32,b'\0'))
            encoded_key_num = HexBytes(w3.toBytes(i).rjust(32,b'\0'))
            key = keccak(encoded_key_num + encoded_slot_num)
            key_with_offset = HexBytes(int(key.hex(), 16) + x)
            slot4 = get_storage_at(addr, key_with_offset)
            if x == 0:
                value1 = w3.toChecksumAddress(slot4.hex()[len(slot4.hex())-40:])
            elif x == 3:
                value1 = w3.toInt(slot4)
                value1 = value1 == 1
            else:
                value1 = w3.toInt(slot4)
            print_slot_data(slot4, value1)

    """
    Slot 5:
         mapping(uint => Struct) public structMap2
    """
    slot_num = 5
    print(f'--- SLOT {slot_num} --- ')
    for i in [0,1]:
        print(f'checking mapping index {i}')
        for x in [0,1,2,3,4]: # Offset required to access members
            print(f'--> Offset {x}')
            encoded_slot_num = HexBytes(w3.toBytes(slot_num).rjust(32,b'\0'))
            encoded_key_num = HexBytes(w3.toBytes(i).rjust(32,b'\0'))
            key = keccak(encoded_key_num + encoded_slot_num)
            key_with_offset = HexBytes(int(key.hex(), 16) + x)
            slot5 = get_storage_at(addr, key_with_offset)
            # value1 = w3.toChecksumAddress(slot5.hex()[len(slot5.hex())-40:])
            print_slot_data(slot5, slot5.hex())

    """
    Slot 7:
         ExampleStruct[] structArray;

         keccack(p) + i

         where p = declaration appearnce
         where i = slot index from start (not item index, as single item can have multiple slots)
    """
    slot_num = 7
    length = w3.toInt(get_storage_at(addr, slot_num)) # Length is stored at position
    print(f'--- SLOT {slot_num} --- ')
    for i in range(0,8):
        print(f'checking mapping index {i} of array with length {length}')
        print(f'--> Slot {i}')
        encoded_slot_num = HexBytes(w3.toBytes(slot_num).rjust(32,b'\0'))
        # encoded_key_num = HexBytes(w3.toBytes(i).rjust(32,b'\0'))
        key = keccak(encoded_slot_num)
        key_with_offset = HexBytes(int(key.hex(), 16) + i)
        slot7 = get_storage_at(addr, key_with_offset)
        print_slot_data(slot7, slot7.hex())
    print()

    """
    Slot 8:
         ExampleStructPacked[] structArray

         keccack(p) + i

         where p = declaration appearnce
         where i = slot index from start (not item index, as single item can have multiple slots)
    """
    slot_num = 8
    length = w3.toInt(get_storage_at(addr, slot_num)) # Length is stored at position
    print(f'--- SLOT {slot_num} --- ')
    for i in range(0,4):
        print(f'checking mapping index {i} of array with length {length}')
        print(f'--> Slot {i}')
        encoded_slot_num = HexBytes(w3.toBytes(slot_num).rjust(32,b'\0'))
        encoded_key_num = HexBytes(w3.toBytes(i).rjust(32,b'\0'))
        key = keccak(encoded_slot_num)
        key_with_offset = HexBytes(int(key.hex(), 16) + i)
        print(HexBytes(key_with_offset).hex())
        slot8 = get_storage_at(addr, key_with_offset)
        # value1 = w3.toChecksumAddress(slot5.hex()[len(slot5.hex())-40:])
        print_slot_data(slot8, slot8.hex())
        print()

def get_storage_at(contract, slot):
    return networks.provider.get_storage_at(contract, slot)

def print_slot_data(slot_data, string):
    print(f'Slot Data: {slot_data.hex()}')
    print(f'Value: {string}')


