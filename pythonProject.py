#Graph Theory Project - Brendan Toolan - G00350190

def shunter(infix):
    specialChar = {'*':50, '.':40, '|':30}
    postFix = ""
    stack = ""

    for x in infix:
        if x == '(':
            stack = stack + x
        elif x == ')':
            while stack[-1] != '(':
                postFix, stack = postFix + stack[-1], stack[:-1]
            stack = stack[:-1]
        elif x in specialChar:
            while stack and specialChar.get(x,0) <= specialChar.get(stack[-1], 0):
                postFix, stack = postFix + stack[-1], stack[:-1]
            stack = stack + x
        
        else:
            postFix = postFix + x
    
    while stack:
        postFix, stack = postFix + stack[-1], stack[:-1]

    return postFix
#Thompson Constructor
class state:
    label = None
    edge1 = None
    edge2 = None

class nfa:
    initial = None
    accept = None

    def __init__(self, initial, accept):
        self.initial = initial
        self.accept = accept

def compile(postFix):
    nfastack =[]

    for x in postFix:
        if x == '.':
            nfa2 = nfastack.pop()
            nfa1 = nfastack.pop()
            nfa1.accept.edge1 = nfa2.initial
                    
            nfastack.append(nfa(nfa1.initial, nfa2.accept))


        elif x == '|':
            nfa2 = nfastack.pop()
            nfa1 = nfastack.pop()
           
            initial = state()
            initial.edge1 = nfa1.initial
            initial.edge2 = nfa2.initial

            accept = state()
            nfa1.accept.edge1 = accept
            nfa2.accept.edge1 = accept
           
            nfastack.append(nfa(initial, accept))


        elif x == '*':
            nfa1 = nfastack.pop()
            initial = state()
            accept = state()
            initial.edge1 = nfa1.initial
            initial.edge2 = accept
            nfa1.accept.edge1= nfa1.initial
            nfa1.accept.edge2 = accept
            nfastack.append(nfa(initial, accept))


        else:
            accept = state()
            initial = state()
            initial.label = x
            initial.edge1 = accept
            nfastack.append(nfa(initial, accept))

    return nfastack.pop()
    
def follows(state):
    states = set()
    states.add(state)

    if state.label is None:
        if state.edge1 is not None:
            states |= follows(state.edge1)
        if state.edge2 is not None:
            states |= follows(state.edge2)

    return states

def match(infix, string):
    postFix = shunter(infix)
    nfa = compile(postFix)

    currentState = set()
    nextState = set()

    currentState |= follows(nfa.initial)

    for x in string:
        for y in currentState:
            if y.label == x:
                nextState |= follows(y.edge1)
                
        currentState = nextState
        nextState = set()

    return (nfa.accept in currentState) 

infix = ["a.b.c*", "a.(b|d).c*", "(a.(b|d))*", "a.(b.b)*.c"]
string = ["", "abc", "abbc","abcc","abad", "abbbc"]

for i in infix:
    for v in string:
        print(match(i,v),i,v)

#print(compile("ab.cd.|"))
#print(compile("aa.*"))  
#print(shunter("(a.b)|(c*.d)"))