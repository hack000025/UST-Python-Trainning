#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#search()

import re 
s = input("Enter pattern to check:")
m = re.search(s,"abaaaba")
if m!= None :
    print("Match is available")
    print("First Occurence of match start index:",m.start(),"and End index:",m.end())
else:
    print("Match is available")


# In[ ]:





# In[ ]:




