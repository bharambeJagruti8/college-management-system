from django.shortcuts import render
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.conf import settings
import json
import urllib.request
import urllib.error

@login_required
def roadmap_index(request):
    return render(request, 'study_roadmap/study_roadmap.html')

@login_required
def generate_plan(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST only'}, status=405)

    try:
        body = json.loads(request.body)
        topics = body.get('topics', [])

        topics_str = ', '.join([f"{t['name']}: {t['strength']}/10" for t in topics])

        payload = json.dumps({
            "model": "claude-sonnet-4-20250514",
            "max_tokens": 1000,
            "system": """You are a study planner for engineering students.
Return ONLY a valid JSON object, no markdown, no backticks, no extra text.
Format:
{
  "summary": "2-line summary in Hinglish",
  "tasks": [
    {"subject": "name", "task": "specific task", "duration": "30 min", "priority": "high"}
  ],
  "tip": "one motivational tip in Hinglish"
}
Generate 4-6 tasks. Focus most on weak subjects (low scores). Priority: high/medium/low.""",
            "messages": [{
                "role": "user",
                "content": f"Student subject strengths: {topics_str}. Generate today's personalized study plan."
            }]
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
            raw = data['content'][0]['text'].strip()
            plan = json.loads(raw)
            return JsonResponse({'plan': plan})

    except urllib.error.HTTPError as e:
        return JsonResponse({'error': e.read().decode('utf-8')}, status=500)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
# Create your views here.
