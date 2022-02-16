from django.shortcuts import render
from django.http import HttpResponse
from . import module

#--- Function-based View
def ssuapgo(request):
    if request.method == 'GET':
        return HttpResponse('GET request received')

    if request.method == 'POST':
        converter = module.Converter()
        text = request.POST['content']

        # split text into sentences
        text_kor = ""
        for dump in text.split(". "):
            text_kor += converter.trans_with_papago(dump)
        text_sum = converter.summ_with_sumz3(text_kor)

        response = HttpResponse(text_sum)
        response["Access-Control-Allow-Origin"] = "*"
        return response
