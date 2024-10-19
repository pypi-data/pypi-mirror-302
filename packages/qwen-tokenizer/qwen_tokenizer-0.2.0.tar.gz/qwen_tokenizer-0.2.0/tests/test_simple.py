# @Author: Bi Ying
# @Date:   2024-08-14 15:49:21
from qwen_tokenizer import get_tokenizer


qwen_tokenizer = get_tokenizer("qwen2.5-72b-instruct")
chat_tokenizer_dir = "./"
text = "Hello! 毕老师！1 + 1 = 2 ĠÑĤÐ²ÑĬÑĢ"

result = qwen_tokenizer.encode(text)
print(result)
