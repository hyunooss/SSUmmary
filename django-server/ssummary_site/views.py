from django.shortcuts import render
from django.http import HttpResponse
from . import module

# initialize converter instance
converter = module.Converter()

#--- Function-based View
def ssummary(request):
    if request.method == 'GET':
        return HttpResponse('GET request received')

    if request.method == 'POST':
        text = request.POST['content']
        deep = True if request.POST['deep'] == 'true' else False

        ## ---시간측정--- ##
        import time
        start = time.time()
        # 번역
        text_kor = converter.translate(text, input_size=5000)
        print("\n번역 소요시간:", time.time() - start)

        # 문법 검사
        start = time.time()
        text_checked_kor = converter.spell_check(text_kor)
        print("\n검사 소요시간:", time.time() - start)

        start = time.time()
        # 요약
        text_sum = converter.summarize(text_checked_kor, deep=deep)
        if deep == True: print("깊은 ", end="")
        else: print("얕은 ", end="")
        print("요약 소요시간:", time.time() - start)
        ## ---시간측정--- ##


        # send response
        response = HttpResponse(text_sum)
        response["Access-Control-Allow-Origin"] = "*"
        return response
