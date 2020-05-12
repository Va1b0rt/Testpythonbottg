import os

legend = {
'�':'a',
'�':'b',
'�':'v',
'�':'g',
'�':'d',
'�':'e',
'�':'yo',
'�':'zh',
'�':'z',
'�':'i',
'�':'y',
'�':'k',
'�':'l',
'�':'m',
'�':'n',
'�':'o',
'�':'p',
'�':'r',
'�':'s',
'�':'t',
'�':'u',
'�':'f',
'�':'h',
'�':'ts',
'�':'ch',
'�':'sh',
'�':'shch',
'�':'y',
'�':'y',
'�':"'",
'�':'e',
'�':'yu',
'�':'ya',

'�':'A',
'�':'B',
'�':'V',
'�':'G',
'�':'D',
'�':'E',
'�':'Yo',
'�':'Zh',
'�':'Z',
'�':'I',
'�':'Y',
'�':'K',
'�':'L',
'�':'M',
'�':'N',
'�':'O',
'�':'P',
'�':'R',
'�':'S',
'�':'T',
'�':'U',
'�':'F',
'�':'H',
'�':'Ts',
'�':'Ch',
'�':'Sh',
'�':'Shch',
'�':'Y',
'�':'Y',
'�':"'",
'�':'E',
'�':'Yu',
'�':'Ya',
}

def latinizator(letter):
    for i, j in legend.items():
        letter = letter.replace(i, j)
    return letter