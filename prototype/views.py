from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . import serializers  # Import your serializer (explained in step 4)
import google.generativeai as genai
import os
from .models import PrevRoadmap
from django.conf import settings
import json
# Create your views here.
def roadmap(request):
    prev_roadmaps=PrevRoadmap.objects.all()
    return render(request,'prototype/roadmap.html', context={"prev_roadmaps":prev_roadmaps})



api_key = settings.API_KEY
genai.configure(api_key=api_key)
generation_config=settings.GENERATION_CONFIG
model = genai.GenerativeModel(
  model_name="gemini-1.5-pro",
  generation_config=generation_config,
  # safety_settings = Adjust safety settings
  # See https://ai.google.dev/gemini-api/docs/safety-settings
  system_instruction="You are an expert in Computer Engineering, Data Science and any Field related to Computers, also in Finance, MBA.You also know very much in very detail about careers like Plumbing, Electrician etc. You are a Mentor to all the people who are beginners in a certain field, they will come to you and ask for your mentorship in prompt,based on their details you have to detect what is their field of interest or the job profile which they want to apply and give them all the necessary technologies/frameworks/things they need to learn in order to get a real job in that field, also tell approximate time for each technology/item to learn along with description of the technology/item and why is it crucial to get into their feild of interest of their dream job role. also give all the item they need to learn in chronological order which they should ideally learn along with approximate time for each thing and approximate total time to complete roadmap, The output of every response should be in a same structure as we are picking data from your JSON fields from your response and powering our javascript roadmap from those values. so each response should compulsarily follow same structure. Also the roadmap should be extensive and should mention all the small and big skills needed",
)
chat_session = model.start_chat(
  history=[
    {
      "role": "user",
      "parts": [
        "hii, generate a roadmap for a LLMOps Engineer",
      ],
    },
    {
      "role": "model",
      "parts": [
        "```json\n{\"title\": \"LLMOps Engineer Roadmap\", \"description\": \"This roadmap outlines the essential skills and technologies necessary to become an LLMOps Engineer, focusing on the deployment, management, and scaling of Large Language Models (LLMs).\", \"totalTime\": \"12-18 Months\", \"roadmap\": [{\"name\": \"Foundational Skills\", \"duration\": \"4-6 Months\", \"skills\": [{\"name\": \"Programming\", \"description\": \"Solid programming skills are crucial, particularly in Python, for interacting with LLMs, building pipelines, and automating tasks.\", \"time\": \"2-3 Months\"}, {\"name\": \"Version Control (Git)\", \"description\": \"Understanding Git is essential for collaborating on code, managing different versions of your LLM pipelines, and tracking changes effectively.\", \"time\": \"2 Weeks\"}, {\"name\": \"Cloud Computing Basics (AWS, Azure, GCP)\", \"description\": \"Familiarize yourself with cloud platforms like AWS, Azure, or GCP, as LLMs often require significant computational resources best handled in the cloud.\", \"time\": \"1 Month\"}]}, {\"name\": \"Core LLMOps Concepts\", \"duration\": \"3-4 Months\", \"skills\": [{\"name\": \"LLM Fundamentals\", \"description\": \"Grasp the basics of how LLMs work, different LLM architectures (Transformers, etc.), and their strengths and limitations.\", \"time\": \"1 Month\"}, {\"name\": \"Model Deployment\", \"description\": \"Learn to deploy LLMs for inference using frameworks like TensorFlow Serving, TorchServe, or dedicated platforms like Hugging Face Inference Endpoints.\", \"time\": \"1 Month\"}, {\"name\": \"Model Monitoring & Logging\", \"description\": \"Implement monitoring systems to track LLM performance, identify potential issues like model drift, and ensure reliability in production.\", \"time\": \"2 Weeks\"}, {\"name\": \"Containerization (Docker)\", \"description\": \"Master Docker to package your LLM applications and dependencies into containers, making them portable and consistent across environments.\", \"time\": \"2 Weeks\"}]}, {\"name\": \"Advanced LLMOps Practices\", \"duration\": \"4-6 Months\", \"skills\": [{\"name\": \"Orchestration & Pipelines (Kubernetes)\", \"description\": \"Explore Kubernetes for orchestrating containerized LLM deployments, managing scaling, and ensuring high availability.\", \"time\": \"2 Months\"}, {\"name\": \"MLOps Tools & Platforms\", \"description\": \"Gain experience with MLOps platforms like MLflow, Kubeflow, or cloud-specific offerings to streamline your LLM workflows.\", \"time\": \"1 Month\"}, {\"name\": \"Model Optimization\", \"description\": \"Dive into techniques like quantization, pruning, and distillation to optimize LLM size and inference speed for better performance.\", \"time\": \"1 Month\"}, {\"name\": \"Security & Ethical Considerations\", \"description\": \"Understand the security risks and ethical implications associated with LLMs, learning best practices for responsible LLM deployment.\", \"time\": \"2 Weeks\"}]}, {\"name\": \"Continuous Learning\", \"duration\": \"Ongoing\", \"skills\": [{\"name\": \"Stay Updated\", \"description\": \"The LLM landscape is rapidly evolving.  Continuously learn about new model architectures, techniques, and tools to remain at the forefront of LLMOps.\", \"time\": \"Ongoing\"}]}]}\n\n```",
      ],
    },
  ]
)
class ProcessPromptView(APIView):
    def post(self, request):
        serializer = serializers.PromptSerializer(data=request.data)
        if serializer.is_valid():
            prompt = serializer.validated_data['prompt']

            # Replace with your actual chat session logic
            response = chat_session.send_message(prompt)

            return Response({'response': response.text}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
class SaveEmitPromptView(APIView):
    def get(self, request):
        roadmaps = PrevRoadmap.objects.all()
        serializer = serializers.RoadmapSerializer(roadmaps, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = serializers.RoadmapSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class GetRoadmapView(APIView):
    def get(self, request, pk):
        try:
            roadmap = PrevRoadmap.objects.get(pk=pk)
            # Extract the 'response' field from the object and convert it to a proper JSON
            raw_response = roadmap.response  # This is a string in JSON format
            
            # Assuming the 'response' field contains JSON data inside as a string
            response_json = json.loads(raw_response)  # Convert the string into a dictionary

            # Return the filtered 'response' part, which is a valid JSON
            return Response(response_json, status=status.HTTP_200_OK)
            
        except PrevRoadmap.DoesNotExist:
            return Response({'error': 'Roadmap not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': f'An error occurred: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, pk):
        try:
            roadmap = PrevRoadmap.objects.get(pk=pk)
            roadmap.delete()
            return Response({'message': 'Roadmap deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except PrevRoadmap.DoesNotExist:
            return Response({'error': 'Roadmap not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': f'An error occurred: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def main_roadmap(request):
    return render(request,'prototype/main_roadmap.html')

def test_roadmap(request):
    return render(request,'prototype/test_roadmap.html')