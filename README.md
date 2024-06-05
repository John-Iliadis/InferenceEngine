# Inference engine implemented for COS30019 - Intro to AI

Given a knowledge base KB and a query q as input, the program checks if KB entails q using a specified inference algorithm.

The algorithms implemented are:
- Truth table enumeration 
- Forward chaining
- Backward chaining
- Davis–Putnam–Logemann–Loveland

## Example command:
> py iengine.py {filename} {algorithm}

The algorithm can be one of [TT, FC, BC, DPLL].


## Example problem:

Knowledge base: If it's snowing, it is cold. If it's cold, John is wearing a coat. It is snowing.

Query: Is John wearing a coat?

<br>

Propositional symbols:
- **Snowing**: It is snowing.
- **Cold**: It is cold.
- **JC**: John wears a coat.


<br>

Problem file based on the above scenario:
```
TELL
Snowing => Cold;
Cold => JC;
Snowing;

ASK
JC
```
