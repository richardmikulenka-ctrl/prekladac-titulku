import streamlit as st
from deep_translator import GoogleTranslator
import re

st.set_page_config(page_title="SRT Překladač", page_icon="📝")

def process_srt(content):
    lines = content.splitlines()
    final_output = []
    current_batch = []
    translator = GoogleTranslator(source='auto', target='cs')

    for line in lines:
        if re.match(r'^\d+$', line) or '-->' in line or not line.strip():
            if current_batch:
                translated = translator.translate("\n".join(current_batch))
                final_output.extend(translated.split('\n'))
                current_batch = []
            final_output.append(line)
        else:
            current_batch.append(line)
    
    if current_batch:
        translated = translator.translate("\n".join(current_batch))
        final_output.extend(translated.split('\n'))
        
    return "\n".join(final_output)

st.title("📝 SRT Překladač")
st.write("Nahraj soubor a já ho bleskově přeložím do češtiny.")

uploaded_file = st.file_uploader("Vyber .srt soubor", type=["srt"])

if uploaded_file is not None:
    if st.button("Přeložit nyní"):
        with st.spinner('Překládám...'):
            content = uploaded_file.getvalue().decode("utf-8")
            result = process_srt(content)
            st.success("Hotovo!")
            st.download_button(
                label="Stáhnout přeložené titulky",
                data=result,
                file_name=f"CZE_{uploaded_file.name}",
                mime="text/plain"
            )
