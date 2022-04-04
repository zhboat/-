from django.shortcuts import render

# 主页
def home(request):
    return render(request, 'index.html')
# 登录
def login(request):
    # 懒得写注册，密码校验了...0-0
    return render(request, 'login.html')
# 公司规模
def company_size(request):
    return render(request, '公司规模分布横向柱状图.html')
# 学历要求
def education(request):
    return render(request, '学历要求饼状图.html')
# 地图
def state(request):
    return render(request, '职位分布地图.html')
# 工作经验
def job_exp(request):
    return render(request, '工作经验要求柱状图.html')