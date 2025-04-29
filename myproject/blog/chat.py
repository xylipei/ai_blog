import os
import json
from django.http import JsonResponse
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage
from django.http import JsonResponse, StreamingHttpResponse

load_dotenv(dotenv_path=os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '.env'))

def chat_with_ai(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message')
            user_id = data.get('userid', 'default_user')
            print(f"Received message: {user_message}, User ID: {user_id}")
            if not user_message:
                return JsonResponse({'error': 'No message provided'}, status=400)

            openai_api_key = os.getenv("OPENAI_API_KEY")
            if not openai_api_key or openai_api_key == "YOUR_OPENAI_API_KEY":
                return JsonResponse({'reply': '抱歉，我的大脑（OpenAI API Key）还没配置好，暂时无法回复。请联系管理员设置OpenAI API Key。'})

            chat_model = ChatOpenAI(
                api_key=openai_api_key,
                model="deepseek-chat",
                temperature=0.7,
                streaming=True  # 启用流式输出
            )

            # 定义提示词模板
            prompt_template = """你是一个专业的博客助手，你的名字为：可乐不加冰，请用中文回答用户的问题。
            回答要求：
            - 保持专业但友好的语气
            - 回答简洁明了，不超过200字
            - 如果问题与博客内容相关，优先参考博客文章回答
            - 避免提供医疗、法律等专业建议
            
            用户问题：{user_input}"""
            
            # 定义流式响应生成器
            def stream_response_generator():
                try:
                    formatted_prompt = prompt_template.format(user_input=user_message)
                    for chunk in chat_model.stream([HumanMessage(content=formatted_prompt)]):
                        if chunk.content:
                            yield chunk.content
                except Exception as e:
                    print(f"Error during streaming: {e}")
                    yield f"Error: {str(e)}"

            # 返回 StreamingHttpResponse
            response = StreamingHttpResponse(stream_response_generator(), content_type='text/plain')
            return response

        except Exception as e:
            print(f"Error processing request: {e}")
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Only POST method is allowed'}, status=405)
