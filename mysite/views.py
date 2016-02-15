from django.http import HttpResponse
from nltk.tokenize import word_tokenize
from django.shortcuts import render
import nltk
import json
from nltk.corpus import wordnet


ks = word_tokenize("Hello World. It's goot to see you. Thanks for buying this book.")

def hello(request):
    kk = json.dumps({'list': ks})
    return HttpResponse(kk)

def hello2(request):
    return HttpResponse(request.GET['test'])

from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def hello3(request):
    list = []
    print(request.POST['test'])
    texts = nltk.word_tokenize(request.POST['test'])
    tags = nltk.pos_tag(texts)

    for word in tags:
        list.append([word[0],word[1]])

    kk = json.dumps({'list': list})
    return HttpResponse(kk)

def index(request):
    return render(request, 'nltk.html', {})

def difIndex(str1, str2):
    index = 0
    while True:
        if(str1[:index]!=str2[:index]):
            break
        else: index=index+1
    return index

@csrf_exempt
def hello4(request):
    list = []
    name = request.POST['test'].lower()
    type = request.POST['type'].lower()
    syn = wordnet.synsets(name)
    difIndexs = 0
    compIndex = 0
    for synset in syn:
        if(synset.pos()!=type):
            continue

        compIndex = difIndex(name, synset.name())
        if(difIndexs<compIndex):
            list=[]
            difIndexs = compIndex
            list.append(synset.name())
            list.append(synset.definition())
        elif(difIndexs==compIndex):
            list.append(synset.name())
            list.append(synset.definition())

    if(len(list)==0):
        list.append('not found in wordnet')
    kk = json.dumps({'list': list})
    return HttpResponse(kk)