#!/usr/bin/env python
# coding: utf-8

# In[5]:


#program for simple calculator

#function for adding two numbers
def add(num1,num2):
    return num1+num2

#function for substracting two numbers
def sub(num1,num2):
    return num1-num2

#function for multiplying two numbers
def mult(num1,num2):
    return num1*num2

#function for dividing two numbers
def div(num1,num2):
    return num1/num2

print("Please Select which you want to perform:\n"     "1.Addition\n"     "2.Substraction\n"     "3.Multiplication\n"     "4.Division\n")

#Taking input from user, that has to be selected which operation he/she want to do
select = int(input("Select operation from 1,2,3,4"))
n1 = int(input("Enter first number:"))
n2 = int(input("Enter Second Number:"))

if select == 1:
    print(n1, "+", n2, "=", add(n1,n2))
elif select ==2:
    print(n1, "-", n2, "=", sub(n1,n2))
elif select ==3:
    print(n1, "*", n2, "=", mult(n1,n2))
elif select ==4:
    print(n1, "/", n2, "=", div(n1,n2))
else:
    print("Invalid Input....")


# In[ ]:




