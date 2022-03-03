# Rock, Paper, Scissors

1. We have 3 parties
    * Do we need 3 TOZNY clients?
        * Probably
    1. Clarence
    2. Alicia
    3. Bruce


## Alicia
* Can submit a move
    * Must be encrypted. 
    * Only decrypted by:
        * Clarence
        * Alicia
## Bruce
* Can submit a move
    * Must be encrypted.
    * Only decrypted by:
        * Clarence
        * __ALICIA__
            * Do we not want Bruce to review their move after submission?
## Clarence
* Can decrypt 
* Can declare winner
    * Must be encrypted.
    * Only decrypted by:
        * Alicia
        * Bruce
---
## Solution
* Going w/ one program for all 3 parties
    * Using params passed to dictate behavior
* Use `1` client class ? 
    * All 3 classes inherit from it
* look into features provided by `e3db` SDK
--- 
## Resources
[1]- [Tonzy's Python SDK](https://github.com/tozny/e3db-python/)

[2]- [Tozny Dashboard](https://dashboard.tozny.com/register)