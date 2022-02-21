from django.shortcuts import render
from django.http import HttpResponse
from . import module

def split_and_run(fn, text, max_len=1000):
    result = ""
    dumps = ""
    for idx, dump in enumerate(text.split(". ")):
        dumps += dump + ". "

        if len(dumps) >= max_len or idx == len(text.split(". "))-1:
            result += fn(dumps)
            dumps = ""

    return result

#--- Function-based View
def ssuapgo(request):
    if request.method == 'GET':
        return HttpResponse('GET request received')

    if request.method == 'POST':
        converter = module.Converter()
        text = request.POST['content']

        # split text into sentences
        text_kor = split_and_run(converter.trans_with_papago, text)
        text_sum = converter.summ_with_sumz3(text_kor)

        response = HttpResponse(text_sum)
        response["Access-Control-Allow-Origin"] = "*"
        return response
