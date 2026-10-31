// SAATHI IMAGE COMPRESSOR
document.addEventListener("DOMContentLoaded", () => {
    // हम 'FileReader' को ओवरराइड करेंगे ताकि जब भी इमेज पढ़ी जाए, वह पहले छोटी हो जाए
    const originalReadAsDataURL = FileReader.prototype.readAsDataURL;
    
    FileReader.prototype.readAsDataURL = function(file) {
        if (file && file.type && file.type.startsWith('image/')) {
            const self = this;
            const img = new Image();
            const url = URL.createObjectURL(file);
            
            img.onload = function() {
                const canvas = document.createElement('canvas');
                const MAX_WIDTH = 800;
                let width = img.width;
                let height = img.height;
                
                if (width > MAX_WIDTH) {
                    height = Math.round((height * MAX_WIDTH) / width);
                    width = MAX_WIDTH;
                }
                
                canvas.width = width;
                canvas.height = height;
                const ctx = canvas.getContext('2d');
                ctx.drawImage(img, 0, 0, width, height);
                
                const compressedBase64 = canvas.toDataURL('image/jpeg', 0.7);
                
                // नकली (Fake) इवेंट बनाकर असली फाइल रीडर को ट्रिगर करें
                const fakeEvent = { target: { result: compressedBase64 } };
                if (typeof self.onload === 'function') {
                    self.onload(fakeEvent);
                }
                URL.revokeObjectURL(url);
            };
            img.src = url;
        } else {
            // अगर इमेज नहीं है, तो सामान्य तरीके से पढ़ें
            return originalReadAsDataURL.call(this, file);
        }
    };
});
