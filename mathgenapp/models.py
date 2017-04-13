from django.db import models
from jsonfield import JSONField
from mathgenapp.dispatcher import generate as generate_task
import datetime
from django.utils import timezone
import logging, logging.handlers

logger = logging.getLogger("djangosyslog")
hdlr = logging.handlers.SysLogHandler(facility=logging.handlers.SysLogHandler.LOG_DAEMON)
formatter = logging.Formatter('%(filename)s: %(levelname)s: %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)

class GeneratedTaskManager(models.Manager):

    def generate(self, gen_id):
        # Проверяем задание на дублирование
        # Если 5 раз не получилось сгенерировать уникальное, то
        # пришла пора смириться и выдать пользователю задание из БД
        exists_count = 0
        # В 21:17 объект заданий
        t = 0 # Количество попыток генерации нового задания
        while t == 0 or GeneratedTask.tasks.filter(task_object=t).exists():
            if exists_count == 5:
                return GeneratedTask.tasks.get(task_object=t)
            else:
                t = generate_task(gen_id)
                exists_count += 1

        # g = generator_id
        g = gen_id
        d = timezone.now()
        return super().create(generator_id=g, task_object=t, date_created=d)


class GeneratedTask(models.Model):

    class Meta:
        verbose_name = "Задание"
        verbose_name_plural = "Задания"
        get_latest_by = "date_created"
        ordering = ['?']

    task_object = JSONField(verbose_name="Объект задания")
    generator_id = models.CharField(max_length=100, verbose_name="ID генератора")
    tasks = GeneratedTaskManager()
    date_created = models.DateTimeField(verbose_name="Дата создания")

    def __str__(self) :
        return self.task_object

class SolvedTask(models.Model):

    class Meta:
        verbose_name = "Решенное задание"
        verbose_name_plural = "Решенные задания"
        get_latest_by = "date_created"

    generator_id = models.CharField(max_length=100, verbose_name="ID генератора")
    date_created = models.DateTimeField(verbose_name="Дата создания")

    def __str__(self):
        return "{0} -- {1}".format(self.date_created, self.generator_id)
