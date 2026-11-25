p = 'index.html'
s = open(p, encoding='utf-8').read()
FN = r"""function __bAsync2(m,t){
const EN={newBudget:'New Budget',name:'Name',nameHint:'e.g. Home budget',total:'Total budget',totalHint:'Enter amount',expTitle:'Expenses - tick and enter amount',addOwn:'Add your own expense',totalSpent:'Total spent',saving:'Savings',submit:'Submit',needName:'Enter a name',needTotal:'Enter the total budget',budget:'Budget',spent:'Spent',myBudgets:'My budgets',seeAll:'All budgets',noBudget:'No budget saved yet',createNew:'Create a new budget',notFound:'This budget was not found',report:'Budget Report',expense:'Expense',amount:'Amount',allTotalBudget:'Total budget',allTotalSpent:'Total spent',allTotalSaving:'Total savings',c0:'Food',c1:'Rent',c2:'Electricity / Bills',c3:'Travel',c4:'Medicine',c5:'Education',c6:'Entertainment',c7:'Shopping'};
const G=[['newBudget','name','nameHint','total','totalHint','expTitle','addOwn','totalSpent','saving','submit','needName'],['needTotal','budget','spent','myBudgets','seeAll','noBudget','createNew','notFound','report','expense','amount'],['allTotalBudget','allTotalSpent','allTotalSaving','c0','c1','c2','c3','c4','c5','c6','c7']];
const errs=[];
function ask(prompt){return fetch(SAATHI_API_BASE+'/v1/chat',{method:'POST',headers:{'Content-Type':'application/json','X-API-Key':SAATHI_KEY},body:JSON.stringify({message:prompt,model:currentModel,memory:[],allow_web_search:false,think:false})}).then(function(r){if(!r.ok){throw new Error('server '+r.status);}return r.json();}).then(function(d){const o=String((d&&d.reply)||'');const i=o.indexOf('{'),k=o.lastIndexOf('}');if(i<0||k<i)throw new Error('no json: '+o.slice(0,50));return JSON.parse(o.slice(i,k+1));});}
function sub(g){const o={};g.forEach(function(k){o[k]=EN[k];});return o;}
let metaP=null,partsP=[];
try{
metaP=ask('The user wrote: '+t+'\nReturn only a JSON object like {"intent":"create","lang":"zh-CN","cur":"¥"}. lang is the BCP-47 code of the language the user wrote in. cur is the currency symbol of the main country of that language. intent is "show" if the user wants to see saved budgets or a report, otherwise "create". No other text.').catch(function(e){errs.push('meta: '+e.message);return {};});
partsP=G.map(function(g){return ask('The user wrote: '+t+'\nTranslate the values of this JSON object into the language the user wrote in. Keep the same keys. Return only the JSON object, nothing else.\n'+JSON.stringify(sub(g))).then(function(d){const res={};g.forEach(function(k){if(d&&typeof d[k]==='string'&&d[k].trim())res[k]=d[k].trim();});if(!Object.keys(res).length)errs.push('empty reply');return res;}).catch(function(e){errs.push('tr: '+e.message);return {};});});
}catch(e){errs.push('js: '+e.message);}
Promise.all([metaP||Promise.resolve({})].concat(partsP)).then(function(a){
const meta=a[0]||{};const labels={};a.slice(1).forEach(function(r){Object.assign(labels,r);});
const n=Object.keys(labels).length;
const ui={lang:String(meta.lang||'en'),cur:String(meta.cur||'₹'),labels:labels};
if(n<10)ui.err=errs.length?errs.slice(0,2).join(' | ').slice(0,160):('translation incomplete ('+n+'/32)');
__bFinish(m,{mode:String(meta.intent||'').toLowerCase().indexOf('show')===0?'all':'form',draft:{},ui:ui});});}
"""
a1 = 'function __budgetHandle(m,text){'
a2 = '__bAsync(m,t);return true;'
if 'function __bAsync2' in s:
    print('budget6: pehle se laga hai')
elif s.count(a1) != 1 or s.count(a2) != 1:
    print('budget6: jagah nahi mili', s.count(a1), s.count(a2))
else:
    s = s.replace(a2, '__bAsync2(m,t);return true;', 1).replace(a1, FN + a1, 1)
    open(p, 'w', encoding='utf-8').write(s)
    print('budget6: laga diya')
