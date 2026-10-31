// SAATHI CLEAN ENGINE (For Copy & Listen)
(function() {
    // 1. Jab bhi koi text Copy ho
    document.addEventListener('copy', function(e) {
        var selection = document.getSelection();
        if (!selection || !selection.toString()) return;
        var text = selection.toString();
        if (text.includes('**') || text.includes('*') || text.includes('#')) {
            var cleanText = text
                .replace(/\*\*/g, '')
                .replace(/\*/g, '')
                .replace(/^#+\s*/gm, '')
                .replace(/`/g, '');
            e.clipboardData.setData("text/plain", cleanText);
            e.preventDefault();
        }
    });

    // 2. Jab bhi AI bole (Listen), uske text ko saaf karein
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
