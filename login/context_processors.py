"""
如果你在每个视图函数里都重复读取会话（session）数据并传递给模板，
代码会变得冗余。Django 提供了上下文处理器（Context Processors）来解决这个问题，
它能让你在所有模板里都可以使用某些变量，而无需在每个视图函数里重复传递。
实现步骤
1. 创建上下文处理器函数
首先，在你的项目里创建一个 Python 文件，例如在某个应用（比如 utils 应用，你可以按需创建）下创建 context_processors.py 文件，
然后在该文件中编写上下文处理器函数。
2. 配置上下文处理器
在你的项目的 settings.py 文件里，
找到 TEMPLATES 设置项，在 OPTIONS 里的 context_processors 列表中添加你刚刚创建的上下文处理器函数。
3. 在模板中使用会话数据
现在，你可以在任何模板里直接使用 login_info 变量来显示登录信息了，无需在每个视图函数里手动传递。
"""


def login_info(request):
    user_info = {}
    if 'user_id' in request.session:
        user_info = {
            'user_id': request.session.get('user_id'),
            'username': request.session.get('username'),
            'privileges': request.session.get('privileges'),
            'department': request.session.get('department'),
            'department_code': request.session.get('department_code'),
            'employee_name': request.session.get('employee_name')
        }
    return {'login_info': user_info}
