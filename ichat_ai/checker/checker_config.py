"""Saathi answer checker - settings. Kuch badalna ho to sirf yahin badlo."""
ENABLED = True                  # False karoge to checker band, chat pehle jaisi
MAX_CORRECTIONS = 1             # adhiktam sudhar prayas (2 se zyada nahi chalega)
MAX_EVIDENCE_CHARS = 6000       # khoj ke nateeje kitne akshar tak jaanch ko denge
MIN_REPLY_CHARS = 40            # isse chhota jawab INCOMPLETE maana jayega
HI_NOTE = "ध्यान दें: इस जानकारी की पक्की पुष्टि नहीं हो पाई, इसलिए इसे अंतिम सच न मानें और किसी आधिकारिक स्रोत से जाँच लें।"
EN_NOTE = "Note: I could not fully verify this, so please don't treat it as final and check an official source."
