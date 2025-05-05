from django.shortcuts import render, redirect
from openai import OpenAI
from forum.models import Ticket
from Aianswers.models import AiAnswer
# Create your views here.
client = OpenAI(
        base_url = "http://localhost:11434/v1",
        api_key = "ollama"
    )
def AiAnswerCreate(pk):
    def generate_responce(text, time=30, max_length=250):
        response = client.chat.completions.create(
        model="mistral", 
        messages=[
            {"role": "user", "content": f"{text}"}
        ],
        max_tokens=max_length ,
        temperature = 0.5,
        timeout=time,
        )
        return response.choices[0].message.content


    ticket = Ticket.objects.get(id=pk)
    text = ticket.description
    ai_answer = generate_responce(text, 60, 400)
    Ai_answer = AiAnswer.objects.create(ticket=ticket)
    Ai_answer.text = ai_answer
    Ai_answer.save()
    return redirect("ticket-details", pk=ticket.pk)
