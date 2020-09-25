import nltk
from nltk import CFG
from nltk.parse import RecursiveDescentParser
import pycountry
import languages_to_use
from languages_to_use import uninstall, language_list
import node_func

class interpreter:

    def check_syntax(text):
# here we list all possible languages that can be used in the grammar        
        lang_pos = {}

        for l in pycountry.languages:
            p = pycountry.languages.get(name=l.name)
            try:
                alpha_kind = p.alpha_2
                lang_pos[p.name]=alpha_kind
            except:
                pass
 
        lang_command = '''LANG ->'''
        for lg in lang_pos:
            if list(lang_pos.keys()).index(lg) == 0:
                lang_command+=' '+str(lang_pos[lg])+' '
            else:
                lang_command+='''| '{x}' '''.format(x=lang_pos[lg])

# here we list all possible functions , given that the system was already re-written to accomodate 
# the changes        
        func_command = '''FUNC ->'''
        for attr in dir(node_func):
            if dir(node_func).index(attr) == 0:
                func_command+=' '+str(attr)+' '
            else:
                func_command+='''| '{x}' '''.format(x=attr)
# here we substitute the pre made rules in the grammar itself

        grammar = CFG.fromstring(('''
            S -> 'plug' '<' FUNC '>' 'as' LANG | 'unplug' '<' LANG '>'
            command1
            command2
            
            '''.replace('command1',lang_command)).replace('command2',func_command))

        grammar_rd = RecursiveDescentParser(grammar)
# here we check the syntax and the lexical using the already described cfg
        for t in text.split('\n'):
            parsed = []
            try:
                for tree in grammar_rd.parse(t.split()):
                    parsed.append(tree)
                
                    if len(parsed) != 0:
                        print(parsed)
                        pass  
                    else:
                        return 'syntax error'

                return 'parsed'
            except:
                return 'syntax/lexical error'

    def run(text):
# here the interpreter will read the commands itself 
        aligned_text = text.split('\n')
        print(aligned_text)
# here we handle all exceptions describe in each function 
        for sentence in aligned_text:
            s = sentence.split()
            try:
                if s[0] == 'plug':
                
                    l = language_list((s[6],s[2]))

                    if l != 'sucessfully plugged':
                        return l 
                    else:
                        pass

                elif s[0] == 'unplug':
                    
                    l = uninstall(s[2])
                    if l != 'sucessfully deplugged node':
                        return l
                    else:
                        pass 
                return 'sucessfully plugged all nodes'
            except IndexError:
                print('expception')
                print(s)

