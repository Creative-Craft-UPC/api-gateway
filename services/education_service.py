import json
import random
from typing import List, Literal
import unicodedata
from fastapi import HTTPException
import httpx
from schemas.education_schemas import ActivitySchema, ExercicesSchema
from schemas.ia_schema import AudioPromptSchema
from schemas.profile_schemas import AsdProfileSchema
from services.ia_service import post_generate_audio, post_generate_exercice
from utils.http_client import request
import uuid
from datetime import datetime

EDUCATION_SERVICE_URL = "http://localhost:8002"

async def get_activity_by_id(activity_id: str):
    return await request("GET", f"{EDUCATION_SERVICE_URL}/activities/{activity_id}")

async def get_exercice_by_id(exercice_id: str):
    return await request("GET", f"{EDUCATION_SERVICE_URL}/exercices/{exercice_id}")

async def post_activity(activity: dict):
    return await request("POST",f"{EDUCATION_SERVICE_URL}/activities/",json=activity )

async def update_activity(activity_id: str, activity: dict):
    return await request('PUT', f"{EDUCATION_SERVICE_URL}/activities/{activity_id}", json={
        "instructions": activity["instructions"],
        "type": activity["type"],
        "subtype": activity.get("subtype"),
        "statement": activity["statement"],
        "audio": activity.get("audio")
    })

async def create_exercice(exercice: dict):
    return await request("POST", f"{EDUCATION_SERVICE_URL}/exercices/", json={
        "audio": exercice.get("audio"),
        "question": exercice.get("question"),
        "answer": exercice["answer"],
        "options": exercice.get("options", []),
        "image_options": exercice.get("image_options", []),
        "principal_image": exercice.get("principal_image"),
        "type": exercice["type"],
        "subtype": exercice.get("subtype")
    })

async def update_exercice(exercice_id: str, exercice: dict):
    return await request("PUT", f"{EDUCATION_SERVICE_URL}/exercices/{exercice_id}", json={
        "audio": exercice.get("audio"),
        "question": exercice.get("question"),
        "answer": exercice["answer"],
        "options": exercice.get("options", []),
        "image_options": exercice.get("image_options", []),
        "principal_image": exercice.get("principal_image"),
        "type": exercice["type"],
        "subtype": exercice.get("subtype")
    })

async def get_image_data_by_type_and_concept(type: str, concept: str):
    return await request("GET", f"{EDUCATION_SERVICE_URL}/image-data/{type}/concept/{concept}")

async def generate_instruction_audios(instructions: list[str]):
    url_audio_list = []
    for instruction in instructions:
        audio_instruction: AudioPromptSchema = {
            "text": instruction,
            "voice": "nova",
            "audio_name": "audio-" + str(uuid.uuid4()),
            "instructions": "Habla con voz clara y pausada, toma tiempos, usa un tono infantil y tranquilo."
        }
        url_audio_instruction = await post_generate_audio(audio_instruction)
        url_audio_list.append(url_audio_instruction["audio_url"])
    return url_audio_list
    

async def create_default_activities() -> List[dict]:
    instruction_list = ["Escucha el audio y selecciona la emoción que escuchas.",
                        "Mira la imagen y escucha la historia, luego selecciona la emoción correcta.",
                        "Mira la imagen y escucha la historia, luego selecciona la actividad que hacen.",
                        "Arma el rompecabezas juntando las piezas y formando una imagen. Luego responde: ¿Qué emoción está en la imagen",
                        "Arma el rompecabezas juntando las piezas y formando una imagen. Luego responde: ¿Qué actividad está realizando la imagen?"
                        ]
    url_audio_list = await generate_instruction_audios(instruction_list)
    default_data = [
        {
            "type": "Escucha emoción",
            "subtype": "emocional",
            "instructions": instruction_list[0],
            "statement": "Escucha y responde",
            "audio":url_audio_list[0]
        },
        {
            "type": "Historias",
            "subtype": "emocional",
            "instructions": instruction_list[1],
            "statement": "Escucha la historia y responde",
            "audio":url_audio_list[1]
        },
        {
            "type": "Historias",
            "subtype": "social",
            "instructions": instruction_list[2],
            "statement": "Escucha la historia y responde",
            "audio":url_audio_list[2]
        },
        {
           "type": "Resuelve problema",
            "subtype": "emocional",
            "instructions": instruction_list[3],
            "statement": "Relaciona las emociones",
            "audio":url_audio_list[3]
        },
        {
            "type": "Resuelve problema",
            "subtype": "social",
            "instructions": instruction_list[4],
            "statement": "Arma el rompecabezas",
            "audio":url_audio_list[4]
        },
    ]


    activities = []
    for activity in default_data:
        response = await post_activity(activity)
        if response:
            activities.append(response)
    return activities



