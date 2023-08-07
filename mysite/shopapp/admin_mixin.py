import csv
from django.db.models import QuerySet
from django.db.models.options import Options
from django.http import HttpRequest, HttpResponse


#позволяет скачать csv файл и этот класс можно подмешивать в другие админки
class ExportAsCSVMixin:
    def export_csv(self, request: HttpRequest, queryset: QuerySet):
        meta: Options = self.model._meta #предоставляет весь список полей модели
        field_names = [field.name for field in meta.fields] #получение всех имен полей (строка)
        response = HttpResponse(content_type='text/csv') #подготовка объекта, в который будут выводиться данные

        # скачивание файла уже с готовым именем
        response['Content-Disposition'] = f'attachment; filename={meta}-export.csv'

        #запись результата
        csv_writer = csv.writer(response)

        # запись заголовков
        csv_writer.writerow(field_names)

        #запись объектов
        for obj in queryset:
            csv_writer.writerow([getattr(obj, field) for field in field_names])

        return response

    #описание действия в админке
    export_csv.short_description = 'Export as CSV'
