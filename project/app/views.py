import csv
import xlwt
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
    sheet1 = wb.add_sheet("sample1")
    

    for post in Post.objects.all():
        row_list = [post.pk, post.title, post.text, post.category.name]
        sheet1.write(0,0, row_list[0])
        sheet1_row_1 = sheet1.row(0)
        sheet1_row_1.write(1, row_list[0])
    
    
    wb.save(response)

    return response

'''
    sheet1_row_1 = sheet1.row(0)
    sheet1_row_1.write(0, row[0])
    sheet1_row_1.write(1, row[1])
    sheet1_row_1.write(2, row[2])
    sheet1_row_1.write(3, row[3])
'''