def generate_unique_audio_name(prefix: str = "audio") -> str:
    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    unique_id = uuid.uuid4().hex[:8]  # usa solo 8 caracteres del UUID para hacerlo más corto
    return f"{prefix}-{timestamp}-{unique_id}"

def normalize_text(text: str) -> str:
    return unicodedata.normalize("NFKD", text).encode("ASCII", "ignore").decode().lower()

def get_voice_instructions_by_emotion(emotion: str) -> str:
    emotion = normalize_text(emotion)
    emotion_instructions = {
        "alegria": "Lee el texto con una voz animada, brillante y rápida. Usa entonación ascendente y énfasis positivo",
        "miedo": "Lee con voz temblorosa, pausada, y con tono descendente. Que suene como si estuvieras asustado.",
        "tristeza": "Usa voz suave, lenta, con tono bajo y apagado. Habla como si estuvieras apesadumbrado, triste, sollozando.",
        "enojo": "Habla con voz firme, rápida, y tono más fuerte. Usa un ritmo cortante y enérgico, con ira.",
        "asco": "Lee con tono de repulsión, ligeramente nasal o contenido. Que suene como si algo te diera asco.",
        "sorpresa": "Usa una voz con cambios rápidos de tono, entonación alta y energía repentina. Haz pausas para mostrar sorpresa."
    }

    if emotion not in emotion_instructions:
        raise ValueError(f"Emoción no reconocida: '{emotion}'")

    return emotion_instructions[emotion]

def get_option_images_url(options: list[str]) -> list[str]:
    base_url = "https://storage.googleapis.com/socialfun-images/pictograms/pictograma_"
    url_list = []
    for option in options:
        replaced = option.replace(" ", "_")
        newOption = ""
        if replaced == "alegria" or replaced == "alegría":
            newOption = "alegre"
        elif replaced == "tristeza":
            newOption = "triste"
        else:
            newOption = replaced
        url = base_url + newOption + ".png"
        url_list.append(url)
    return url_list

