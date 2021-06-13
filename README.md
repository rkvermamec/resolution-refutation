# resolution-refutation
### Implement a propositional logic theorem-prover using the resolution-refutation algorithm.


## Input Format: 
From a given file, your program should read the knowledge base and the query statement.
-  The first line contains one integer value, ‘n’, which is the number of formulae 
-  followed by the given formulae in CNF (the Knowledge Base) in the next ‘n’ lines
-  The last line contains the propositional sentence in CNF that needs to be proved (i.e.; the “query”) 

#### Operators: 
We will use the following characters for different operators (remaining operators are not in the scope of this assignment): 
#### OR : | 
#### NOT : ! 

#### Example input file: 
2  
A|B 
!B 
A

The program should implement a resolution refutation proof, and report the result (1 if the KB entails the query, and 0 otherwise). Additionally, the program should print the resolution steps used in the proof (this would also help you in debugging your codes). 
Note that your program should really implement resolution theorem proving, and NOT be specific to any particular KB. 

#### Output Format:
First print the resolution steps (one step per line), and then print the result (integer value 0/1) in the last line
 
#### Some Guidelines: 
(1) When executed, your program should ask for the name of the input file (as an input) in the beginning. 
