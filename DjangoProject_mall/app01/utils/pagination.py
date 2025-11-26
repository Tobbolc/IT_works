"""
自定义的分页组件，以后如果要使用这个组件，需要做以下几件事：

在视图函数中：
def index(request):
    # 1. 根据自己的情况去筛选自己的数据
    queryset = Commodity.objects.filter(**data_search)

    # 2. 实例化分页对象
    page_object = Pagination(request, queryset)

    context = {
        'queryset': page_object.page_queryset,
        'page_string': page_object.html(),
        'search': search
    }
    return render(request, 'index.html', context)

在HTML页面中：
    {% for datum in queryset %}
        <div class="col-md-2">
            <div class="card">
                <div class="card-body">
                    <img src="{% static '/img/artknife.jpg' %}" class="card-img-top" alt=" "
                         style="width: 135px;height: 150px;">
                    <h5 class="card-title">名称：{{ datum.name }}</h5>
                    <p class="card-text">价格：{{ datum.price }}</p>
                    <p class="card-text">库存：{{ datum.stock }}</p>
                </div>

            </div>
        </div>
    {% endfor %}

    <ul class="pagination">
        {{ page_string }}
    </ul>
"""
from django.utils.safestring import mark_safe

class Pagination(object):
    def __init__(self, request, queryset, page_size=12, page_param='page', plus=5):
        """
        :param request: 请求的对象
        :param queryset: 符合条件的数据 （根据这个数据进行分页处理）
        :param page_size: 每页数据量
        :param page_param: 在URL中传递的获取分页的参数 例如http://127.0.0.1:8000/?page=1
        :param plus: 显示单次增减页数
        """
        from django.http.request import QueryDict
        import copy
        query_dict = copy.deepcopy(request.GET)
        query_dict._mutable = True
        self.query_dict = query_dict
        self.page_param = page_param
        page = request.GET.get(page_param, "1")
        # 是十进制再转换
        if page.isdecimal():
            page = int(page)
        else:
            page = 1

        self.page = page
        self.page_size = page_size
        self.start = (page - 1) * page_size
        self.end = page * page_size

        self.page_queryset = queryset[self.start:self.end]

        # 数据总条数
        total_count = queryset.count()
        # 总页数
        page_count, div = divmod(total_count, page_size)
        if div:
            page_count += 1
        self.total_pages = page_count
        self.plus = plus

    def html(self):
        # 显示前5页和后5页
        if self.total_pages <= 2 * self.plus + 1:
            # 页数比较少，未达到11页
            start_page = 1
            end_page = self.total_pages
        else:
            # 页数比较多

            # 当前页<5时
            if self.page <= self.plus:
                start_page = 1
                end_page = 2 * self.plus + 1
            else:
                if (self.page + self.plus) > self.total_pages:
                    start_page = self.total_pages - 2 * self.plus
                    end_page = self.total_pages
                else:
                    start_page = self.page - self.plus
                    end_page = self.page + self.plus

        # 页码列表
        page_str_list = []
        # 首页
        self.query_dict.setlist(self.page_param, [1])
        page_str_list.append('<li><a href="?{}">首页</a></li>'.format(self.query_dict.urlencode()))
        # 上一页
        if self.page > 1:
            self.query_dict.setlist(self.page_param, [self.page-1])
            prev = '<li><a href="?{}">上一页</a></li>'.format(self.query_dict.urlencode())
        else:
            self.query_dict.setlist(self.page_param, [1])
            prev = '<li><a href="?{}">上一页</a></li>'.format(self.query_dict.urlencode())
        page_str_list.append(prev)
        for i in range(start_page, end_page + 1):
            self.query_dict.setlist(self.page_param, [i])
            if i == self.page:
                ele = '<li class="active"><a href="?{}">{}</a></li>'.format(self.query_dict.urlencode(), i)
            else:
                ele = '<li><a href="?{}">{}</a></li>'.format(self.query_dict.urlencode(), i)
            page_str_list.append(ele)
        # 下一页
        if self.page < self.total_pages:
            self.query_dict.setlist(self.page_param, [self.page + 1])
            prev = '<li><a href="?{}">下一页</a></li>'.format(self.query_dict.urlencode())
        else:
            self.query_dict.setlist(self.page_param, [self.total_pages])
            prev = '<li><a href="?{}">下一页</a></li>'.format(self.query_dict.urlencode())
        page_str_list.append(prev)
        # 尾页
        self.query_dict.setlist(self.page_param, [self.total_pages])
        page_str_list.append('<li><a href="?{}">尾页</a></li>'.format(self.query_dict.urlencode()))

        search_string = """
                           <li>
                               <form style="float: left;margin-left: -1px" method="get">
                                   <div class="input-group" style="width: 200px">
                                       <input type="text" name="page" class="form-control" placeholder="页码" 
                                              style="position: relative;float: left;display: inline-block;width: 80px;border-radius: 0;">
                                       <button style="border-radius: 0" class="btn btn-default" type="submit">跳转</button>
                                   </div>
                               </form>
                           </li>
                           """
        page_str_list.append(search_string)
        page_string = mark_safe("".join(page_str_list))
        return page_string