async def generate_one_story_exercice(asd_data: dict, type: Literal["emocional", "social"]):
    emotions = ["tristeza", "alegria", "miedo", "enojo", "asco", "sorpresa"]
    social_activities = ["decir_adios", "decir_gracias", "decir_hola", "decir_muy_bien", "pedir_ayuda", "pedir_permiso"]
    image_type = ""
    if asd_data["visualComprehension"] == 1:
        image_type = "pictograma"
    elif asd_data["visualComprehension"] == 2:
        image_type = "animada"
    else:
        image_type = "real"

    if type == "emocional":
        emotion = random.choice(emotions)
        data_emotional = await get_image_data_by_type_and_concept(image_type, emotion)
        prompt_emotional = ("Crea un ejercicio tipo: historia, subtipo: emocional, de entre 20 "
                "y 40 palabras para un niño con TEA de nivel DSM " + str(asd_data.severityLevel) + 
                 ", con una edad de " + str(asd_data.age) + " años, que refleje la "
                 "emoción \"" + emotion + "\". Usa esta descripción de una imagen "
                 "para realizarlo: \"" + data_emotional["description"] + ".\" Escoge 2 emociones extra como "
                 "opciones erróneas. Las emociones solo pueden ser estas: \"tristeza\", \"alegria\", \"miedo\", \"enojo\", \"asco\", \"sorpresa\". Devuelve un JSON con este formato exacto: {\n\"story\": \"Pedro tocó algo sucio. Pedro tocó basura. Pedro movió las manos. Pedro quería limpiarse. Pedro buscó servilletas. Pedro sintió asco. \", \n\"answer\": \"asco\",\n \"options\": [\"enojo\", \"miedo\"],\n \"type\": \"Historia\",\n \"subtype\": \"emocional\"\n}. ")
        ia_response_emotional = await post_generate_exercice(prompt_emotional)
        emotional_response_dict = json.loads(ia_response_emotional["response"])
        emotional_options = emotional_response_dict["options"]
        final_emotional_options = emotional_options + [emotional_response_dict["answer"]]
        random.shuffle(final_emotional_options)
        audio_emotional_story: AudioPromptSchema = {
            "text": emotional_response_dict["story"],
            "voice": "nova",
            "audio_name": generate_unique_audio_name(emotional_response_dict["answer"]),
            "instructions": "Habla con voz clara y pausada, toma tiempos, usa un tono infantil y tranquilo."
        }
        url_emotional_audio = await post_generate_audio(audio_emotional_story)
        emotional_storie_exercice: ExercicesSchema = {
            "audio": url_emotional_audio["audio_url"],
            "question": "¿Cómo se sintió?",
            "answer": emotional_response_dict["answer"],
            "options": final_emotional_options,
            "image_options": get_option_images_url(final_emotional_options),
            "principal_image": data_emotional["image_url"],
            "type": "Historias",
            "subtype": "emocional"
        }
        return emotional_storie_exercice
        
    else:
        social_activity = random.choice(social_activities)
        data_social = await get_image_data_by_type_and_concept(image_type, social_activity)
        prompt_social = ("Crea un ejercicio tipo: historia, subtipo: social, de entre 20 "
                "y 40 palabras para un niño con TEA de nivel DSM " + str(asd_data.severityLevel) + 
                 ", con una edad de " + str(asd_data.age) + " años, en la que se realize la "
                 "actividad \"" + social_activity.replace("_", " ") + "\". Usa esta descripción de una imagen "
                 "para realizarlo: \"" + data_social["description"] + ".\" Escoge 2 actividades sociales extra como "
                 "opciones erróneas. Las actividades sociales solo pueden ser estas: \"decir adios\", \"decir gracias\", \"decir hola\", \"decir muy bien\", \"pedir ayuda\", \"pedir permiso\". No inventes otras opciones. Devuelve un JSON con este formato exacto: {\n\"story\": \"El profesor entró al salón. La profesor dijo \\\"Buenos días, Marcos\\\". Marcos dijo \\\"Hola, profesor\\\". Marcos dijo hola al profesor.\", \n\"answer\": \"decir hola\",\n \"options\": [\"pedir permiso\", \"decir gracias\"],\n \"type\": \"Historia\",\n \"subtype\": \"social\"\n}")
        ia_response_social = await post_generate_exercice(prompt_social)
        social_response_dict = json.loads(ia_response_social["response"])
        social_options = social_response_dict["options"]
        final_social_options = social_options + [social_response_dict["answer"]]
        random.shuffle(final_social_options)
        audio_social_story: AudioPromptSchema = {
            "text": social_response_dict["story"],
            "voice": "nova",
            "audio_name": generate_unique_audio_name(social_response_dict["answer"]),
            "instructions": "Habla con voz clara y pausada, toma tiempos, usa un tono infantil y tranquilo."
        }
        url_social_audio = await post_generate_audio(audio_social_story)
        social_storie_exercice: ExercicesSchema = {
            "audio": url_social_audio["audio_url"],
            "question": "¿Qué hicieron?",
            "answer": social_response_dict["answer"],
            "options": final_social_options,
            "image_options": get_option_images_url(final_social_options),
            "principal_image": data_social["image_url"],
            "type": "Historias",
            "subtype": "social"
        }
        return social_storie_exercice
        


