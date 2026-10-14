import time
from googletrans import Translator
import pysrt

def translate_srt_batched(file_path, output_path, batch_size=20, delay_seconds=1.0):
    translator = Translator()
    subs = pysrt.open(file_path)
    
    # Rozdělíme titulky do dávkových skupin
    for i in range(0, len(subs), batch_size):
        batch = subs[i:i + batch_size]
        
        # Spojíme texty z aktuální dávky oddělené řádkem
        combined_text = "\n".join([sub.text for sub in batch])
        
        try:
            # Přeložíme celý balík najednou
            translated = translator.translate(combined_text, src='en', dest='cs')
            translated_lines = translated.text.split("\n")
            
            # Zpětně přiřadíme přeložené řádky k titulkům
            for j, sub in enumerate(batch):
                if j < len(translated_lines):
                    sub.text = translated_lines[j]
                    
        except Exception as e:
            print(f"Chyba při překladu dávky {i}: {e}")
            
        # Krátká pauza, aby si servery zchladily hlavy
        time.sleep(delay_seconds)
        
    subs.save(output_path, encoding='utf-8')
    print("Překlad dokončen!")
