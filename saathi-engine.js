// Saathi Premium Engine JS
document.addEventListener("DOMContentLoaded", () => {
    if (typeof marked !== 'undefined') marked.setOptions({ gfm: true, breaks: true });
});

window.renderSaathiPremium = function(element, rawText) {
    if (!element) return;
    if (typeof marked === 'undefined' || typeof DOMPurify === 'undefined') {
        element.textContent = rawText; return;
    }
    const html = DOMPurify.sanitize(marked.parse(rawText));
    element.innerHTML = html;
    element.classList.add('saathi-premium-md');
    
    if (/[\u0591-\u07FF\uFB1D-\uFDFD\uFE70-\uFEFC]/.test(rawText)) element.setAttribute('dir', 'rtl');
    if (typeof renderMathInElement !== 'undefined') {
        renderMathInElement(element, { delimiters: [{left: '$$', right: '$$', display: true}, {left: '$', right: '$', display: false}] });
    }
    element.querySelectorAll("pre").forEach(pre => {
        if (pre.parentElement.classList.contains("code-card")) return;
        const card = document.createElement("div"); card.className = "code-card";
        const code = pre.querySelector("code");
        const head = document.createElement("div"); head.className = "code-head";
        const btn = document.createElement("button"); btn.textContent = "Copy"; btn.style.cssText = "background:transparent; border:1px solid #555; color:white; border-radius:5px; padding:2px 8px; cursor:pointer;";
        btn.onclick = async () => { try { await navigator.clipboard.writeText(code?.textContent || pre.textContent); btn.textContent = "Copied!"; setTimeout(()=>btn.textContent="Copy", 1500); } catch(e){} };
        head.appendChild(btn);
        pre.parentNode.insertBefore(card, pre); card.append(head, pre);
    });
};