async def generate_stories_exercices(asd_data: dict):
    emotions = ["tristeza", "alegria", "miedo", "enojo", "asco", "sorpresa"]
    social_activities = ["decir_adios", "decir_gracias", "decir_hola", "decir_muy_bien", "pedir_ayuda", "pedir_permiso"]
    story_exercices = []
    available_emotions = emotions.copy()
    available_social_activities = social_activities.copy()
    for _ in range(3):
        emotion = random.choice(available_emotions)
        available_emotions.remove(emotion)

        social_activity = random.choice(available_social_activities)
        available_social_activities.remove(social_activity)

        image_type = ""
        if asd_data["visualComprehension"] == 1:
            image_type = "pictograma"
        elif asd_data["visualComprehension"] == 2:
            image_type = "animada"
        else:
            image_type = "real"
        data_emotional = await get_image_data_by_type_and_concept(image_type, emotion)
        data_social = await get_image_data_by_type_and_concept(image_type, social_activity)
        prompt_emotional = ("Crea un ejercicio tipo: historia, subtipo: emocional, de entre 20 "
                "y 40 palabras para un niño con TEA de nivel DSM " + str(asd_data["severityLevel"]) + 
                 ", con una edad de " + str(asd_data["age"]) + " años, que refleje la "
                 "emoción \"" + emotion + "\". Usa esta descripción de una imagen "
                 "para realizarlo: \"" + data_emotional["description"] + ".\" Escoge 2 emociones extra como "
                 "opciones erróneas. Las emociones solo pueden ser estas: \"tristeza\", \"alegria\", \"miedo\", \"enojo\", \"asco\", \"sorpresa\". Devuelve un JSON con este formato exacto: {\n\"story\": \"Pedro tocó algo sucio. Pedro tocó basura. Pedro movió las manos. Pedro quería limpiarse. Pedro buscó servilletas. Pedro sintió asco. \", \n\"answer\": \"asco\",\n \"options\": [\"enojo\", \"miedo\"],\n \"type\": \"Historia\",\n \"subtype\": \"emocional\"\n}. ")
        prompt_social = ("Crea un ejercicio tipo: historia, subtipo: social, de entre 20 "
                "y 40 palabras para un niño con TEA de nivel DSM " + str(asd_data["severityLevel"]) + 
                 ", con una edad de " + str(asd_data["age"]) + " años, en la que se realize la "
                 "actividad \"" + social_activity.replace("_", " ") + "\". Usa esta descripción de una imagen "
                 "para realizarlo: \"" + data_social["description"] + ". Escoge 2 actividades sociales extra como "
                 "opciones erróneas. Las actividades sociales solo pueden ser estas: \"decir adios\", \"decir gracias\", \"decir hola\", \"decir muy bien\", \"pedir ayuda\", \"pedir permiso\". No inventes otras opciones. Devuelve un JSON con este formato exacto: {\n\"story\": \"El profesor entró al salón. La profesor dijo \\\"Buenos días, Marcos\\\". Marcos dijo \\\"Hola, profesor\\\". Marcos dijo hola al profesor.\", \n\"answer\": \"decir hola\",\n \"options\": [\"pedir permiso\", \"decir gracias\"],\n \"type\": \"Historia\",\n \"subtype\": \"social\"\n}")
        ia_response_emotional = await post_generate_exercice(prompt_emotional)
        ia_response_social = await post_generate_exercice(prompt_social)
        emotional_response_dict = json.loads(ia_response_emotional["response"])
        social_response_dict = json.loads(ia_response_social["response"])
        
        audio_emotional_story: AudioPromptSchema = {
            "text": emotional_response_dict["story"],
            "voice": "nova",
            "audio_name": generate_unique_audio_name(emotional_response_dict["answer"]),
            "instructions": "Habla con voz clara y pausada, toma tiempos, usa un tono infantil y tranquilo."
        }
        audio_social_story: AudioPromptSchema = {
            "text": social_response_dict["story"],
            "voice": "nova",
            "audio_name": generate_unique_audio_name(social_response_dict["answer"]),
            "instructions": "Habla con voz clara y pausada, toma tiempos, usa un tono infantil y tranquilo."
        }

        url_emotional_audio = await post_generate_audio(audio_emotional_story)
        url_social_audio = await post_generate_audio(audio_social_story)
        emotional_options = emotional_response_dict["options"]
        social_options = social_response_dict["options"]
        
        final_emotional_options = emotional_options + [emotional_response_dict["answer"]]
        random.shuffle(final_emotional_options)
        
        final_social_options = social_options + [social_response_dict["answer"]]
        random.shuffle(final_social_options)

        emotional_storie_exercice: ExercicesSchema = {
            "audio": url_emotional_audio["audio_url"],
            "question": "¿Cómo se sintió?",
            "answer": emotional_response_dict["answer"],
            "options": final_emotional_options,
            "image_options": get_option_images_url(final_emotional_options),
            "principal_image": data_emotional["image_url"],
            "type": "Historias",
            "subtype": "emocional"
        }
        social_storie_exercice: ExercicesSchema = {
            "audio": url_social_audio["audio_url"],
            "question": "¿Qué hicieron?",
            "answer": social_response_dict["answer"],
            "options": final_social_options,
            "image_options": get_option_images_url(final_social_options),
            "principal_image": data_social["image_url"],
            "type": "Historias",
            "subtype": "social"
        }
        story_exercices.append(emotional_storie_exercice)
        story_exercices.append(social_storie_exercice)
    return story_exercices


