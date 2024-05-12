from transformers import pipeline
import streamlit as st
import os
from streamlit_mic_recorder import mic_recorder

# Переменные для загрузки модели
task_type = 'automatic-speech-recognition'            # Задаем тип запроса
model_path = "path/to/whisper-small-ru"    # Задаем путь до модели
token_path = "path/to/whisper-small-ru"    # Задаем путь до токенизатора


# Функции
def model_result(file_path, task_type, model_path, token_path):
    pipe = pipeline(task=task_type, model=model_path,
                    tokenizer=token_path, device=0)

    text = pipe(file_path)["text"]
    return text

def result(file_path, task_type, model_path, token_path, output_audio_file_name, transcript_path):
    with st.spinner(f"Создание транскрибации... 💫"):
        trans = model_result(file_path, task_type, model_path, token_path)

        output_txt_file = str(output_audio_file_name.split('.')[0]+".txt")

        with open(os.path.join(transcript_path, output_txt_file), "w", encoding='utf8') as f:
            f.write(trans)
        output_file = open(os.path.join(transcript_path,output_txt_file), "r", encoding='utf8')
        output_file_data = output_file.read()

    st.write("Результат: ")
    st.write(trans)
    st.write('\n')
    st.write('\n')
    st.write('Вы можете скачать результат и создать файл для транскрибации заново')

    if st.download_button(
                            label="Скачать результат 📝",
                            data=output_file_data,
                            file_name=output_txt_file,
                            mime='text/plain'
                        ):
        st.balloons()
        st.success('✅ Загрузка завершена !!')   

# Код работы программы
st.set_page_config(
    page_title="Whisper based ASR",
    page_icon="musical_note",
    layout="wide",
    initial_sidebar_state="auto",
)

upload_path = "./whisp_st/uploads/"
download_path = "./whisp_st/downloads/"
transcript_path = "./whisp_st/transcripts/"

st.title("🗣 Автоматический перевод русской речи в текст на small модели Whisper✨")
st.text("Загрузите файл или используйте микрофон")
choose = st.selectbox("Выберите тип аудиоданных", ['Запись из файла', 'Запись с микрофона'])
if "Запись из файла" in choose:
    uploaded_file = st.file_uploader("Загрузите файл", type=["wav","mp3","ogg","wma","aac","flac","mp4","flv"])

    if uploaded_file:
        file_path = os.path.join(upload_path,uploaded_file.name)
        with open(file_path,"wb") as f:
            f.write((uploaded_file).getbuffer())
        with st.spinner(f"Загрузка аудио ... 💫"):
            output_audio_file_name = uploaded_file.name

        if st.button("Создать транскрибацию"):
            result(file_path, task_type, model_path, token_path, output_audio_file_name, transcript_path)

elif 'Запись с микрофона' in choose:
    streamfile = mic_recorder(start_prompt="Начать запись ⏺️",stop_prompt="Закончить запись ⏹️",key='recorder')

    if streamfile:
        file_path = os.path.join(upload_path,'Record.wav')
        with open(file_path,"wb") as f:
            f.write(streamfile['bytes'])
        with st.spinner(f"Загрузка аудио ... 💫"):
            output_audio_file_name = 'Record.wav'
        
        if st.button("Создать транскрибацию"):
            result(file_path, task_type, model_path, token_path, output_audio_file_name, transcript_path)