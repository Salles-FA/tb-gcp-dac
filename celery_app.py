from celery import Celery

# print("DEBUG: {}".format(os.environ['DEBUG']))

CELERY_BROKER_URL = 'redis://localhost:6379',
CELERY_RESULT_BACKEND = 'redis://localhost:6379'

celery = Celery(
    'worker',
    backend=CELERY_RESULT_BACKEND,
    broker=CELERY_BROKER_URL
)

# def make_celery(app):
#     celery = Celery(
#         app.import_name,
#         backend=app.config['CELERY_RESULT_BACKEND'],
#         broker=app.config['CELERY_BROKER_URL']
#     )
#     celery.conf.update(app.config)
#
#     class ContextTask(celery.Task):
#         def __call__(self, *args, **kwargs):
#             with app.app_context():
#                 return self.run(*args, **kwargs)
#
#     celery.Task = ContextTask
#     return celery
#
# celery = make_celery(self)

#
# @celery.task()
# def func1(arg):
#     ...
#     return ...
