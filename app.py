import streamlit as st
from deep_translator import MyMemoryTranslator
import re
import time

st.set_page_config(page_title="SRT Překladač", page_icon="📝")

def process_srt(content):
    lines = content.splitlines()
    final_output = []
    current_batch = []
    current_length = 0
    
    # Opravené kódy jazyků pro MyMemory
    translator = MyMemoryTranslator(source='en-US', target='cs-CZ')
    
    progress_bar = st.progress(0)
    
    # Rozdělíme na řádky, které chceme přeložit
    text_lines_indices = [i for i, l in enumerate(lines) if not (re.match(r'^\d+$', l) or '-->' in l or not l.strip())]
    total_to_translate = len(text_lines_indices)
    translated_count = 0

    for i, line in enumerate(lines):
        if re.match(r'^\d+$', line) or '-->' in line or not line.strip():
            if current_batch:
                text_to_translate = "\n".join(current_batch)
                try:
                    translated = translator.translate(text_to_translate)
                except Exception:
                    translated = text_to_translate  # Fallback při chybě
                
                final_output.extend(translated.split('\n'))
                translated_count += len(current_batch)
                progress_bar.progress(min(translated_count / total_to_translate, 1.0))
                current_batch = []
                current_length = 0
                time.sleep(0.5)
            final_output.append(line)
        else:
            current_batch.append(line)
            current_length += len(line)
            # MyMemory raději menší dávky
            if current_length > 400:
                text_to_translate = "\n".join(current_batch)
                try:
                    translated = translator.translate(text_to_translate)
                except Exception:
                    translated = text_to_translate
                
                final_output.extend(translated.split('\n'))
                translated_count += len(current_batch)
                progress_bar.progress(min(translated_count / total_to_translate, 1.0))
                current_batch = []
                current_length = 0
                time.sleep(0.5)
    
    if current_batch:
        text_to_translate = "\n".join(current_batch)
        try:
            translated = translator.translate(text_to_translate)
        except Exception:
            translated = text_to_translate
        final_output.extend(translated.split('\n'))
        progress_bar.progress(1.0)
        
    return "\n".join(final_output)

st.title("📝 SRT Překladač (MyMemory)")
uploaded_file = st.file_uploader("Vyber .srt soubor", type=["srt"])

if uploaded_file is not None:
    if st.button("Spustit překlad"):
        try:
            content = uploaded_file.getvalue().decode("utf-8")
            result = process_srt(content)
            st.success("Hotovo! Překlad dokončen.")
            st.download_button(
                label="📥 STÁHNOUT PŘELOŽENÝ SOUBOR",
                data=result,
                file_name=f"CZE_{uploaded_file.name}",
                mime="text/plain"
            )
        except Exception as e:
            st.error(f"Ajaj, něco se pokazilo: {e}")
