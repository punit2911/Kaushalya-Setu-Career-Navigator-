import requests
from django.http import JsonResponse

def process_prompt(request):
    if request.method == 'POST':
        prompt = request.POST.get('prompt')
        if prompt:
            # Replace with your actual Gemini API key
            GEMINI_API_KEY = 'AIzaSyDlX5LfqNdiROBZd4YmNSrznocJbxfY6Ms'

            headers = {
                'Authorization': f'Bearer {GEMINI_API_KEY}'
            }
            url = 'https://api.llamalabs.com/generate'

            payload = {
                "text": prompt,
                "model": "gemini-1.5-flash",
                # Adjust parameters as needed
            }

            response = requests.post(url, headers=headers, json=payload)
            if response.status_code == 200:
                result = response.json()
                return JsonResponse({'response': result['text']})
            else:
                return JsonResponse({'error': 'Error processing prompt'}, status=500)
        else:
            return JsonResponse({'error': 'Prompt is required'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)