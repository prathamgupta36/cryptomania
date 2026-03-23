## CBC-MAC with Random IV

This challenge shows why CBC-MAC should not use a random or attacker-controlled IV. You are given a valid message, IV, and tag, along with a required replacement for the first block.

Your task is to compute a new IV so that the modified message still verifies under the original tag.