async def generate_listen_exercices(asd_data: dict):
    emotions = ["tristeza", "alegria", "miedo", "enojo", "asco", "sorpresa"]
    available_emotions = emotions.copy()
    phrase_exercies = []
    for _ in range(3):
        emotion = random.choice(available_emotions)
        available_emotions.remove(emotion)
        prompt = ("Crea un ejercicio tipo: escucha emoción, subtipo: emocional, de no más "
              "de 12 palabras para un niño con TEA de nivel DSM " + str(asd_data["severityLevel"]) +", con una edad de "+ str(asd_data["age"]) +
              " años, en la que se refleje la emoción \"" + emotion + "\". Para este ejercicio, debes inventar "
              "una frase que niños con el nivel de TEA y de esa edad puedan decir y/o comprender, "
              "en base a la emoción. Las emociones solo pueden ser estas: \"tristeza\", \"alegria\", \"miedo\", \"enojo\", \"asco\", \"sorpresa\". Devuelve un JSON con este formato exacto: {\"phrase\": \"Estoy triste porque perdí mi juguete.\",\"answer\": \"tristeza\",\"options\": [\"alegría\", \"asco\"],\"type\": \"Escucha emoción\",\"subtype\": \"emocional\"}")
        ia_response = await post_generate_exercice(prompt)
        response_dict = json.loads(ia_response["response"])
        emotional_options = response_dict["options"]
        audio_phrase: AudioPromptSchema = {
            "text": response_dict["phrase"],
            "voice": "nova",
            "audio_name": generate_unique_audio_name(response_dict["answer"]),
            "instructions": get_voice_instructions_by_emotion(response_dict["answer"])
        }
        url_audio = await post_generate_audio(audio_phrase)
        final_emotional_options = emotional_options + [response_dict["answer"]]
        random.shuffle(final_emotional_options)
        phrase_exercice: ExercicesSchema = {
            "audio": url_audio["audio_url"],
            "question": "¿Qué emoción es?",
            "answer": response_dict["answer"],
            "options": final_emotional_options,
            "image_options": get_option_images_url(final_emotional_options),
            "type": "Escucha emoción",
            "subtype": "emocional"
        }
        phrase_exercies.append(phrase_exercice)
    return phrase_exercies
        


async def create_initial_exercises(asd_profile: dict):
    story_exercices = await generate_stories_exercices(asd_profile)
    listen_exercices = await generate_listen_exercices(asd_profile)

    total_exercices = story_exercices + listen_exercices
    user_exercices = []
    for exercice in total_exercices:
        response = await create_exercice(exercice)
        if response:
            user_exercices.append(response)
    return user_exercices
    
    

