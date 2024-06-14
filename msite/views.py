from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from msite.models import Dailybind, Cardtyperef, Registercard
from msite import forms
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.template import loader
from django import template
from django.db import transaction
from rest_framework.generics import GenericAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import serializers
from msite.serializers import DailybindSerializer, CardtyperefSerializer, RegistercardSerializer 
from tool import xstr
from datetime import date

# Create your views here.
@login_required(login_url='/login/')
def Index(request):
    return render(request, "index.html", locals())

def Login(request):
    if request.method == 'POST':
        loginForm = forms.LoginForm(request.POST)
        if loginForm.is_valid():
            login_account = request.POST['Account'].strip()
            login_password = request.POST['Password']

            try:
                user = authenticate(request, username=login_account, password=login_password)

                if user is not None:
                    login(request, user)
                    messages.success(request, "登入成功")
                    return redirect('/')
                else:
                    messages.warning(request, "帳號或密碼錯誤")

            except:
                messages.warning(request, "找不到使用者")
        else:
            messages.warning(request, "請檢查輸入內容")
    else:
        loginForm = forms.LoginForm()
    return render(request, "login.html", locals())

def history(request):
    results = None
    print("begin")

    if request.method == "POST":
        # 獲取用戶提交的日期條件
        start_date = request.POST.get("start_date")
        end_date = request.POST.get("end_date")

        # 在這裡執行查詢操作，使用你的模型和日期條件
        if xstr(start_date) == '' and xstr(end_date) == '':
            results = Dailybind.objects.all()
        elif  xstr(start_date) == '' and xstr(end_date) != '':
            results = Dailybind.objects.filter(LogDate__lte=end_date)
        elif xstr(end_date) == '' and  xstr(start_date) != '':
            results = Dailybind.objects.filter(LogDate__gte=start_date)
        else:
            results = Dailybind.objects.filter(LogDate__range=[start_date, end_date])

    return render(request, "history.html", locals())



def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]
        context['segment'] = load_template

        html_template = loader.get_template(load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('Page_404.html')
        return HttpResponse(html_template.render(context, request))

    except:

        html_template = loader.get_template('Page_500.html')
        return HttpResponse(html_template.render(context, request))
    
class DailybindView(GenericAPIView):
    serializer_class = DailybindSerializer
    def get(self, request, *args, **krgs):
        queryset = Dailybind.objects.all()
        #dailybinds = self.get_queryset()
        start_date=request.query_params.get('start_date', None)
        end_date=request.query_params.get('end_date', None)
        if start_date:
            queryset = queryset.filter(LogDate__gte=start_date)
        if end_date:
            queryset = queryset.filter(LogDate__lte=end_date)
        serializer = self.serializer_class(queryset, many=True)
        data = serializer.data
        return JsonResponse(data, safe=False)
    def post(self, request, *args, **krgs):
        data = request.data
        try:
            serializer = self.serializer_class(data=data)
            serializer.is_valid(raise_exception=True)
            with transaction.atomic():
                serializer.save()
            data = serializer.data
        except Exception as e:
            data = {'error': str(e)}
        return JsonResponse(data)

class CardtyperefView(GenericAPIView):
    queryset = Cardtyperef.objects.all()
    serializer_class = CardtyperefSerializer
    def get(self, request, *args, **krgs):
        cardtypes = self.get_queryset()
        serializer = self.serializer_class(cardtypes, many=True)
        data = serializer.data
        return JsonResponse(data, safe=False)

class RegisterCardView(GenericAPIView):
    serializer_class = RegistercardSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['cardno', 'cardid']  # 指定要过滤的字段
    def get(self, request, *args, **krgs):
        queryset = Registercard.objects.all()
        cardno=request.query_params.get('cardno', None)
        cardid=request.query_params.get('cardid', None)
        if cardno:
            queryset = queryset.filter(cardno=cardno)
        if cardid:
            queryset = queryset.filter(cardid=cardid)
        registercards = queryset
        serializer = self.serializer_class(registercards, many=True)
        data = serializer.data
        return JsonResponse(data, safe=False)
    
    def post(self, request, *args, **krgs):
        data=request.data
        serializer = self.serializer_class(data = data)

        try:
            if(data['cardno'] == ''):
                raise Exception("卡號不可為空")
            existing_data = Registercard.objects.filter(cardno=data['cardno'])
            if existing_data.exists():
                raise Exception('卡號:' + data['cardno'] +' 已存在')
            if serializer.is_valid():
                serializer.save()
                return HttpResponse(status = 201)
            else:
                errors = serializer.errors
                raise Exception(errors)
            
        except Exception as e:
            #messages.warning(request, str(e))
            #print(e)
            return JsonResponse(status = 500, data={'error': str(e)})
    def delete(self, request, *args, **krgs):
        data=request.data.get('data', [])
        print(data)
        try:
            for item in data:
                pk = item
                deleteItem = Registercard.objects.get(pk=pk)
                deleteItem.delete()
            return HttpResponse(status = 204)
        except Exception as e:
            return JsonResponse(status = 500, data={'error': str(e)})
        
class RegisterCardBatchView(GenericAPIView):
    serializer_class = RegistercardSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['cardno', 'cardid']  # 指定要过滤的字段
        
    def post(self, request, *args, **krgs):
        data=request.data
        print(data)
        cardversion = data['cardversion']
        cardspecial = data['cardspecial']
        versions = data['versions']
        start = int(data['start'])
        end = int(data['end'])

        try:
            if start > end:
                raise Exception('編號請由小到大')
            for i in range(start, end+1):
                if cardspecial == '':
                    CardNo = cardversion + '-' + versions + str(i).zfill(3)
                else:
                    CardNo = cardversion + '-' + versions + cardspecial + str(i).zfill(2)

                existing_data = Registercard.objects.filter(cardno=CardNo)
                if not existing_data.exists():
                    serializer = self.serializer_class(data = {'cardno': CardNo})
                    if serializer.is_valid():
                        serializer.save()
            return HttpResponse(status = 201)            
        except Exception as e:
            #messages.warning(request, str(e))
            #print(e)
            return JsonResponse(status = 500, data={'error': str(e)})
        
class RutenCompare(GenericAPIView):
    def post(self, request, *args, **krgs):
        data = request.data
        queryset = Dailybind.objects.all()

        try:
            for item in data:
                cardno = item['cardno']
                cardnumber = item['cardnumber']
                
                if(not queryset.filter(CardNo=cardno, LogDate = date.today()).exists()):
                    raise Exception('查無卡號:' + cardno + ' 今天的紀錄')
            
            
            return JsonResponse(data, safe=False)
        except Exception as e:
            return JsonResponse(status = 500, data={'error': str(e)})