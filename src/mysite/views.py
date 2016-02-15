from django.http import HttpResponse
from nltk.tokenize import word_tokenize
from django.shortcuts import render
import nltk
import json
from nltk.corpus import wordnet
from django.views.decorators.csrf import csrf_exempt


def index(request):
    return render(request, 'nltk.html', {})


@csrf_exempt
def postag(request):
    list = []
    print(request.POST['document'])
    texts = nltk.word_tokenize(request.POST['document'])
    tags = nltk.pos_tag(texts)

    for word in tags:
        list.append([word[0],word[1]])

    kk = json.dumps({'list': list})
    return HttpResponse(kk)



@csrf_exempt
def synsets(request):
    list = []
    name = request.POST['word'].lower()
    type = request.POST['pos'].lower()
    syn = wordnet.synsets(name)
    difIndex = 0
    for synset in syn:
        if(synset.pos()!=type):
            continue

        compIndex = difIndex
        while True:
            if(name[:compIndex]!=synset.name()[:compIndex]):
                break
            else: compIndex=compIndex+1

        if(difIndex<compIndex):
            list=[]
            difIndexs = compIndex
            list.append(synset.name())
            list.append(synset.definition())
        elif(difIndex==compIndex):
            list.append(synset.name())
            list.append(synset.definition())

    if(len(list)==0):
        list.append('not found in wordnet')
    kk = json.dumps({'list': list})
    return HttpResponse(kk)