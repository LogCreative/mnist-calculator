import math

ADD     = 10        # +
MINUS   = 11        # -
MUL     = 12        # ×
DIV     = 13        # ÷
LP      = 14        # (
RP      = 15        # )
END     = 16        # \0

def getDisplay(results):
    displayText = ""
    for literal in results:
        if literal == ADD:
            displayText += "+"
        elif literal == MINUS:
            displayText += "-"
        elif literal == MUL:
            displayText += "×"
        elif literal == DIV:
            displayText += "÷"
        elif literal == LP:
            displayText += "("
        elif literal == RP:
            displayText += ")"
        else:
            displayText += str(literal)
    displayText += "="
    return displayText

def operate(op1, op2, op):
    if op == ADD:
        return op1 + op2
    elif op == MINUS:
        return op1 - op2
    elif op == MUL:
        return op1 * op2
    elif op == DIV:
        if op2 == 0:
            return math.inf
        else:
            return op1 / op2

def makeCalculation(results):
    # conflicting naming scheme bans
    # the use of postfix method.
    results.append(END)  # add an ending symbol
    numStack = []
    opStack = []
    curnum = 0
    for i, literal in enumerate(results):
        if literal < 10: # single number
            curnum = curnum * 10 + literal
        else: # operator
            if literal == LP:
                if i>0 and results[i-1] < 10:
                    numStack.append(curnum)
                    curnum = 0
                    opStack.append(MUL) # handle 2(3) -> 2 * (3)
                opStack.append(literal)
            else:
                # push the current num
                if literal != END:
                    numStack.append(curnum)
                    curnum = 0
                # 2 + (12 + 2 * 3 + 1)
                if len(opStack) == 0:
                    opStack.append(literal)
                    continue
                while len(opStack)>0:
                    topOp = opStack[-1]
                    if literal == RP and topOp == LP:
                        topOp = opStack.pop()
                        break
                    if (topOp - literal >= -1 and topOp != LP) or literal == RP or literal == END:
                        # topOp is of higher priority or the same priority
                        # or it meets RP or END to collapse
                        # make calculation now
                        topOp = opStack.pop()
                        try: 
                            op2 = numStack.pop()
                            op1 = numStack.pop()
                        except:
                            return "ERROR"
                        numStack.append(operate(op1, op2, topOp))
                    else:
                        # topOp is of lower priority
                        # push the literal
                        opStack.append(literal)
                        break
                    if len(opStack)==0 and literal == RP:
                        # the ) doesn't match (
                        return "ERROR"
    return numStack.pop()

def calc(results):
    displayText = getDisplay(results)
    displayText += str(makeCalculation(results))
    return displayText