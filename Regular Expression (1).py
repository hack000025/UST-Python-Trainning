#!/usr/bin/env python
# coding: utf-8

# In[4]:


#Regular Expression 

"""A regular expression is a special sequence of characters that helps you match or
find other strings or sets of strings, using a specialized syntax held in a pattern




Syntax of Character Classes: 

[0-9] ===>         Any digit  from 0 - 9
[a-z]===>          Any lower case alphabet
[A-Z]===>          Any uppper case alphabet
[a-zA-Z]===>       Any aplhabet (lower or uppper )
[abc]===>          Either a or b or c
[^abc]===>         Except a and b and c
[a-zA-Z0-9]====>   Any aplhanumeric character 
[^a-zA-Z0-9]====>  Except aplhanumeric character (special character like $ , & ,@...etc)






Pre - Defined character  classes :

\d ====>  any digit from 0 - 9 

\D  ====> Any chracter except digit

\s   =====> Space character 

\S  ====>  Any character except space character  

\w =====>   any word character [a-zA-Z0-9]

\W  ====>   Special character 

\.  ====> any characater including special character 









Important function of re Module :


1)  sub()

2) subn()

3) findall()

4) match()

5) fullmatch()

6) search()
 
 etc..

"""


# In[ ]:




