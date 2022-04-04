import pymongo  # 连接mongodb
from pyecharts.charts import Bar, Pie, Map  # bar：条形图绘制模块，pie：饼图绘制模块, map: 地图绘制模块
from pyecharts import options as opts
from pyecharts.globals import ThemeType  # 主题类型

'''
TODO：
√ 1. 公司规模横向柱状图
√ 2. 工作经验竖柱状图
'''

# pyecharts官网http://pyecharts.org/

client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client['recruitment']
mycol = db['job']

# 学历
education = []
# 城市
state = []
# 公司规模
company_size = []
# 工作经验
job_exp = []

# 省市对应关系
city_lists = {
    "北京": ["北京"],
    "天津": ["天津"],
    "山西": ["太原", "阳泉", "晋城", "长治", "临汾", "运城", "忻州", "吕梁", "晋中", "大同", "朔州"],
    "河北": ["沧州", "石家庄", "唐山", "保定", "廊坊", "衡水", "邯郸", "邢台", "张家口", "辛集", "秦皇岛", "定州", "承德", "涿州"],
    "山东": ["济南", "淄博", "聊城", "德州", "滨州", "济宁", "菏泽", "枣庄", "烟台", "威海", "泰安", "青岛", "临沂", "莱芜", "东营", "潍坊", "日照"],
    "河南": ["郑州", "新乡", "鹤壁", "安阳", "焦作", "濮阳", "开封", "驻马店", "商丘", "三门峡", "南阳", "洛阳", "周口", "许昌", "信阳", "漯河", "平顶山",
           "济源"],
    "广东": ["珠海", "中山", "肇庆", "深圳", "清远", "揭阳", "江门", "惠州", "河源", "广州", "佛山", "东莞", "潮州", "汕尾", "梅州", "阳江", "云浮", "韶关",
           "湛江", "汕头", "茂名"],
    "浙江": ["舟山", "温州", "台州", "绍兴", "衢州", "宁波", "丽水", "金华", "嘉兴", "湖州", "杭州"],
    "宁夏": ["中卫", "银川", "吴忠", "石嘴山", "固原"],
    "江苏": ["镇江", "扬州", "盐城", "徐州", "宿迁", "无锡", "苏州", "南通", "南京", "连云港", "淮安", "常州", "泰州"],
    "湖南": ["长沙", "邵阳", "怀化", "株洲", "张家界", "永州", "益阳", "湘西", "娄底", "衡阳", "郴州", "岳阳", "常德", "湘潭"],
    "吉林": ["长春", "长春", "通化", "松原", "四平", "辽源", "吉林", "延边", "白山", "白城"],
    "福建": ["漳州", "厦门", "福州", "三明", "莆田", "宁德", "南平", "龙岩", "泉州"],
    "甘肃": ["张掖", "陇南", "兰州", "嘉峪关", "白银", "武威", "天水", "庆阳", "平凉", "临夏", "酒泉", "金昌", "甘南", "定西"],
    "陕西": ["榆林", "西安", "延安", "咸阳", "渭南", "铜川", "商洛", "汉中", "宝鸡", "安康"],
    "辽宁": ["营口", "铁岭", "沈阳", "盘锦", "辽阳", "锦州", "葫芦岛", "阜新", "抚顺", "丹东", "大连", "朝阳", "本溪", "鞍山"],
    "江西": ["鹰潭", "宜春", "上饶", "萍乡", "南昌", "景德镇", "吉安", "抚州", "新余", "九江", "赣州"],
    "黑龙江": ["伊春", "七台河", "牡丹江", "鸡西", "黑河", "鹤岗", "哈尔滨", "大兴安岭", "绥化", "双鸭山", "齐齐哈尔", "佳木斯", "大庆"],
    "安徽": ["宣城", "铜陵", "六安", "黄山", "淮南", "合肥", "阜阳", "亳州", "安庆", "池州", "宿州", "芜湖", "马鞍山", "淮北", "滁州", "蚌埠"],
    "湖北": ["孝感", "武汉", "十堰", "荆门", "黄冈", "襄阳", "咸宁", "随州", "黄石", "恩施", "鄂州", "荆州", "宜昌", "潜江", "天门", "神农架", "仙桃"],
    "青海": ["西宁", "海西", "海东", "玉树", "黄南", "海南", "海北", "果洛"],
    "新疆": ["乌鲁木齐", "克州", "阿勒泰", "五家渠", "石河子", "伊犁", "吐鲁番", "塔城", "克拉玛依", "喀什", "和田", "哈密", "昌吉", "博尔塔拉", "阿克苏", "巴音郭楞",
           "阿拉尔", "图木舒克", "铁门关"],
    "贵州": ["铜仁", "黔东南", "贵阳", "安顺", "遵义", "黔西南", "黔南", "六盘水", "毕节"],
    "四川": ["遂宁", "攀枝花", "眉山", "凉山", "成都", "巴中", "广安", "自贡", "甘孜", "资阳", "宜宾", "雅安", "内江", "南充", "绵阳", "泸州", "凉山", "乐山",
           "广元", "甘孜", "德阳", "达州", "阿坝"],
    "上海": ["上海"],
    "广西": ["南宁", "贵港", "玉林", "梧州", "钦州", "柳州", "来宾", "贺州", "河池", "桂林", "防城港", "崇左", "北海", "百色"],
    "西藏": ["拉萨", "山南", "日喀则", "那曲", "林芝", "昌都", "阿里"],
    "云南": ["昆明", "红河", "大理", "玉溪", "昭通", "西双版纳", "文山", "曲靖", "普洱", "怒江", "临沧", "丽江", "红河", "迪庆", "德宏", "大理", "楚雄",
           "保山"],
    "内蒙古": ["呼和浩特", "乌兰察布", "兴安", "赤峰", "呼伦贝尔", "锡林郭勒", "乌海", "通辽", "巴彦淖尔", "阿拉善", "鄂尔多斯", "包头"],
    "海南": ["海口", "三沙", "三亚", "临高", "五指山", "陵水", "文昌", "万宁", "白沙", "乐东", "澄迈", "屯昌", "定安", "东方", "保亭", "琼中", "琼海", "儋州",
           "昌江"],
    "重庆": ["重庆"]
}

