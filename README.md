# #D (hashD)
A fully decentralized broadcast system for the based on gossip and proof of work

Original Paper https://hashd.in/hashd-in-draft0/


## PoC - ethDenver

- [ ] PoW hashing Alorithm SHA256 - moving to coocko cycle
- [ ] Merkle Tree hash SHA256 - moving to blake2b or keccak
- [ ] Signatures ECDSA secp256k1 - if there is a working BLS implementation we should move to that


### CLI API

Prefix commands with `python`, i.e., `python hashd init`

- [ ] hashd init - implemented
  - Create new block with prevBlk = 0
  - Create two new keys
    - hot key
    - cold key output as a mnemonic
- [ ] hashd addWork blkSig - adds proof of work to a block signature - implemented
- [ ] hashd hashBench - benchmark and show lowest hash after 1,10,100 seconds - implemented
- [ ] hashd set -v 10 "Message" "tag1,tag2" image.jpg - partially implemented
- [ ] hashd get -v 10 type="value"
- [ ] hashd config threshold (forward|store-headers|store-broadcast|store-data)
- [ ] hashd verify KEY - block info
- [ ] hashd explore - p2p search


### Message Types
| message | Contents | Size | Compute| Forward Rules | description|
|---------|----------|------|--------|---------------|------------|
|nonceRelay  | BlkSig + nonce | 80b | 1 hash| does the hash verify & meet threshold| Relay additional PoW|
|headerRelay | nonceRelay + header| 80b+100b| 1 signature| does signature verify| Relay new blockheaders|
|bCastRelay  | headerRelay + hash[A:B] + type + value| 180b+64b+128b| 4 hashes| do all the hashes verify | Add new k,v to database|
|authRelay   | bCastRelay + Auth Script + hashes| 372b+ script size| more hashes and script validation| do all the hashes verify & script is well formed| set new consensus rules for chain|
|dataRelay   | bCastRelay + data + hashes |372b+merkle tree & leaves| n hashes for n data verfification |verify hashes|  Store data of another node's block|

```                                                                            Bytes        Name
                  PoW Hash                      | 1 comparison             | 32 |    |    | Broadcast Hash
                     |                          |                          | sig|nonc|    |
        Block Signature || nonce                | 1 hash verification      | 32 | 16 |    |
               |                                |                          |root|Psig|Pkey|
(Op(4b)||Merkle Root||PrevBlkSig)sign+(pub-key) | 1 signature verification | 32 | 32 | 64 | Blockheader + 4bytes for bit tag field
            /     \                             | 1 hash verification      |    |    |    |
           /       \                            |                          |    |    |    |
          /         \                           |                          |    |    |    |
         /           \                          |                          |    |    |    |
      hashA         hashB(root of block data)   | 1 hash verification(A)   | 32 | 32 |    | hashA tree - Broadcast Tree
      /   \         /   \                       |                          |    |    |    | hashB tree - Data Tree
     /     \                                    |                          |    |    |    |
    /       \                                   |                          |    |    |    |
 hashC     hashD                                | 2 hash verifications(C,D)| 32 | 32 |    |
   |         |                                  |                          |    |    |    |
 type      value                                | 2 data fields            | 64 | 64 |    |
```

| OP Value | Type | Value | Description|
|----------|-----|-------|------------|
| 0        |No broadcast| 0|0|NA|
| 1        |Key Replacement| [current key, hash(cold key)] | Declares the new replacement key and the current key|
| 2        |Well Known| String| This would be a name the chain/id want's to be know by|
| 3        |Service Endpoint| JSON object | containing protocol and address tuples of supported endpoints |  
| 4        |Schema| JSON {opVal:Ttype}| the last schema for a chain supercedes eariler ones on the same opval |
| 5        |Tweet| [hashtag1,hashtag2...]| Simple tweet data type, message data is in the data side of the merkle tree|
