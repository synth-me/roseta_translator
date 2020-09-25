# roseta_translator
Real time translation system with a package manager to control the language's dialect you're using  

The main feature of roseta is the possibility to modify an json file containing paths to certain language nodes. Each language node is designed to improve the quality
of the translation for each language. 
The default nodes are japanese, korean and chinese. They are main used to romanize the text after translation , which makes the synthtizer works better.
The nodes can be used to store language's variation whitin an range, for example : you can have Portuguese from Portugal and Portuguese from Brazil in the same node, an then using the commands you can switch between them for a better translation depending upon the person you're talking to.

Nodes are storage in the file 'node_func', to add a node(which have to be written in the file node_func) you just need to open the node_shell and type 'plug < x > as < y >' 
where x is the function's name and y the language's alpha 2 code as an example : plug < korean_node > as < ko >. To disconnect : unplug < ko >
To make a good node and functional one you need to follow the same pattern as the default ones, with input as a native's language and output as target's language. 
We recommend you studying about tokenization, romanization and dialects to make your own nodes. We strongly support iniciatives to include minoritary languages in the system with their nodes, just pull request us.     

I hope you can contribute to the software, i do really think diversity is one of main weak points of today's automatic translation system. 
