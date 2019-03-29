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