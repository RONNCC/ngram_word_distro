# removes the intermediate headers from Shakespare's sonnet's
# eg.
# 
#  I
#  
#  Sonnet sonnet sonnet
#  Sonnet sonnet sonnet
#
#  II
#
#  sonnet sonnet sonnet sonnet
## >> deletes the I and II in this case and just puts newlines
import re
a= open('shakespeare.txt','r').read()
b = open('shakespeare_clean.txt','w')
c=re.sub('[IVXLCDM]{1,10}','',a)
b.write(c)