# 下面是比较辣眼睛的数据处理 0-0

# 数据清洗 -- 学历
for i in mycol.find({}, {'job_edu': 1, '_id': 0}):
    for j in i.values():
        education.append(j)
        pass
    pass
# 数据清洗 -- 学历
def get_edu(list):
    education2 = {}
    for i in set(list):
        education2[i] = list.count(i)
        pass
    return education2
edu = get_edu(education)

# 数据清洗 -- 城市
for i in mycol.find({}, {'work_area': 1, '_id': 0}):
    for j in i.values():
        data = j.split('-')[0]
        city = ''
        if '省' in data:
            state.append(data.split('省')[0])
        else:
            # 获取city_lists中的省份
            # z:城市
            # k:省份
            for k, z in city_lists.items():
                if data in z:
                    state.append(k)
                    pass
                pass
            pass
        pass
    pass
# 数据清洗 -- 城市
def get_city(list):
    work_city = {}
    for i in set(list):
        work_city[i] = list.count(i)
        pass
    return work_city
city = get_city(state)


# 数据清洗 -- 公司规模
for i in mycol.find({}, {'company_size': 1, '_id': 0}):
    for j in i.values():
        company_size.append(j)
        pass
    pass
# 数据清洗 -- 公司规模
def company_scale(list):
    size = {}
    for i in set(list):
        size[i] = list.count(i)
        pass
    return size


size = company_scale(company_size)

# 数据清洗 -- 工作经验
for i in mycol.find({}, {'job_exp': 1, '_id': 0}):
    for j in i.values():
        job_exp.append(j)
        pass
    pass
