import string
import matplotlib
matplotlib.use('WX')

import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import numpy as np
from itertools import izip,chain


"""

Letter distribution from Wikipedia that has been normalized
http://en.wikipedia.org/wiki/Letter_frequency

"""

english_letter_distribution=[
['a',0.08167],['b',0.01492],['c',0.02782],['d',0.04253],['e',0.12702],
['f',0.02228],['g',0.02015],['h',0.06094],['i',0.06966],['j',0.00153],
['k',0.00772],['l',0.04025],['m',0.02406],['n',0.06749],['o',0.07507],
['p',0.01929],['q',0.00095],['r',0.05987],['s',0.06327],['t',0.09056],
['u',0.02758],['v',0.00978],['w',0.02360],['x',0.00150],['y',0.01974],
['z',0.00074]]



f=open('shakespeare_clean.txt')
remove_punc = lambda x: x.translate(string.maketrans("",""),
                        string.punctuation)


# the replaces are done with replace - 
# not as fast as a translate table, 
# but I don't need that level of efficiency and I use that for
# punctuation, which has significantly more chars to exclude

# Take out punctuation and make the strings lowercase; 
# splits strings into an array of lines
str_list  = [y for y in 
    [string.lower(x).replace(',','').replace('  ','').replace('\n','') 
    for x in map(remove_punc,f.readlines())] if y!='' ]

char_list={}
for c in ''.join(np.ndarray.flatten(np.array(str_list))):
    if c != ' ':
        if c in char_list:
            char_list[c]+=1
        else:
            char_list[c]=1        
total_sum=sum([k for j,k in char_list.items()])
#normalize char distribution

for key,obj in char_list.items():
    char_list[key]=obj/(1.0*total_sum)

# makes an ngram. n has to be smaller than or equal to 
# the smallest list
# sl = length of smallest list
# if:
#   n > sl: prints empty list
#   n = sl: prints the given list
#   n < sl: prints the ngram for the list
#           as long as possible
#   
#   ngram(['a','cat','jumped','over','the','hat'],5)
#   would print the 2 5 grams

def ngram(li,n):
    return zip(li,*[li[x:] for x in range(1,n)])

# generates a 2 gram
ngram_list = [ngram(k,2) for k in [z.split() for z in str_list]]
strdict = {}
for ngram_line_list in ngram_list:
    for ngram in ngram_line_list:
        if ngram in strdict:
            strdict[ngram]+=1;
        else:
            strdict[ngram]=1

# get list sorted by descending freq
sorted_by_freq = sorted(strdict.items(),key=lambda x: -x[1])
chars_sorted_by_charval = sorted(char_list.items(),key=lambda x:x[0])
# plot using matplotlib

f,((ax1,ax2),(ax3,ax4)) = plt.subplots(2,2)

# frequency counts
freqs = [li[1] for li in sorted_by_freq]

#number of bins to use for histogram 
nbins = 10
n,bins,patches = ax1.hist(freqs,nbins)

# so for each pair there is a frequency 'f'.
# graphs the 'f's as the x axis
# and the amount of times that f shows up as the y axis

ax1.set_xlabel('Frequency of pair')
ax1.set_ylabel('Frequency of said frequency')

# np histogram uses uniform bin widths
bin_width=bins[1]-bins[0]
ax2.set_yscale('log',basey=10)
ax2.bar(bins[:-1],n,width=bin_width)
print bins[:-1],n,bin_width
#ax2.set_autoscaley_on(False)
#ax2.set_ylim([0,10])


## graph char distro

#0-25, 'a'-'z'.
ax3.set_xlim(0,25)
ax3.bar(range(len(chars_sorted_by_charval)),
        [freq for char,freq in chars_sorted_by_charval] )
char_probs=[prob for char,prob in english_letter_distribution]
ax3.plot(range(26),char_probs,color='r')

# smoothing function
# assumes length > 2, and npoints < length, where length refers to 
# the length of the array and npoints is the # of smoothing points
# to be used. - Has to be an even integer...well it doesn't _have_
# to, using a simple moving avg. definition but it should be in order
# to take a symmetric mean, and this assumes it is, otherwise it will
# cast the divison to an integer.

#... yeah this could use better formatting
def smooth(y,npoints):
    def _smoothing(x):
        return (sum(y[x:x+npoints/2])\
              +sum(y[x-npoints/2:x]))/(1.0*npoints)
    return [y[0]]+y[:npoints-2]+map(_smoothing,range(npoints-1,len(y)+2-npoints))+y[len(y)+2-npoints:]

print(len(smooth(char_probs,3)))

# use two point smoothin
ax3.plot(range(26),smooth(char_probs,2),color="g",linestyle="-",linewidth=.5)
ax3.plot(range(26),smooth(char_probs,3),color="y",linestyle="-",linewidth=.5)
 

plt.show()
