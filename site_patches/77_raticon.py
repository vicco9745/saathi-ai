p='index.html'
s=open(p,encoding='utf-8').read()
old1="'<span>How was this conversation?</span><button type=\"button\" data-r=\"up\""
new1="'<span class=\"cri\" style=\"display:flex\">'+(function(){var a=document.getElementById('actionIcon');return a&&a.innerHTML.indexOf('<svg')>-1?a.innerHTML:'';})()+'</span><span class=\"crt\">How was this conversation?</span><button type=\"button\" data-r=\"up\""
old2="b.querySelector('span').style.cssText='flex:1';"
new2="b.querySelector('.crt').style.cssText='flex:1';var s0=b.querySelector('.cri svg');if(s0){s0.style.cssText='width:22px;height:22px;display:block';}/*raticon77*/"
if 'raticon77' in s:
    print('raticon: pehle se laga hai')
else:
    cnt=[s.count(old1),s.count(old2)]
    if cnt==[1,1]:
        s=s.replace(old1,new1,1).replace(old2,new2,1)
        open(p,'w',encoding='utf-8').write(s)
        print('raticon: laga diya')
    else:
        print('raticon: jagah nahi mili',cnt)
