import streamlit as st

from deep_translator import GoogleTranslator

import re

import time



st.set_page_config(page_title="SRT Překladač", page_icon="📝")



def process_srt(content):

    lines = content.splitlines()

    final_output = []

    current_batch = []

    current_length = 0

    translator = GoogleTranslator(source='auto', target='cs')

    

    progress_bar = st.progress(0)

    status_text = st.empty()

    

    # Rozdělíme na řádky, které chceme přeložit

    text_lines_indices = [i for i, l in enumerate(lines) if not (re.match(r'^\d+$', l) or '-->' in l or not l.strip())]

    total_to_translate = len(text_lines_indices)

    translated_count = 0



    for i, line in enumerate(lines):

        if re.match(r'^\d+$', line) or '-->' in line or not line.strip():

            if current_batch:

                translated = translator.translate("\n".join(current_batch))

                final_output.extend(translated.split('\n'))

                translated_count += len(current_batch)

                progress_bar.progress(min(translated_count / total_to_translate, 1.0))

                current_batch = []

                current_length = 0

            final_output.append(line)

        else:

            current_batch.append(line)

            current_length += len(line)

            # Posíláme větší bloky (cca 3000 znaků), aby to bylo rychlejší

            if current_length > 3000:

                translated = translator.translate("\n".join(current_batch))

                final_output.extend(translated.split('\n'))

                translated_count += len(current_batch)

                progress_bar.progress(min(translated_count / total_to_translate, 1.0))

                current_batch = []

                current_length = 0

    

    if current_batch:

        translated = translator.translate("\n".join(current_batch))

        final_output.extend(translated.split('\n'))

        progress_bar.progress(1.0)

        

    return "\n".join(final_output)



st.title("📝 SRT Překladač")

uploaded_file = st.file_uploader("Vyber .srt soubor", type=["srt"])



if uploaded_file is not None:

    if st.button("Spustit bleskový překlad"):

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

