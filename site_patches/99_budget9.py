p = 'index.html'
s = open(p, encoding='utf-8').read()
FN = r"""const __BGUIDE={
hi:`नाम और कुल बजट भरो, फिर जो खर्च हैं उन पर टिक लगाकर हर खर्च की रकम लिखो। इसके बाद सबमिट दबाओ। तुम्हारा बजट तुम्हारे नाम से सेव हो जाएगा और बचत (बजट − खर्च) अपने आप निकल आएगी। बाद में किसी भी चैट में वही नाम लिखो या "मेरा बजट बताओ" कहो, Saathi वही सेव किया हुआ डेटा फिर दिखा देगा। सारे बजट एक पन्ने में खुलते हैं और वहाँ से PDF भी मिल जाती है।`,
en:`Fill in the name and the total budget, tick the expenses you have and enter each amount. Then press Submit. Your budget is saved under your name, and the savings (budget minus expenses) is worked out for you. Later, in any chat, just type that name or ask for your budget and Saathi shows the saved data again. You can also open all your budgets on one page and download the PDF.`,
'zh-CN':`填写名称和总预算，勾选你的支出项目并填写每项金额，然后点击“提交”。预算会以你的名称保存，结余（预算减支出）会自动算出。之后在任何聊天里输入这个名称或说“查看我的预算”，Saathi 就会再次显示已保存的数据。你也可以在一个页面查看全部预算并下载 PDF。`,
es:`Escribe el nombre y el presupuesto total, marca tus gastos y escribe el monto de cada uno. Luego pulsa Enviar. Tu presupuesto se guarda con tu nombre y el ahorro (presupuesto menos gastos) se calcula solo. Más tarde, en cualquier chat, escribe ese nombre o pide tu presupuesto y Saathi mostrará de nuevo los datos guardados. También puedes ver todos tus presupuestos en una página y descargar el PDF.`,
ar:`اكتب الاسم وإجمالي الميزانية، ثم ضع علامة على مصروفاتك واكتب مبلغ كل منها، ثم اضغط إرسال. تُحفظ ميزانيتك باسمك ويُحسب المدخرات (الميزانية ناقص المصروفات) تلقائيًا. لاحقًا، في أي محادثة، اكتب هذا الاسم أو اطلب ميزانيتك وسيعرض Saathi البيانات المحفوظة مرة أخرى. ويمكنك أيضًا فتح كل ميزانياتك في صفحة واحدة وتنزيل ملف PDF.`,
fr:`Saisissez le nom et le budget total, cochez vos dépenses et saisissez le montant de chacune, puis appuyez sur Envoyer. Votre budget est enregistré à votre nom et l'épargne (budget moins dépenses) est calculée automatiquement. Plus tard, dans n'importe quelle discussion, écrivez ce nom ou demandez votre budget et Saathi affichera de nouveau les données enregistrées. Vous pouvez aussi ouvrir tous vos budgets sur une page et télécharger le PDF.`,
de:`Gib den Namen und das Gesamtbudget ein, kreuze deine Ausgaben an und trage jeweils den Betrag ein. Tippe dann auf Absenden. Dein Budget wird unter deinem Namen gespeichert, und die Ersparnis (Budget minus Ausgaben) wird automatisch berechnet. Später kannst du in jedem Chat diesen Namen eingeben oder nach deinem Budget fragen, und Saathi zeigt die gespeicherten Daten wieder an. Alle Budgets lassen sich außerdem auf einer Seite öffnen und als PDF herunterladen.`,
'pt-BR':`Digite o nome e o orçamento total, marque suas despesas e digite o valor de cada uma. Depois toque em Enviar. Seu orçamento é salvo com o seu nome e a economia (orçamento menos despesas) é calculada automaticamente. Mais tarde, em qualquer chat, digite esse nome ou peça seu orçamento e o Saathi mostrará os dados salvos de novo. Você também pode abrir todos os orçamentos em uma página e baixar o PDF.`,
ru:`Введите название и общий бюджет, отметьте свои расходы и укажите сумму каждого, затем нажмите «Отправить». Бюджет сохранится под вашим названием, а сбережения (бюджет минус расходы) посчитаются автоматически. Позже в любом чате напишите это название или попросите показать бюджет, и Saathi снова покажет сохранённые данные. Все бюджеты также открываются на одной странице, оттуда можно скачать PDF.`,
ja:`名前と予算合計を入力し、支出にチェックを入れて金額を入力してから「送信」を押してください。予算はあなたの名前で保存され、貯蓄（予算−支出）は自動で計算されます。後でどのチャットでもその名前を入力するか予算を尋ねると、Saathi が保存したデータをもう一度表示します。すべての予算を1ページで開いて PDF をダウンロードすることもできます。`,
ko:`이름과 총 예산을 입력하고, 지출 항목에 체크한 뒤 금액을 입력하고 ‘제출’을 누르세요. 예산은 입력한 이름으로 저장되며 저축(예산−지출)은 자동으로 계산됩니다. 나중에 어느 채팅에서든 그 이름을 입력하거나 예산을 물어보면 Saathi가 저장된 데이터를 다시 보여 줍니다. 모든 예산을 한 페이지에서 열어 PDF로 내려받을 수도 있습니다.`,
ta:`பெயரையும் மொத்த பட்ஜெட்டையும் நிரப்பி, உங்கள் செலவுகளில் டிக் செய்து ஒவ்வொன்றின் தொகையையும் உள்ளிட்டு “சமர்ப்பி” அழுத்துங்கள். உங்கள் பட்ஜெட் உங்கள் பெயரில் சேமிக்கப்படும்; சேமிப்பு (பட்ஜெட் − செலவு) தானாகக் கணக்கிடப்படும். பின்னர் எந்த அரட்டையிலும் அந்தப் பெயரை எழுதினாலோ உங்கள் பட்ஜெட்டைக் கேட்டாலோ Saathi சேமித்த தரவை மீண்டும் காட்டும். அனைத்து பட்ஜெட்களையும் ஒரே பக்கத்தில் திறந்து PDF பதிவிறக்கலாம்.`,
bn:`নাম ও মোট বাজেট লিখুন, আপনার খরচগুলোতে টিক দিয়ে প্রতিটির পরিমাণ লিখুন, তারপর “জমা দিন” চাপুন। আপনার বাজেট আপনার নামে সংরক্ষিত হবে এবং সঞ্চয় (বাজেট − খরচ) নিজে থেকেই হিসাব হবে। পরে যেকোনো চ্যাটে সেই নামটি লিখলে বা আপনার বাজেট চাইলে Saathi সংরক্ষিত তথ্য আবার দেখাবে। সব বাজেট এক পৃষ্ঠায় খুলে PDF-ও নামিয়ে নেওয়া যায়।`
};
__BGUIDE.zh=__BGUIDE['zh-CN'];__BGUIDE.pt=__BGUIDE['pt-BR'];
function __bGuideText(u){return __BGUIDE[u.lang]||__BGUIDE[String(u.lang||'').split('-')[0].toLowerCase()]||__BGUIDE.en;}
function __bGuideRun(m,el,row){
const bd=m.budget||{};const u=__bU(bd.ui);
const sg=function(t){try{return Array.from(new Intl.Segmenter(undefined,{granularity:'grapheme'}).segment(t),function(x){return x.segment;});}catch(_){return Array.from(t);}};
const g=sg(__bGuideText(u));
const gb=document.createElement('div');gb.className='bubble';gb.dir='auto';row.appendChild(gb);el.__gb=gb;
const kids=Array.from(el.children);const K=kids.length;const R=4;
const total=K*R+Math.ceil(g.length/3);
let c=(typeof m.__ba==='number'&&!m.__bdone)?m.__ba:total;
function render(c){
kids.forEach(function(k,i){k.style.display=(c>=i*R)?'':'none';});
const n=Math.max(0,Math.min(g.length,(c-K*R)*3));
gb.textContent=n?g.slice(0,n).join(''):'';
gb.style.display=(c>=K*R)?'':'none';}
render(c);
if(c<total){
window.__bTm=window.__bTm||new Map();
const old=window.__bTm.get(m);if(old)clearInterval(old);
const id=setInterval(function(){
if(!el.isConnected){clearInterval(id);return;}
c=Math.min(total,c+1);m.__ba=c;render(c);
if(c>=total){clearInterval(id);m.__bdone=true;try{saveChats();}catch(_){}}
},28);
window.__bTm.set(m,id);}}
"""
a1 = 'function __budgetHandle(m,text){'
R = [
(r"""function __buildBudgetCard(m){__bCss();""", r"""function __buildBudgetCard(m,row){__bCss();"""),
(r"""if(bd.mode==='form')drawForm();else if(bd.mode==='saved')drawSaved();else drawAll();""",
 r"""if(bd.mode==='form')drawForm();else if(bd.mode==='saved')drawSaved();else drawAll();
if(row){row.appendChild(el);if(bd.mode==='form')__bGuideRun(m,el,row);}"""),
(r"""row.appendChild(__buildBudgetCard(m));""", r"""__buildBudgetCard(m,row);"""),
(r"""function __bFinish(m,b){m.typing=false;m.processing=null;m.text='';m.budget=b;""",
 r"""function __bFinish(m,b){m.typing=false;m.processing=null;m.text='';m.budget=b;if(b&&b.mode==='form'){m.__ba=0;m.__bdone=false;}"""),
(r"""m.budget={mode:'saved',id:rec.id,ui:bd.ui||null};""",
 r"""m.budget={mode:'saved',id:rec.id,ui:bd.ui||null};if(el.__gb)el.__gb.remove();try{const _t=window.__bTm&&window.__bTm.get(m);if(_t)clearInterval(_t);}catch(_){}m.__bdone=true;"""),
]
if 'function __bGuideRun' in s:
    print('budget9: pehle se laga hai')
else:
    bad = [i for i, (a, b) in enumerate(R) if s.count(a) != 1]
    if bad or s.count(a1) != 1:
        print('budget9: jagah nahi mili', bad, s.count(a1))
    else:
        for a, b in R:
            s = s.replace(a, b, 1)
        s = s.replace(a1, FN + a1, 1)
        open(p, 'w', encoding='utf-8').write(s)
        print('budget9: laga diya')
