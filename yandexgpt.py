import openai

YANDEX_CLOUD_MODEL = "yandexgpt-lite"

YANDEX_CLOUD_FOLDER = "FOLDER"

YANDEX_CLOUD_API_KEY = "API_KEY"

def get_filtered_values(csv):
    with open("example.csv", encoding="utf-8") as f:
        exported_file = f.read()

    client = openai.OpenAI(
        api_key=YANDEX_CLOUD_API_KEY,
        base_url="https://rest-assistant.api.cloud.yandex.net/v1",
        project= YANDEX_CLOUD_FOLDER
    )

    response = client.responses.create(
        model=f"gpt://{YANDEX_CLOUD_FOLDER}/{YANDEX_CLOUD_MODEL}",
        input=f"У меня есть файл с продутками из магаизнов. Верни мне продукты в таком же формате, только замени похожие продукты"
              f"правильными/полными названиями, чтобы один и тот же товар (даже из разных магазинов) назывался одинаково и поставь все названия в кавычки.\n{exported_file}",
        temperature=0.8,
        max_output_tokens=1500
    )

    return response.output[0].content[0].text
