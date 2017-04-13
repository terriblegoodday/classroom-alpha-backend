from django.shortcuts import render
from django.http import HttpResponse
from mathgenapp.models import GeneratedTask
from mathgenapp.models import SolvedTask
from mathgenapp.dispatcher import getAvailableGenerators
import mathgenapp.utils as utils
import json
from time import sleep
import pdb
from django.views.decorators.csrf import csrf_exempt
import logging
import warnings
from django.utils import timezone

def index(request):
    # Главная страница, отображает 10 рандомных заданий
    objects = map(lambda x: "<hr />" + x.task_object, GeneratedTask.tasks.all()[:10])
    return HttpResponse(objects)

def api_getTasks(request):
    """
    Апи для React
    Позволяет получать задания с определенного генератора
    (request => output)
    ({
        gen_id:str, -> ID генератора заданий
        limit:int   -> количество заданий для вывода
    } => [
        {
            task:str, -> задание
            pk:int, -> ID задания
            gen_id:int -> ID генератора заданий
        },
        ...
    ])
    """

    # Получаем запрос FrontEnd
    request = request.GET
    gen_id = request.get('gen_id')
    limit = int(request.get('limit'))

    # Найти уже сгенерированные объекты с ID генератора из вводных данных и
    # сгенерировать недостающие (точнее наоборот)
    objects = set()

    while len(objects) != limit:
            x = GeneratedTask.tasks.generate(gen_id)
            if x not in objects:
                objects.add(x)

    def prepare(x):
        prepared_Task = {}
        # Загружаем текст из json-объекта задания
        task_object = json.loads(x.task_object)
        task_str = task_object['task']


        """
        {
            task:str, -> задание
            pk:int, -> ID задания
            gen_id:int -> ID генератора заданий
        },
        """
        prepared_Task['task'] = task_str
        prepared_Task['pk'] = x.pk
        prepared_Task['gen_id'] = x.generator_id
        prepared_Task['fields'] = []
        for ik,la in task_object['answers'].items():
            if ik == "_replaceable":
                for vg, ds in la.items():
                    for i in ds:
                        prepared_Task['fields'].append({"placeholder": i['placeholder']})
            else:
                prepared_Task['fields'].append({"placeholder": la['placeholder']})

        return prepared_Task



    objects = list(map(prepare, objects))

    response = HttpResponse(json.dumps(objects), content_type="application/json")
    response['AllowedOrigin'] = '*'
    response['AllowedHeader'] = 'origin, x-requested-with'

    return response

@csrf_exempt
def api_reviewAnswers(request):
    """
    Апи для React
    Проверить правильность ответов на задания

    """
    if request.POST:
        # Просматриваем список ответов от пользователя
        answersFromUser = json.loads(request.body.decode("utf-8"))
        # Загрузить задания, чтобы потом сопоставить ответы
        objects = dict()
        for key, value in answersFromUser.items():
            key = str(key)
            objects[key] = json.loads(GeneratedTask.tasks.get(pk=key).task_object)

        # Создать список ответов
        answers = dict()
        for key, task_object in objects.items():
            answers[key] = []
            for ik, la in task_object['answers'].items():
                if ik == "_replaceable":
                    for vg, ds in la.items():
                        for i in ds:
                            answers[key].append(i['answer'])
                else:
                    answers[key].append(la['answer'])
        
        # Сравнить правильные ответы и ответы пользователя
        decision = dict()
        for key, value in answersFromUser.items():
            key = str(key)
            decision[key] = False
            for answerKey, answer in value.items():
                if answer['value'] in answers[key][int(answerKey)]:
                    decision[key] = True
                    new_solved_task = SolvedTask(generator_id=GeneratedTask.tasks.get(pk=key).generator_id, date_created=timezone.now())
                    new_solved_task.save()
        
        response = HttpResponse(json.dumps(decision), content_type="application/json")
        response['AllowedOrigin'] = '*'
        response['AllowedHeader'] = 'origin, x-requested-with'

        return response

    return HttpResponse('none')

def api_getAvailableGenerators(request):
    """
    Апи для React
    Позволяет получать доступные генераторы
    (() => [<{
        title: <str>,
        description: <str>,
        gen_id: <str>
    }>])
    """

    response = HttpResponse(json.dumps(getAvailableGenerators()), content_type="application/json")
    response['AllowedOrigin'] = '*'
    response['AllowedHeader'] = 'origin, x-requested-with'

    return response

def api_getStatistics(request):
    """
    Апи для React
    Позволяет получить статистику по сайту
    – Количество сгенерированных заданий
    - Количество решенных заданий
    - Последние 5 решенных заданий (1 колонка с строковым представлением решенного задания)
    """

    # Количество сгенерированных заданий
    generated_tasks = int(GeneratedTask.tasks.count() / 2)

    # Количество решенных заданий
    solved_tasks = SolvedTask.objects.count()

    # Последние 5 решенных заданий
    last_five = list(map(str, SolvedTask.objects.order_by('-id')[:10]))

    # Объект, который отправим клиенту
    stats = {
        "generated_tasks": generated_tasks,
        "solved_tasks": solved_tasks,
        "last_five": last_five
    }

    # Отправляем ответ

    response = HttpResponse(json.dumps(stats), content_type="application/json")
    response['AllowedOrigin'] = '*'
    response['AllowedHeader'] = 'origin, x-requested-with'

    return response
