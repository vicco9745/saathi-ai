p='index.html'
s=open(p,encoding='utf-8').read()
pairs=[
("b.style.top='57%';/*ratemid78*/", "b.style.top='170px';/*ratetop79*/"),
("var t=setTimeout(gone,7000);", "var ch0=(typeof getCurrentChat==='function')?getCurrentChat():null,n0=ch0?ch0.messages.length:0,id0=ch0?ch0.id:null;var t=setInterval(function(){try{if(!document.body.contains(b)){clearInterval(t);return;}var c2=getCurrentChat();if(!c2||c2.id!==id0||c2.messages.length>n0){clearInterval(t);gone();}}catch(_){}},400);"),
("if(!x)return;clearTimeout(t);try{var up=", "if(!x)return;clearInterval(t);try{var up="),
]
if 'ratetop79' in s:
    print('ratetop: pehle se laga hai')
else:
    cnt=[s.count(a) for a,b in pairs]
    if cnt==[1,1,1]:
        for a,b in pairs:
            s=s.replace(a,b,1)
        open(p,'w',encoding='utf-8').write(s)
        print('ratetop: laga diya')
    else:
        print('ratetop: jagah nahi mili',cnt)
