#Graph Theory Project - Brendan Toolan - G00350190

class state:
    label = None
    edge1 = None
    edge2 = None

class nfa:
    initial = None
    accept = None

    def _init_(self, initial, accept):
        self.initial = initial
        self.accept = accept

def compile(pointFix):
    nfastack =[]

    for x in pointFix:
        if x == '.':
            nfa2 = nfastack.pop()
            nfa1 = nfastack.pop()
            nfa1.accept.edge1 = nfa2.initial
            newnfa =  nfa(nfa1.initial, nfa2.accept)
            nfastack.append(newnfa)

        elif x == '|':
            nfa2 = nfastack.pop()
            nfa1 = nfastack.pop()
           
            initial = state()
            initial.edge1 = nfa1.initial
            initial.ege2 = nfa2.initial

            accept = state()
            nfa1.accept.edge1 = accept
            nfa2.accept.edge1 = accept
           
            newnfa =  nfa(nfa1.initial, nfa2.accept)
            nfastack.append(newnfa)

        elif x == '*':
            nfa1 = nfastack.pop()
            initial = state()
            accept = state()
            initial.edge1 = nfa1.initial
            initial.edge2 = accept
            nfa1.accept.edge1= nfa1.initial
            nfa1.accept.edge2 = accept
            newnfa =  nfa(nfa1.initial, nfa2.accept)
            nfastack.append(newnfa)

        else:
            accept = state()
            initial = state()
            initial.label = x
            initial.edge1 = accept
            newnfa =  nfa(nfa1.initial, nfa2.accept)
            nfastack.append(newnfa)

    return nfastack.pop()
    
#print(compile("ab.cd.|"))
#print(compile("aa.*"))

def shunter(infix):
    specialChar = {'*':50, '.':40, '|':30}
    pointFix = ""
    stack = ""

    for x in infix:
        if x == '(':
            stack = stack + x
        elif x == ')':
            while stack[-1] != '(':
                pointFix, stack = pointFix + stack[-1], stack[:-1]
            stack = stack[:-1]
        elif x in specialChar:
            while stack and specialChar.get(x,0) <= specialChar.get(stack[-1], 0):
                pointFix, stack = pointFix + stack[-1], stack[:-1]
            stack = stack + x
        
        else:
            pointFix = pointFix + x
    
    while stack:
        pointFix, stack = pointFix + stack[-1], stack[:-1]

    return pointFix

print(shunter("(a.b)|(c*.d)"))