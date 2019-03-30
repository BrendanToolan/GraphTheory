#Graph Theory Project - Brendan Toolan - G00350190

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
            initial.ege2 = nfa2.initial

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
    
print(compile("ab.cd.|"))
print(compile("aa.*"))

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

print(shunter("(a.b)|(c*.d)"))