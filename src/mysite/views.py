from django.http import HttpResponse
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

def difIndex(str1, str2):
    index = 0
    while True:
        if(str1[:index]!=str2[:index]):
            break
        else: index=index+1
    return index

@csrf_exempt
def synsets(request):
    list = []
    name = request.POST['word'].lower()
    type = request.POST['pos'].lower()
    syn = wordnet.synsets(name)
    difIndexs = 0
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