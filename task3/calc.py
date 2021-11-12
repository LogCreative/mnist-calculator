# -*- coding:gbk -*-

import math

ADD     = 10        # +
MINUS   = 11        # -
MUL     = 12        # ×
DIV     = 13        # ÷
LP      = 14        # (
RP      = 15        # )

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

def getPostfix(results):
    # translate to postfix expression.
    postfix = []
    postStack = []
    for literal in results:
        if literal < 10:
            postfix.append(literal)
        elif literal == LP:
            postStack.append(literal)
        elif literal == RP:
            while len(postStack)>0:
                top = postStack.pop()
                if top == LP:
                    break
                postfix.append(top)
        else:
            # operator
            if len(postStack) == 0:
                postStack.append(literal)
                continue
            while len(postStack)>0:
                top = postStack[-1]
                if top - literal <= -2 or top == LP:
                    postStack.append(literal)
                    break
                else:
                    top = postStack.pop()
                    postfix.append(top)
                    if len(postStack) == 0:
                        postStack.append(literal)
                        break
    while len(postStack)>0:
        postfix.append(postStack.pop())
    return postfix

def calcPostfix(postfix):
    # calculate the postfix.
    calcStack = []
    for literal in postfix:
        if literal < 10:
            calcStack.append(literal)
        else:
            try:
                op2 = calcStack.pop()
                op1 = calcStack.pop()
            except:
                return "ERROR"
            if literal == ADD:
                calcStack.append(op1 + op2)
            elif literal == MINUS:
                calcStack.append(op1 - op2)
            elif literal == MUL:
                calcStack.append(op1 * op2)
            elif literal == DIV:
                if op2 == 0:
                    calcStack.append(math.inf)
                else:
                    calcStack.append(op1 / op2)
    return calcStack.pop()

def makeCalculation(results):
    postfix = getPostfix(results)
    return calcPostfix(postfix)

def calc(results):
    displayText = getDisplay(results)
    displayText += str(makeCalculation(results))
    return displayText