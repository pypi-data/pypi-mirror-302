import datetime as dt
import json
import os
from .config import OPENAI_API_KEY, GOOGLE_API_KEY, DEFAULT_PROMPT
#from openai_utils import openai_init
from .gmap_utils import get_gmap_url
import openai

def get_event_gmap_info(str_input, lang='CH', **kwargs):
    """
    解析字串中的事件、時間和地點，並生成相應的Google地圖URL。

    參數:
        str_input (str): 要解析的文本。
        lang (str, 可選): 預設為 'CH'。指定回覆的語言，可以是 'CH'（中文）或 'EN'（英文）。
        **kwargs: 其他選項性參數。特別地，可以使用 'prompt_path' 參數來指定提示訊息文檔的路徑。

    讀取prompt_path檔案時的注意事項:
        格式: 請確保提詞文檔的格式是正確的，並且可以被JSON解析。
        必須欄位:
            time: 須為YYYY-mm-dd HH:MM:SS的格式
            location: 地點描述，例如"台北車站"
            event: 事件說明，例如"環保會議"
        清晰度: 提詞應該清楚明瞭，以避免模型產生歧義或不準確的回應。
        可解析: 確保提詞和模型回傳的內容都是可被JSON解析的，避免包含可能破壞JSON格式的特殊字符。

    回傳:
        dict: 包含以下鍵值：
            - 'time': 事件時間（格式為 'YYYY-MM-DD HH:MM:SS'）。
            - 'location': 事件地點。
            - 'event': 事件描述。
            - 'gmap': Google地圖的URL。
    例外:
        ValueError: 如果指定了不支援的語言。
    
    使用方式:
        result = get_event_gmap_info("包含事件、時間與地點的字串", lang='EN', prompt_path="your_prompt_path.txt")
    """
    if lang not in ['EN', 'CH']:
        raise ValueError('supported language: CH, EN')
        
    now = dt.datetime.utcnow() + dt.timedelta(hours=8)
    weekday = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
    
    #openai_init(OPENAI_API_KEY)

    prompt_path = kwargs.get('prompt_path', None)

    if prompt_path:
        with open(prompt_path, 'r', encoding='utf-8') as f:
            str_prompt = f.read()
    else:
        str_prompt = DEFAULT_PROMPT
    str_prompt = f'# This is your known information:\n「現在」(now) is defined as {now.strftime("%Y-%m-%d %H:%M:%S")}，{weekday[now.isoweekday()-1]}\n' + str_prompt + ('Please reply in English' if lang=='EN' else '請用中文回覆我')
    prompt = []
    prompt.append({
        'role': 'system',
        'content': str_prompt
    })
    prompt.append({
        'role': 'user',
        'content': f'{str_input}'
    })
    model = os.getenv('DEFAULT_MODEL') or 'gpt-4o'
    client = openai.OpenAI(api_key=OPENAI_API_KEY)
    response = client.chat.completions.create(model=model,
                                            messages=prompt,
                                            max_tokens=300)
    content = response.choices[-1].message.content
    try:
        result = json.loads(content)
        if result['status'] == 'error':
            result['data']['lat'] = None
            result['data']['lon'] = None
            result['data']['gmap'] = ''
            return result
        lat, lon, gmap_url = get_gmap_url(result['data']['location'], GOOGLE_API_KEY)
        if lat is None or lon is None:
            result['status'] = 'error'
        result['data']['lat'] = lat
        result['data']['lon'] = lon
        result['data']['gmap'] = gmap_url
        return result
    except json.decoder.JSONDecodeError:
        print(content, flush=True)
        return "抱歉, 我無法解析您的請求, 請試試換句話說" if lang == 'CH' else 'Sorry, I cannot recognize your sentence, please ask in another sentence.'
