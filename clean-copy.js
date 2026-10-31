// SAATHI CLEAN COPY SYSTEM
document.addEventListener("copy", function(e) {
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
