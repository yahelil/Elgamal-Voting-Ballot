# ElGamal Cryptographic Voting Simulator

## Overview

This project presents a secure and verifiable electronic ballot system, built in Python, leveraging **ElGamal encryption** and **Zero-Knowledge Proofs (ZKP)**. It demonstrates core cryptographic principles required for modern digital voting—namely, confidentiality, integrity, and public verifiability.

## Features

- **End-to-End Voter Privacy**: Each vote is encrypted individually using ElGamal.
- **Ballot Integrity**: The system prevents vote tampering via cryptographically verifiable proofs.
- **Zero-Knowledge Proofs**: Ensure correct ballot mixing and tallying without revealing actual votes.
- **Open Verification**: Anyone can verify the election process using public proofs.
- **Modular Python Codebase**: Extensible design with Python modules for encryption, proof, and mixing.

## Architecture

- `Admin.py`: Sets up election parameters and manages trusted authorities.
- `Voter.py`: Handles vote encryption and ZKP generation for voter legitimacy.
- `Mixer.py`: Performs ballot shuffling ("mixnet") with reencryption and ZKP for shuffle integrity.
- `Verifier.py`: Verifies cryptographic proofs for proper mixing and tallying.
- `BulletinBoard.py`: Acts as a public ledger for ballots and proofs.
- `Encryption.py`, `Group.py`: Core cryptographic primitives and group mathematics.

## How It Works

1. **Election Initialization**: Admin defines group parameters for ElGamal and sets up public keys.
2. **Vote Casting**: Voters encrypt their choices individually with ElGamal, submitting ZKPs for validity.
3. **Ballot Mixing**: Ballots undergo mixnet shuffling for anonymity, with shuffle ZKPs.
4. **Verification**: Anyone can audit the ballot mixing and vote tally by checking the generated proofs.
5. **Tallying**: Final result is decrypted and revealed using collaborative keys.

## Installation & Usage

1. Clone the repository:
    ```
    git clone https://github.com/yahelil/Elgamal-Voting-Ballot.git
    cd Elgamal-Voting-Ballot
    ```
2. Install dependencies if required (see any requirements.txt or project docs).
3. Run modules according to election workflow. (See example admin, voting, and verification scripts in the repo.)

## Demonstration

https://github.com/user-attachments/assets/cefa687d-b42e-4ef9-b8e9-de0a4f131c3f



## Contributors

- Yaheli Levit
- Guy Nevo
- Simon Levy
- Eden Sokolov Gulko
- Shira Abuddi

## Documentation

See included PDF and DOCX files for:
- Theoretical background on ElGamal and ZKP
- Implementation notes
- MIT course summary

## License

MIT License. See LICENSE file for details.

## References

- [ElGamal Encryption (Wikipedia)](https://en.wikipedia.org/wiki/ElGamal_encryption)
- [Zero-Knowledge Proofs (Wikipedia)](https://en.wikipedia.org/wiki/Zero-knowledge_proof)

---

*Creating an honest ballot using ElGamal encryption and Zero-Knowledge Proofs for research and educational purposes.*

