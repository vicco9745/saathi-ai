// SAATHI UNIVERSAL CLEAN ENGINE (Copy, Select, Listen)
(function() {
    // 1. जब आप टेक्स्ट को सेलेक्ट (Highlight) करके कॉपी करते हैं
    document.addEventListener('copy', function(e) {
        var selection = document.getSelection();
        if (!selection || !selection.toString()) return;
        
        var text = selection.toString();
        // अगर टेक्स्ट में कोई भी स्टार या हैश है, तो उसे साफ करें
        if (text.includes('*') || text.includes('#')) {
            var cleanText = text
                .replace(/\*\*/g, '')  // डबल स्टार हटाएँ
                .replace(/\*/g, '')    // सिंगल स्टार हटाएँ
                .replace(/^#+\s*/gm, '') // हेडिंग हैश हटाएँ
                .replace(/`/g, '');    // कोड बैकटिक हटाएँ
            
            e.clipboardData.setData("text/plain", cleanText);
            e.preventDefault(); // ब्राउज़र को असली टेक्स्ट कॉपी करने से रोकें
        }
    });

    // 2. जब आप 'Copy' वाले बटन पर क्लिक करते हैं
    // पुराने कॉपी फंक्शन को ओवरराइड करें
    if (navigator.clipboard && navigator.clipboard.writeText) {
        var originalWriteText = navigator.clipboard.writeText;
        navigator.clipboard.writeText = function(text) {
            if (typeof text === 'string') {
                text = text.replace(/\*\*/g, '').replace(/\*/g, '').replace(/^#+\s*/gm, '').replace(/`/g, '');
            }
            return originalWriteText.call(navigator.clipboard, text);
        };
    }

    // 3. जब आप 'Listen' (सुनने) वाले बटन पर क्लिक करते हैं
    if (window.SpeechSynthesisUtterance) {
        var OriginalUtterance = window.SpeechSynthesisUtterance;
        window.SpeechSynthesisUtterance = function(text) {
            if (typeof text === 'string') {
                text = text.replace(/\*\*/g, '').replace(/\*/g, '').replace(/^#+\s*/gm, '').replace(/`/g, '');
            }
            return new OriginalUtterance(text);
        };
        window.SpeechSynthesisUtterance.prototype = OriginalUtterance.prototype;
    }
})();
