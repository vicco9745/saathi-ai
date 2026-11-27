pm = 'app/main.py'
pi = 'index.html'
m = open(pm, encoding='utf-8').read()
h = open(pi, encoding='utf-8').read()
SERVER = r'''_PD_CLASSIFY = (
    "Decide how the user wants the PDF made. Answer exactly DESIGN if they want a visually designed page: poster, flyer, brochure, menu, "
    "invitation, certificate, greeting card, visiting card, infographic, banner, cover page, magazine or newsletter page, creative resume or CV, "
    "price list or catalogue page, or they say design. Answer exactly DOCUMENT if they want a written document: report, essay, notes, book, "
    "letter, bill or invoice, plain form, or anything that is mostly text and tables. Reply with one word only."
)
def _pdf_design_pages(prompt):
    import re
    from concurrent.futures import ThreadPoolExecutor
    t = (prompt or "").strip()
    if not t:
        return None
    try:
        c = _call_groq(t, system=_PD_CLASSIFY)
    except Exception:
        return None
    if not (c or "").strip().upper().startswith("DESIGN"):
        return None
    fmt, orient = _pdf_page_from_prompt(t)
    w, h = round(fmt[0], 1), round(fmt[1], 1)
    if orient == "L":
        w, h = h, w
    m = re.search(r"(\d{1,2})\s*[-]?\s*(?:pages?|pgs?|पन्ने|पन्नों|पन्ना|पेज|पृष्ठ)", t, re.I)
    n = max(1, min(int(m.group(1)), 12)) if m else 1
    base = (
        "You are a professional graphic designer. Output ONLY the complete HTML of ONE page, starting with <!DOCTYPE html>, no markdown, no explanation. "
        "The page is exactly one <div class=\"page\"> that is " + str(w) + "mm wide and " + str(h) + "mm tall "
        "(width:" + str(w) + "mm;height:" + str(h) + "mm;overflow:hidden;position:relative;box-sizing:border-box); body has margin:0. "
        "Use one inline <style> block only. No JavaScript, no external files, fonts, images or links, no <img>, no filter, backdrop-filter or blend modes. "
        "Use font-family: sans-serif. Decorate with CSS gradients, solid shapes, borders and inline SVG. "
        "DESIGN: a bold, modern, professional look that a person would be proud of: a strong colour palette of 3 or 4 colours, a large headline, "
        "clear hierarchy between headline, subheading and body, generous spacing and aligned blocks. "
        "Size text for the page: body text about 3.5mm, headline 12 to 20 percent of the page width. Nothing may overflow the page or overlap by accident. "
        "Write all visible text in the same language as the user's request, with real useful content for the request. "
        "Never invent prices, phone numbers, addresses, dates or names the user did not give; where needed, write [fill in]."
    )
    def clean(x):
        x = (x or "").replace("```html", "").replace("```", "").strip()
        i = x.lower().find("<!doctype")
        if i < 0:
            i = x.lower().find("<html")
        if i < 0:
            i = x.lower().find("<div")
        if i < 0:
            return None
        x = x[i:]
        x = re.sub(r"<script\b.*?</script>", "", x, flags=re.I | re.S)
        x = re.sub(r"<link\b[^>]*>", "", x, flags=re.I)
        x = re.sub(r"<img\b[^>]*>", "", x, flags=re.I)
        x = re.sub(r"@import[^;]*;", "", x, flags=re.I)
        x = re.sub(r"url\(\s*['\"]?https?:[^)]*\)", "none", x, flags=re.I)
        if "</html>" not in x.lower():
            x += "</div></body></html>"
        return x if (len(x) > 250 and "<div" in x.lower()) else None
    def gen(i, css):
        extra = ""
        if n > 1:
            extra = (" This is page " + str(i + 1) + " of " + str(n) + " of the same document. Use exactly the same colour palette and fonts as the CSS of page 1 below, "
                     "with a different layout suited to this page (for example cover, content pages, closing page).")
            if css:
                extra += "\nPAGE 1 CSS:\n" + css
        for _ in range(2):
            try:
                x = clean(_call_groq(t + (("\n\nWrite page " + str(i + 1) + " of " + str(n) + ".") if n > 1 else ""), system=base + extra))
                if x:
                    return x
            except Exception as e:
                print("PDF design error", repr(e)[:120])
        return None
    p1 = gen(0, "")
    if not p1:
        return None
    pages = [p1]
    if n > 1:
        css = "\n".join(re.findall(r"<style[^>]*>(.*?)</style>", p1, flags=re.I | re.S))[:2500]
        with ThreadPoolExecutor(max_workers=3) as ex:
            more = list(ex.map(lambda i: gen(i, css), range(1, n)))
        pages += [x for x in more if x]
    return {"pages": pages, "mm": [w, h]}

'''
JS = r"""async function __designToPdf(d){
var pages=d.design_pages||[];var W=d.page_mm[0],H=d.page_mm[1];
if(!window.html2canvas){await new Promise(function(ok,no){var s=document.createElement('script');s.src='https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js';s.onload=ok;s.onerror=function(){no(new Error('html2canvas load'));};document.head.appendChild(s);});}
var jsPDF=window.jspdf.jsPDF;
var sh=Math.min(W,H),lg=Math.max(W,H),ori=W>H?'l':'p';
var pdf=new jsPDF({orientation:ori,unit:'mm',format:[sh,lg]});
var pxW=Math.round(W*96/25.4),pxH=Math.round(H*96/25.4);
var sc=Math.max(0.5,Math.min(2,3000/Math.max(pxW,pxH)));
for(var i=0;i<pages.length;i++){
var fr=document.createElement('iframe');
fr.style.cssText='position:fixed;left:-99999px;top:0;border:0;width:'+pxW+'px;height:'+pxH+'px;background:#fff';
var html=String(pages[i]||'').replace(/<script[\s\S]*?<\/script>/gi,'');
await new Promise(function(ok){fr.onload=ok;fr.srcdoc=html;document.body.appendChild(fr);setTimeout(ok,6000);});
try{await fr.contentDocument.fonts.ready;}catch(e){}
await new Promise(function(r){setTimeout(r,300);});
var doc=fr.contentDocument;
var el=doc.querySelector('.page')||doc.body;
var cv=await window.html2canvas(el,{scale:sc,backgroundColor:'#ffffff',useCORS:true,logging:false,width:pxW,height:pxH,windowWidth:pxW,windowHeight:pxH});
if(i>0)pdf.addPage([sh,lg],ori);
pdf.addImage(cv.toDataURL('image/jpeg',0.92),'JPEG',0,0,W,H);
fr.remove();
}
return pdf.output('datauristring').split(',')[1];}
"""
S_CALL = '    _ctx = _pdf_web_context(body.prompt)\n    html_body = _pdf_long_html(body.prompt, _ctx, system)'
S_NEW = '    _dz = _pdf_design_pages(body.prompt)\n    if _dz:\n        return {"design_pages": _dz["pages"], "page_mm": _dz["mm"], "filename": "saathi.pdf", "caption": ""}\n' + S_CALL
S_MK = 'def _pdf_theme_from_prompt(t):'
H_OLD = "return data;}).then(data=>{const pdfSrc=data.pdf_url||"
H_NEW = "return data;}).then(async data=>{try{if(data&&data.design_pages){data.pdf_base64=await __designToPdf(data);}}catch(e){console.error(e);}return data;}).then(data=>{const pdfSrc=data.pdf_url||"
H_MK = 'function renderMessages(){'
if '_pdf_design_pages' in m or 'function __designToPdf' in h:
    print('design: pehle se laga hai')
else:
    bad = []
    if m.count(S_CALL) != 1: bad.append('server call')
    if m.count(S_MK) != 1: bad.append('server marker')
    if m.count('def _pdf_page_from_prompt(') != 1: bad.append('page fn')
    if h.count(H_OLD) != 1: bad.append('site call')
    if h.count(H_MK) != 1: bad.append('site marker')
    if bad:
        print('design: jagah nahi mili', bad)
    else:
        m = m.replace(S_CALL, S_NEW, 1)
        m = m.replace(S_MK, SERVER + S_MK, 1)
        h = h.replace(H_OLD, H_NEW, 1)
        h = h.replace(H_MK, JS + H_MK, 1)
        open(pm, 'w', encoding='utf-8').write(m)
        open(pi, 'w', encoding='utf-8').write(h)
        print('design: laga diya')
