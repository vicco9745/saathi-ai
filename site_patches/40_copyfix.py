p='format.js'
s=open(p,encoding='utf-8').read()
old='function clean(t){'
new=r"""function clean(t){var s=String(t);var code=/^\s*(def |class |import |from \S+ import |for .+:|while .+:|if .+:|elif .+:|else:|try:|except|finally:|with .+:|return\b|print\()/m;if(s.indexOf('```')<0)return code.test(s)?s:clean0(s);return s.split('```').map(function(p,i){return i%2?p:clean0(p);}).join('```');}
function clean0(t){"""
if 'function clean0(' in s:
    print('copyfix: pehle se laga hai')
elif s.count(old)==1:
    open(p,'w',encoding='utf-8').write(s.replace(old,new,1))
    print('copyfix: laga diya')
else:
    print('copyfix: jagah nahi mili', s.count(old))
