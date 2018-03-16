import csv
from xlwt import Workbook
from io import TextIOWrapper, StringIO
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views import generic
from .models import Post, Category


class IndexView(generic.ListView):
    model = Post


def csv_import(request):
    if 'csv' in request.FILES:
        form_data = TextIOWrapper(request.FILES['csv'].file, encoding='utf-8')
        csv_file = csv.reader(form_data)
        for line in csv_file:
            post,_ = Post.objects.get_or_create(pk=line[0])
            post.title = line[1]
            post.text = line[2]
            category,_ = Category.objects.get_or_create(name=line[3])
            post.category = category
            post.save()
            
    return redirect('app:index')

def csv_export(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=db.csv'
 
    writer = csv.writer(response)
    for post in Post.objects.all():
        row = [post.pk, post.title, post.text, post.category.name]
        writer.writerow(row)
 
    return response


def xls_export(request):
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content_Disposition'] = 'attachment; filename=%s' % 'report.xls'
    
    wb = Workbook()
    ws = wb.add_sheet("sample")

    ws.write(0,0, "Hello")
    ws.write(0,1, "World")
    ws.write(1,0, "Hello")
    ws.write(1,1, "Excel")

    wb.save(response)

    return response
