#Graph Theory Project - Brendan Toolan - G00350190

#Shunter Algorithm
def shunterAlgorithm(infix):
    #special characters and the order they are in
    specialChar = {'*':50, '.':40, '|':30}
    #output
    postFix = ""
    #stack for the operators
    stack = ""

    #for loop 
    for x in infix:
        # pushs an open bracket to the stack
        if x == '(':
            stack = stack + x
        # pops from the stack and pushs to output when theres a closing bracket
        elif x == ')':
            while stack[-1] != '(':
                postFix, stack = postFix + stack[-1], stack[:-1]
            stack = stack[:-1]
        # pushes to the stack after poping lower/equal order
        # top of stack then gets added to the output
        elif x in specialChar:
            while stack and specialChar.get(x,0) <= specialChar.get(stack[-1], 0):
                postFix, stack = postFix + stack[-1], stack[:-1]
            stack = stack + x
        #Puts any normal characters, (i.e.'a','b' etc) into the output
        else:
            postFix = postFix + x
    #pops leftover operators from the stack to output
    while stack:
        postFix, stack = postFix + stack[-1], stack[:-1]

    #returns postFix Expression
    return postFix

#Thompson Constructor

#state with arrows that are labelled
class state:
    label = None
    edge1 = None
    edge2 = None

#nfa represented by initial and accept states
class nfa:
    initial = None
    accept = None

    #consturctor for nfa
    def __init__(self, initial, accept):
        self.initial = initial
        self.accept = accept

#compile function
def compile(postFix):
    #stores the nfa instances
    nfastack =[]

    #for loop
    for x in postFix:
        #if statement
        if x == '.':
            #pops the first two nfa off stack
            nfa2 = nfastack.pop()
            nfa1 = nfastack.pop()
            #connects first nfa accept to the second nfa inital  
            nfa1.accept.edge1 = nfa2.initial
            #pushes nfa to stack 
            nfastack.append(nfa(nfa1.initial, nfa2.accept))

        elif x == '|':
            #pops the first two nfa off stack
            nfa2 = nfastack.pop()
            nfa1 = nfastack.pop()
            #makes a initial state and connects to the iniital state of nfas popped from stack
            initial = state()
            initial.edge1 = nfa1.initial
            initial.edge2 = nfa2.initial

            #makes an accept state and connects to the accept state of nfas popped from stack
            accept = state()
            nfa1.accept.edge1 = accept
            nfa2.accept.edge1 = accept
            #pushes new nfa to the stack
            nfastack.append(nfa(initial, accept))

        elif x == '*':
            #pops single nfa from the stack
            nfa1 = nfastack.pop()
            #new initial and accept states created
            initial = state()
            accept = state()
            #connects new initial state to new accept state and nfa1 initial state
            initial.edge1 = nfa1.initial
            initial.edge2 = accept
            #connects old accept to new accept state and nfa1 initial state
            nfa1.accept.edge1= nfa1.initial
            nfa1.accept.edge2 = accept
             #pushes new nfa to stack
            nfastack.append(nfa(initial, accept))

        else:
            #creates a new accept and initial state
            accept = state()
            initial = state()
            #connects accept state and initial state together with x label arrow
            initial.label = x
            initial.edge1 = accept
            #pushes nfa to stack
            nfastack.append(nfa(initial, accept))
    #returns output
    return nfastack.pop()
    
#Matching Expressions

#return set of states that can be reached from state  
def follows(state):
    
    states = set()
    states.add(state)
    
    #sees if state has arrows that are labelled
    if state.label is None:
        if state.edge1 is not None:
            states |= follows(state.edge1)
        if state.edge2 is not None:
            states |= follows(state.edge2)
    
    #returns set of states
    return states

#match function: takes infix regular expression and sees if
# it matches the string
def match(infix, string):
    #complie and shunt the expression
    postFix = shunterAlgorithm(infix)
    nfa = compile(postFix)

    #current and next set of states created
    currentState = set()
    nextState = set()


    currentState |= follows(nfa.initial)
     #for loop for characters in the string
    for x in string:
        #inner for loop for set of states currently
        for y in currentState:
            #checks for state labelled x
            if y.label == x:
                #adds edge1 to set
                nextState |= follows(y.edge1)
                
        currentState = nextState
        nextState = set()
    #print(postFix)
    return (nfa.accept in currentState) 

#tests
infix = ["a.b.c*", "a.(b|d).c*", "(a.(b|d))*", "a.(b.b)*.c"]
string = ["", "abc", "abbc","abcc","abad", "abbbc"]
#i is the infix, v is the string
for i in infix:
    for v in string:
        #print true/false
        print(match(i,v),i,v)

print()
#Lets the user input expression
expression = input("Enter Exprssion: ")
#prints out expression entered
print(expression)
#below line converts the expression to postFix
postFix = shunterAlgorithm(expression)
print("Post Fix Expression: "+postFix)
#Turns the postFix into a NFA and stores it
print(compile(postFix))
#print()
#Prints out Thompson
#print(compile("ab.cd.|"))
#print(compile("ab*.c*d.|"))
#print(compile("aa.*"))  
#print(compile("a*b."))  

#print()
#Prints out Shunter
#print(shunterAlgorithm("(a.b)|(c*.d)"))
#print(shunterAlgorithm("(a*.b*)|(a.b*)"))
#print(shunterAlgorithm("(a|b).(c*.d*)|(c|d*)"))
#print(shunterAlgorithm("(a*b*)|(a.b).(c*|d)"))