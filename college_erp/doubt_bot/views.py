from django.shortcuts import render
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.conf import settings
import json
import urllib.request
import urllib.error

@login_required
def doubt_bot_index(request):
    subjects = ['General', 'Mathematics', 'Physics', 'Programming', 'Electronics']
    return render(request, 'doubt_bot/doubt_bot.html', {'subjects': subjects})

@login_required
def ask_doubt(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST only'}, status=405)

    try:
        body = json.loads(request.body)
        messages = body.get('messages', [])
        subject = body.get('subject', 'General')

        payload = json.dumps({
            "model": "claude-sonnet-4-20250514",
            "max_tokens": 800,
            "system": f"""You are a helpful study assistant for engineering students at EDUCORE college.
The student is asking about {subject}.
Answer clearly and concisely with step-by-step explanations where needed.
You can respond in Hinglish if the student writes in Hindi.""",
            "messages": messages
        }).encode('utf-8')

        req = urllib.request.Request(
            "https://api.anthropic.com/v1/messages",
            data=payload,
            headers={
                "Content-Type": "application/json",
                "x-api-key": settings.ANTHROPIC_API_KEY,
                "anthropic-version": "2023-06-01",
            },
            method="POST"
        )

        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            answer = data['content'][0]['text']
            return JsonResponse({'answer': answer})

    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8')
        return JsonResponse({'error': f'API error: {error_body}'}, status=500)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
# Create your views here.
