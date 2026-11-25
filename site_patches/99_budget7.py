p = 'index.html'
s = open(p, encoding='utf-8').read()
FN = r"""const __BLK=['newBudget','name','nameHint','total','totalHint','expTitle','addOwn','totalSpent','saving','submit','needName','needTotal','budget','spent','myBudgets','seeAll','noBudget','createNew','notFound','report','expense','amount','allTotalBudget','allTotalSpent','allTotalSaving','c0','c1','c2','c3','c4','c5','c6','c7'];
const __BLANG={
'zh-CN':{c:'¥',cr:/创建|新建|建立|制定|制作|做/,sh:/查看|显示|顯示|我的预算|报告/,v:['新预算','名称','例如：家庭预算','总预算','输入金额','支出（勾选并填写金额）','添加自己的支出','总支出','结余','提交','请输入名称','请输入总预算','预算','已支出','我的预算','全部预算','还没有保存的预算','新建预算','未找到此预算','预算报告','支出项目','金额','总预算','总支出','总结余','餐饮','房租','水电 / 账单','出行','医药','教育','娱乐','购物']},
'es':{c:'€',cr:/crea|crear|nuevo|haz|hacer|quiero/i,sh:/muestra|mostrar|ver |mis |mi presupuesto|informe/i,v:['Nuevo presupuesto','Nombre','p. ej. Presupuesto del hogar','Presupuesto total','Ingresa el monto','Gastos: marca y escribe el monto','Añade tu propio gasto','Total gastado','Ahorro','Enviar','Escribe un nombre','Escribe el presupuesto total','Presupuesto','Gastado','Mis presupuestos','Todos los presupuestos','Aún no hay presupuestos guardados','Crear un presupuesto nuevo','No se encontró este presupuesto','Informe de presupuesto','Gasto','Monto','Presupuesto total','Total gastado','Ahorro total','Comida','Alquiler','Luz / Facturas','Viajes','Medicinas','Educación','Entretenimiento','Compras']},
'ar':{c:'ر.س',cr:/أنشئ|انشئ|إنشاء|انشاء|اعمل|جديد/,sh:/اعرض|أرني|ميزانيتي|ميزانياتي|تقرير/,v:['ميزانية جديدة','الاسم','مثال: ميزانية المنزل','إجمالي الميزانية','أدخل المبلغ','المصروفات: ضع علامة وأدخل المبلغ','أضف مصروفك الخاص','إجمالي المصروف','المدخرات','إرسال','اكتب اسمًا','أدخل إجمالي الميزانية','الميزانية','المصروف','ميزانياتي','كل الميزانيات','لا توجد ميزانية محفوظة بعد','إنشاء ميزانية جديدة','لم يتم العثور على هذه الميزانية','تقرير الميزانية','المصروف','المبلغ','إجمالي الميزانية','إجمالي المصروف','إجمالي المدخرات','طعام','إيجار','كهرباء / فواتير','سفر','أدوية','تعليم','ترفيه','تسوق']},
'fr':{c:'€',cr:/créer|creer|crée|cree|faire|fais|nouveau/i,sh:/montre|affiche|mon budget|mes budgets|rapport/i,v:['Nouveau budget','Nom','ex. Budget du foyer','Budget total','Saisissez le montant','Dépenses : cochez et saisissez le montant','Ajouter votre propre dépense','Total dépensé','Épargne','Envoyer','Saisissez un nom','Saisissez le budget total','Budget','Dépensé','Mes budgets','Tous les budgets','Aucun budget enregistré','Créer un nouveau budget','Ce budget est introuvable','Rapport de budget','Dépense','Montant','Budget total','Total dépensé','Épargne totale','Alimentation','Loyer','Électricité / Factures','Voyage','Médicaments','Éducation','Loisirs','Achats']},
'de':{c:'€',cr:/erstell|neu|mach/i,sh:/zeig|mein budget|meine budgets|bericht/i,v:['Neues Budget','Name','z. B. Haushaltsbudget','Gesamtbudget','Betrag eingeben','Ausgaben: ankreuzen und Betrag eingeben','Eigene Ausgabe hinzufügen','Gesamtausgaben','Ersparnis','Absenden','Namen eingeben','Gesamtbudget eingeben','Budget','Ausgegeben','Meine Budgets','Alle Budgets','Noch kein Budget gespeichert','Neues Budget erstellen','Dieses Budget wurde nicht gefunden','Budgetbericht','Ausgabe','Betrag','Gesamtbudget','Gesamtausgaben','Gesamtersparnis','Essen','Miete','Strom / Rechnungen','Reisen','Medizin','Bildung','Unterhaltung','Einkaufen']},
'pt-BR':{c:'R$',cr:/criar|crie|novo|fazer|faça/i,sh:/mostrar|mostre|meu orçamento|meus orçamentos|relatório/i,v:['Novo orçamento','Nome','ex.: Orçamento da casa','Orçamento total','Digite o valor','Despesas: marque e digite o valor','Adicionar sua própria despesa','Total gasto','Economia','Enviar','Digite um nome','Digite o orçamento total','Orçamento','Gasto','Meus orçamentos','Todos os orçamentos','Nenhum orçamento salvo ainda','Criar um novo orçamento','Este orçamento não foi encontrado','Relatório de orçamento','Despesa','Valor','Orçamento total','Total gasto','Economia total','Comida','Aluguel','Luz / Contas','Viagem','Remédios','Educação','Lazer','Compras']},
'ru':{c:'₽',cr:/созда|нов|сделай/i,sh:/покажи|мой бюджет|мои бюджеты|отчёт|отчет/i,v:['Новый бюджет','Название','например: Домашний бюджет','Общий бюджет','Введите сумму','Расходы: отметьте и введите сумму','Добавить свой расход','Всего потрачено','Сбережения','Отправить','Введите название','Введите общий бюджет','Бюджет','Потрачено','Мои бюджеты','Все бюджеты','Пока нет сохранённых бюджетов','Создать новый бюджет','Бюджет не найден','Отчёт по бюджету','Расход','Сумма','Общий бюджет','Всего потрачено','Всего сбережений','Еда','Аренда','Электричество / Счета','Поездки','Лекарства','Образование','Развлечения','Покупки']},
'ja':{c:'¥',cr:/作成|作って|作る|新しい|新規/,sh:/見せ|表示|私の予算|レポート/,v:['新しい予算','名前','例：家計の予算','予算合計','金額を入力','支出：チェックして金額を入力','自分の支出を追加','支出合計','貯蓄','送信','名前を入力してください','予算合計を入力してください','予算','支出済み','マイ予算','すべての予算','保存された予算はまだありません','新しい予算を作成','この予算は見つかりません','予算レポート','支出','金額','予算合計','支出合計','貯蓄合計','食費','家賃','電気 / 請求書','交通・旅行','医療','教育','娯楽','買い物']},
'ko':{c:'₩',cr:/만들|생성|새로/,sh:/보여|내 예산|보고서/,v:['새 예산','이름','예: 가계 예산','총 예산','금액 입력','지출: 체크하고 금액 입력','나만의 지출 추가','총 지출','저축','제출','이름을 입력하세요','총 예산을 입력하세요','예산','지출됨','내 예산','모든 예산','저장된 예산이 아직 없습니다','새 예산 만들기','이 예산을 찾을 수 없습니다','예산 보고서','지출','금액','총 예산','총 지출','총 저축','식비','월세','전기 / 공과금','여행','의료','교육','오락','쇼핑']},
'ta':{c:'₹',cr:/உருவாக்கு|புதிய|உருவாக்க/,sh:/காட்டு|என் பட்ஜெட்|அறிக்கை/,v:['புதிய பட்ஜெட்','பெயர்','எ.கா: வீட்டு பட்ஜெட்','மொத்த பட்ஜெட்','தொகையை உள்ளிடவும்','செலவுகள்: டிக் செய்து தொகையை உள்ளிடவும்','உங்கள் சொந்த செலவைச் சேர்க்கவும்','மொத்த செலவு','சேமிப்பு','சமர்ப்பி','பெயரை உள்ளிடவும்','மொத்த பட்ஜெட்டை உள்ளிடவும்','பட்ஜெட்','செலவானது','என் பட்ஜெட்கள்','அனைத்து பட்ஜெட்கள்','இன்னும் பட்ஜெட் சேமிக்கப்படவில்லை','புதிய பட்ஜெட்டை உருவாக்கு','இந்த பட்ஜெட் கிடைக்கவில்லை','பட்ஜெட் அறிக்கை','செலவு','தொகை','மொத்த பட்ஜெட்','மொத்த செலவு','மொத்த சேமிப்பு','உணவு','வாடகை','மின்சாரம் / பில்கள்','பயணம்','மருந்து','கல்வி','பொழுதுபோக்கு','ஷாப்பிங்']},
'bn':{c:'৳',cr:/তৈরি|নতুন|বানাও/,sh:/দেখাও|আমার বাজেট|রিপোর্ট/,v:['নতুন বাজেট','নাম','যেমন: সংসারের বাজেট','মোট বাজেট','পরিমাণ লিখুন','খরচ: টিক দিন এবং পরিমাণ লিখুন','নিজের খরচ যোগ করুন','মোট খরচ','সঞ্চয়','জমা দিন','একটি নাম লিখুন','মোট বাজেট লিখুন','বাজেট','খরচ হয়েছে','আমার বাজেট','সব বাজেট','এখনও কোনো বাজেট সংরক্ষিত নেই','নতুন বাজেট তৈরি করুন','এই বাজেট পাওয়া যায়নি','বাজেট রিপোর্ট','খরচ','পরিমাণ','মোট বাজেট','মোট খরচ','মোট সঞ্চয়','খাবার','ভাড়া','বিদ্যুৎ / বিল','ভ্রমণ','ওষুধ','শিক্ষা','বিনোদন','কেনাকাটা']}
};
function __bDetect(t){
if(/[\u3040-\u30ff]|予算/.test(t))return 'ja';
if(/[\u4e00-\u9fff]/.test(t))return 'zh-CN';
if(/[\uac00-\ud7af]/.test(t))return 'ko';
if(/[\u0600-\u06ff]/.test(t))return /بجٹ|میرا|ہے/.test(t)?null:'ar';
if(/[\u0b80-\u0bff]/.test(t))return 'ta';
if(/[\u0980-\u09ff]/.test(t))return 'bn';
if(/[\u0400-\u04ff]/.test(t))return 'ru';
if(/presupuesto|\bcrear\b|\bquiero\b|\bhaz\b/i.test(t))return 'es';
if(/orçamento|orcamento|\bcriar\b|\bcrie\b/i.test(t))return 'pt-BR';
if(/haushalt|erstell|\bmein\b|\bmeine\b|\bzeig/i.test(t))return 'de';
if(/\b(créer|creer|crée|faire|fais|mon|mes|montre|affiche|nouveau)\b/i.test(t))return 'fr';
return null;}
function __bBuiltin(t){
if(/[?？؟]/.test(t))return null;
const l=__bDetect(t);const L=l&&__BLANG[l];if(!L)return null;
const labels={};__BLK.forEach(function(k,i){labels[k]=L.v[i];});
const show=!L.cr.test(t)&&L.sh.test(t);
return {mode:show?'all':'form',draft:{},ui:{lang:l,cur:L.c,labels:labels}};}
"""
a1 = 'function __budgetHandle(m,text){'
a2 = r"""const ascii=!/[^\x00-\x7F]/.test(t);"""
if 'function __bBuiltin' in s:
    print('budget7: pehle se laga hai')
elif s.count(a1) != 1 or s.count(a2) != 1:
    print('budget7: jagah nahi mili', s.count(a1), s.count(a2))
else:
    s = s.replace(a2, "{const _bb=__bBuiltin(t);if(_bb){__bFinish(m,_bb);return true;}}" + a2, 1).replace(a1, FN + a1, 1)
    open(p, 'w', encoding='utf-8').write(s)
    print('budget7: laga diya')