# 数据清洗 -- 工作经验
def experience(list):
    exp = {}
    for i in set(list):
        exp[i] = list.count(i)
        pass
    return exp
exp = experience(job_exp)


class PyMongoDemo(object):
    # 学历饼图
    def edu_pie(self):
        data_pair = [list(z) for z in zip(edu.keys(), edu.values())]
        (
            Pie()
                .add('', data_pair,
                     radius=['40%', '75%'],
                     center=["50%", "50%"],
                     label_opts=opts.LabelOpts(is_show=False),
                     )
                .set_global_opts(
                title_opts=opts.TitleOpts(
                    title='学历要求饼状图',
                    pos_left='center', ),
                legend_opts=opts.LegendOpts(
                    orient='vertical',
                    pos_top='15%',
                    pos_left='2%',
                ),
            )
                .set_series_opts(
                label_opts=opts.LabelOpts(formatter='{b}: {d}%')
            )
                .render('学历要求饼状图.html')
        )
        pass

    # 职位地图
    def job_map(self):
        data_pair = [list(z) for z in zip(city.keys(), city.values())]
        (
            Map()
                .add(
                "职位数量",
                data_pair,
                'china',
                center=["50%", "50%"],
            )
                .set_global_opts(
                visualmap_opts=opts.VisualMapOpts(
                    is_piecewise=True,
                    pieces=[
                        {"max": 100, "min": 0, "label": "0-100", "color": "#CDCDC1"},
                        {"max": 500, "min": 101, "label": "101-500", "color": "#EE82EE"},
                        {"max": 2000, "min": 501, "label": "501-2000", "color": "#7A7A7A"},
                        {"max": 5000, "min": 2001, "label": "2001-5000", "color": "#EE9A00"},
                        {"max": 10000, "min": 5001, "label": "5001-10000", "color": "#FF6347"},
                        {"max": 15000, "min": 10001, "label": "5001-15000", "color": "#FF0000"}, ]
                ),
                legend_opts=opts.LegendOpts(
                    is_show=False,
                ),
                title_opts=opts.TitleOpts(
                    title="全国各省招聘数量",
                    pos_left='center',
                ),
            )
                .render("职位分布地图.html")
        )
        pass

    # 规模柱状图
    def size_bar(self):
        (
            Bar(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
                .add_xaxis(list(size.keys()))
                .add_yaxis('公司规模', list(size.values()))
                .reversal_axis()
                .set_series_opts(
                label_opts=opts.LabelOpts(position="right")
            )
                .set_global_opts(
                title_opts=opts.TitleOpts(
                    title="公司规模分布",
                    pos_left='center'
                ),
                legend_opts=opts.LegendOpts(
                    orient='vertical',
                    pos_bottom='10%',
                    pos_left='5px'
                ),
            )
                .render('公司规模分布横向柱状图.html')
        )
        pass

    # 经验柱状图
    def exp_bar(self):
        (
            Bar(init_opts=opts.InitOpts(theme=ThemeType.WONDERLAND))
                .add_xaxis(list(exp.keys()))
                .add_yaxis('工作经验', list(exp.values()))
                .set_series_opts(
                label_opts=opts.LabelOpts(
                    formatter='{c}',
                    position='top')
            )
                .set_global_opts(
                title_opts=opts.TitleOpts(
                    title="工作经验要求",
                    pos_left='center'
                ),
                legend_opts=opts.LegendOpts(
                    orient='vertical',
                    pos_bottom='10%',
                    pos_left='5px'
                ),
                xaxis_opts=opts.AxisOpts(
                    name_rotate=60,
                    axislabel_opts={"rotate": 45}
                ),
            )
                .render('工作经验要求柱状图.html')
        )
        pass


if __name__ == '__main__':
    mongo = PyMongoDemo()
    mongo.edu_pie()
    mongo.job_map()
    mongo.size_bar()
    mongo.exp_bar()
