# Elgamal-Voting-Ballot

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#overview">Overview</a></li>
    <li><a href="#about">About</a></li>
    <li><a href="#project-structure">Project Structure</a></li>
    <li>
      <details>
        <summary><a href="#how-to-run-the-project">How to Run the Project</a></summary>
        <ul>
            <li><a href="#start-the-bulletin-board">Start the Bulletin Board</a></li>
            <li><a href="#launch-the-admin">Launch the Admin</a></li>
            <li><a href="#cast-votes">Cast Votes</a></li>
            <li><a href="#run-a-mixer">Run a Mixer</a></li>
            <li><a href="#run-a-verifier-optional-between-mixers">Run a Verifier</a></li>
            <li><a href="#final-verification-optional">Final Verification</a></li>
            <li><a href="#view-the-final-ballot">View the Final Ballot</a></li>
        </ul>
      </details>
    </li>
    <li><a href="#the-project-in-real-life ">The Project in Real Life </a></li>
  </ol>
</details>


## Overview
This repository is part of the Excellence Course: "Spotlight on Computer Science Research".\
It aims to explore the intersection of cryptography and civic technology.\
It’s designed to be simple enough to understand, yet powerful enough to showcase real-world cryptographic principles.

## About
Elgamal Voting Ballot is a lightweight Python-based implementation of a secure voting system simulator using ElGamal encryption.\
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

## How to Run the Project

This guide walks you through the full voting process—from setup to final tally—using the ElGamal Voting Ballot system.

### Start the Bulletin Board
This acts as the public channel for sharing encrypted votes and proofs.
```bash
python BulletinBoard.py
```
You should see:
```bash
Server is running. Waiting for admin...
```
### Launch the Admin
The admin initializes the election and sends cryptographic keys to the bulletin board.

```bash
python Admin.py
```
Expected output:
```
Keys sent.
```

### Cast Votes
Each voter runs the voting script and submits their encrypted vote.

```bash
python Voter.py
```
You’ll be prompted:
```
Cast your vote (Simon, Eden, Guy, Shira, Yaheli):
```

You can vote using full names or shortcuts:
- si → Simon
- e → Eden
- g → Guy
- sh → Shira
- y → Yaheli
  
After voting:
```
Vote sent.
```


### Run a Mixer
Once voting is complete, you can mix the ballots using mixers.
```bash
python Mixer.py
```
You’ll be asked:
```
Mixer x
Cheat? (y or n)
```
- If you choose n, the mixer will shuffle votes truthfully
    
- If you choose y, you’ll input two replacement votes. This simulates tampering for educational purposes.

If it's the fifth mixer, this will be displayed:
```
No more mixes.
```
Else:
```
Done mixing.
```
### Run a Verifier (Optional, Between Mixers)
Between the mixers use verifier to make sure all mixers were honest.

```bash
python Verifier.py
```
- If no cheating occurred:
  ```
  Verifying x mixers...
  
  Mixers verified: True
  ```
- If cheating is detected: (for example mixer 1 and 3 cheated)
  ```
  Verifying x mixers...
  
  Mixer 1 cheated
  Mixer 3 cheated
  Mixers verified: False
  ```
The verifier will notify the bulletin board of the first cheating mixer. You’ll see:
```
Beware a mixer cheated!!!
Want to overrule him? (y/n)
```
- If you choose y, all mixes after the cheating one are discarded.
- You can run up to five mixers total, overruling removes mixers allowing for more mixers to connect

### Final Verification (Optional)
After five mixers, the bulletin board will ask:
```
Verify one last time? (y/n)
```
- If yes, run Verifier.py again.
- If no, proceed to the final tally

### View the Final Ballot
Return to the admin to see the results:
```
Counting the votes...
(Vote 1)
(Vote 2)
Simon votes: X
Eden votes: Y
Guy votes: Z
Shira votes: W
Yaheli votes: V
Winner is: [Name(s)]
```
- The first and second votes reflect the final mixed order.
- If there’s a tie, multiple winners will be listed.

## The Project in Real Life 

