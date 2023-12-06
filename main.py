import pickle
import database as db
import anime_name_recognition as rec


def message(func):
    def in_func(event, *args):
        text = func(event, *args)
        ans = {
            'version': event['version'],
            'session': event['session'],
            'response': {
                'text': text,
                'end_session': 'false'
            },
        }
        return ans
    return in_func


@message
def start_message(event):
    size = db.get_database_size()
    return 'Привет! Если вы дадите мне название аниме я подскажу похожие.' + \
           f'У меня в базе целых {size} отличных вариантов!'


@message
def unsure_anime_message(event, user_anime):
    index = user_anime['id']
    anime = db.get_anime_dict(index)
    text = f'Кажется вы спросили про: {anime["name"]}' + \
           'но я не уверена. Пожалуйста попробуйте спросить по другому'
    return text


@message
def recommendation_message(event, user_anime):
    anime_id = user_anime['id']
    with open('30rec.pickle', 'rb') as file:
        data = pickle.load(file)
    recs = data[anime_id]
    animes = [db.get_anime_dict(n) for n in recs]
    filtered_animes = rec.remove_seasons(user_anime, animes)
    top3 = filtered_animes[:3]

    def anime_to_text(anime: dict, limit=250):
        text = f'"{anime["name"].strip()}" ({anime["age-rating"]}):\n'
        text += f'{anime["genres"]}\n'
        text += f'{anime["period"]}\n'
        text += anime["description"]
        return text[:limit-4] + '...\n\n'

    answer = f'Нашла что-то похожее на {user_anime["name"].strip()}:\n'
    for i in range(3):
        answer += anime_to_text(top3[i])

    answer += 'Также стоит взглянуть на:\n'
    k = 3
    while True:
        added_anime = filtered_animes[k]
        name = f'{added_anime["name"]} ({added_anime["age-rating"]})\n'
        if len(answer + name) > 1024:
            break
        k += 1
        answer += name
    return answer


def handler(event, context):
    """
    Entry-point for Serverless Function.
    :param event: request payload.
    :param context: information about current execution context.
    :return: response to be serialized as JSON.
    """
    text = None
    if 'request' in event and \
            'original_utterance' in event['request'] \
            and len(event['request']['original_utterance']) > 0:
        text = event['request']['original_utterance']

    if text is None:
        answer = start_message(event)
    else:
        anime_ids = rec.NamesIds()
        anime_id, distance = anime_ids.find_id_and_distance(text)
        user_anime = db.get_anime_dict(anime_id)
        name_len = len(user_anime['name'])
        input_len = len(text)
        best_case_distance = input_len - name_len
        #info = (distance, best_case_distance, name_len)
        if distance - best_case_distance > name_len * .2:
            answer = unsure_anime_message(event, user_anime)
        else:
            answer = recommendation_message(event, user_anime)

    return answer
