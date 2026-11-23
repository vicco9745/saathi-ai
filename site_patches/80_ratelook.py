p='index.html'
s=open(p,encoding='utf-8').read()
pairs=[
(r"""<button type="button" data-r="down" aria-label="Bad">'+ic(THUMB_DOWN)+'</button>';""", r"""<button type="button" data-r="down" aria-label="Bad">'+ic(THUMB_DOWN)+'</button><span class="crd"></span><button type="button" data-r="close" aria-label="Close">'+ic('<path d="M18 6 6 18M6 6l12 12"/>')+'</button>';"""),
(r"""background:var(--icon-hover,#f0f0f2);color:var(--text,#1a1c2e);font-size:15px;transition:opacity .3s;opacity:0';""", r"""background:var(--panel-bg,#fff);color:var(--text,#1a1c2e);font-size:15px;border-radius:24px;box-shadow:0 4px 20px rgba(0,0,0,.14);transition:opacity .3s;opacity:0';"""),
(r"""b.style.top='170px';/*ratetop79*/""", r"""b.style.top='142px';/*ratelook80*/"""),
(r"""b.querySelectorAll('button').forEach(function(x){x.style.cssText='border:none;background:transparent;color:inherit;padding:6px;cursor:pointer;display:flex';});""", r"""b.querySelectorAll('button').forEach(function(x){x.style.cssText='border:none;background:transparent;color:inherit;padding:6px;cursor:pointer;display:flex';});var dv=b.querySelector('.crd');if(dv)dv.style.cssText='width:1px;align-self:stretch;background:rgba(128,128,128,.3);margin:0 2px';"""),
(r"""try{var up=x.getAttribute('data-r')==='up',""", r"""try{if(x.getAttribute('data-r')==='close'){gone();return;}var up=x.getAttribute('data-r')==='up',"""),
]
if 'ratelook80' in s:
    print('ratelook: pehle se laga hai')
else:
    cnt=[s.count(a) for a,b in pairs]
    if cnt==[1,1,1,1,1]:
        for a,b in pairs:
            s=s.replace(a,b,1)
        open(p,'w',encoding='utf-8').write(s)
        print('ratelook: laga diya')
    else:
        print('ratelook: jagah nahi mili',cnt)
