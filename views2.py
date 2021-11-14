import logging
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic
from .forms import InquiryForm, DiaryCreateForm
from .models import Diary
from diary import test1
from django.shortcuts import render
from .forms import UserForm #fomrsのuserformクラスをインポート

logger = logging.getLogger(__name__)

def kinmu(request):
    #フォームテンプレート
    #params = {'message': 'new2です'}
    params = {'sousa':'','name': '', 'year': '', 'month': '','day':'',
              'syukkin':'','taikin':'','kyukei':'',
              'bikou':'', 'form': None,'results2' : ''}
    if request.method == 'POST':
        form = UserForm(request.POST)
        params['sousa'] = request.POST['sousa']
        params['name'] = request.POST['name']
        params['year'] = request.POST['year']
        params['month'] = request.POST['month']
        params['day'] = request.POST['day']
        params['syukkin'] = request.POST['syukkin']
        params['taikin'] = request.POST['taikin']
        params['kyukei'] = request.POST['kyukei']
        params['bikou'] = request.POST['bikou']
        params['form'] = form

    else:
        params['form'] = UserForm()

    #DB接続
    import psycopg2
    import psycopg2.extras
    import pandas as pd

    connection = psycopg2.connect("host=localhost port=5432 dbname=postgres user=postgres password=S")
    cur = connection.cursor()

    #elif com == 'c' and params['name'] != '':
    date = params['year'] + "-" + params['month'] + "-" + params['day']
    if params['sousa'] == '削除':
        cur.execute("delete from kinmu where name=%s AND hiduke=%s",(params['name'],date))
    elif params['sousa'] == '入力':
        cur.execute("insert into kinmu(name,hiduke,syukkin,taikin,kyukei,bikou) values(%s,%s,%s,%s,%s,%s)",
        (params['name'], date, params['syukkin'], params['taikin'], params['kyukei'], params['bikou']))
    elif params['sousa'] == '更新':
        print()
    connection.commit()

    # select to_char(syukkin,'HH24:MI') from kinmu;
    cur.execute('SELECT * FROM kinmu;')
    #to_char(syukkin,'HH24:MI')
    df = pd.read_sql(sql="select *, to_char(taikin -syukkin - kyukei, 'HH24:MI') as kei,"
                         "(select to_char(sum(taikin - syukkin - kyukei),'HH24:MI') as gokei from kinmu)"
                         " from kinmu where name='" + params['name'] + "' order by hiduke;", con=connection)
    #ここにpandasで合計時間の列を追加したい
    df.to_html("diary/templates/kinmuhyo.html")
    params['results2'] = df
    cur.close()
    connection.close()
    return render(request,'kinmu.html',params)