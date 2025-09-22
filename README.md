# Elgamal-Voting-Ballot

## Overview
This repository is part of the Excellence Course: "Spotlight on Computer Science Research".\
It aims to explore the intersection of cryptography and civic technology.\
It’s designed to be simple enough to understand, yet powerful enough to showcase real-world cryptographic principles.

## About
Elgamal Voting Ballot is a lightweight Python-based implementation of a secure voting system using ElGamal encryption.\
It demonstrates how cryptographic techniques can be applied to protect voter privacy, ensure vote integrity, and enable verifiable tallying. All without revealing individual choices.

## Project Structure
- Admin.py - Handles election setup, key distribution, and counting of the votes.
- Bulletin Board.py - Acts as a public ledger where encrypted ballots and proofs are posted for transparency.
- Voter.py - Manages voter, ballot creation, and vote encryption using public keys.
- Mixer.py - Shuffles encrypted ballots to anonymize vote origins while preserving their validity.
- Verifier.py - Validates the integrity of ballots and mixing using cryptographic proofs.
- Encryption.py - Implements ElGamal encryption and decryption functions.
- Group.py - Defines the cyclic group class used for secure operations.

```
Elgamal-Voting-Ballot/
├── Admin.py
├── Bulletin Board.py
├── Voter.py
├── Mixer.py
├── Verifier.py
├── Encryption.py
└── Group.py
```
