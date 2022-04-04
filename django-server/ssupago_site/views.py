from django.shortcuts import render
from django.http import HttpResponse
from . import module

# initialize converter instance
converter = module.Converter()

#--- Function-based View
def ssuapgo(request):
    if request.method == 'GET':
        return HttpResponse('GET request received')

    if request.method == 'POST':
        text = request.POST['content']


        ## ---시간측정--- ##
        import time
        start = time.time()
        text_kor = converter.translate(text, input_size=5000)
        print("trans_time:", time.time() - start)

        start = time.time()
        text_sum = converter.summarize(text_kor, deep=True)
        print("summ_time:", time.time() - start)
        ## ---시간측정--- ##


        # send response
        response = HttpResponse(text_sum)
        response["Access-Control-Allow-Origin"] = "*"
        return response
