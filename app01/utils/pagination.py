from django.utils.safestring import mark_safe

class Pagination:
    def __init__(self, request, queryset, page_size=5):
        self.request = request
        self.queryset = queryset
        self.page_size = page_size

        # 获取当前页码
        page = self.request.GET.get("page", "1")
        if not page.isdigit():
            page = 1
        self.page = int(page)

        # 复制GET参数，去掉page，翻页的时候保留搜索q
        self.query_params = self.request.GET.copy()
        if "page" in self.query_params:
            del self.query_params["page"]
        self.query_str = self.query_params.urlencode()

        # 数据切片
        self.start = (self.page - 1) * self.page_size
        self.end = self.page * self.page_size
        self.page_queryset = self.queryset[self.start:self.end]

        # 总条数、总页数
        self.total_count = self.queryset.count()
        self.total_page, remainder = divmod(self.total_count, self.page_size)
        if remainder:
            self.total_page += 1

    def html(self):
        page_list = []
        # ========== 首页 ==========
        if self.page == 1:
            page_list.append('<button class="btn btn-default">首页</button>')
        else:
            if self.query_str:
                page_list.append(f'<a class="btn btn-default" href="?{self.query_str}&page=1">首页</a>')
            else:
                page_list.append(f'<a class="btn btn-default" href="?page=1">首页</a>')

        # ========== 上一页 ==========
        if self.page == 1:
            page_list.append('<button class="btn btn-default">上一页</button>')
        else:
            prev_page = self.page - 1
            if self.query_str:
                page_list.append(f'<a class="btn btn-default" href="?{self.query_str}&page={prev_page}">上一页</a>')
            else:
                page_list.append(f'<a class="btn btn-default" href="?page={prev_page}">上一页</a>')

        # ========== 页码（只展示 1、2、3... 简单版本，适合你的作业） ==========
        for i in range(1, self.total_page + 1):
            if i == self.page:
                # 当前页蓝色高亮
                page_list.append(f'<a class="btn btn-primary" href="?page={i}">{i}</a>')
            else:
                if self.query_str:
                    page_list.append(f'<a class="btn btn-default" href="?{self.query_str}&page={i}">{i}</a>')
                else:
                    page_list.append(f'<a class="btn btn-default" href="?page={i}">{i}</a>')

        # ========== 下一页 ==========
        if self.page == self.total_page:
            page_list.append('<button class="btn btn-default">下一页</button>')
        else:
            next_page = self.page + 1
            if self.query_str:
                page_list.append(f'<a class="btn btn-default" href="?{self.query_str}&page={next_page}">下一页</a>')
            else:
                page_list.append(f'<a class="btn btn-default" href="?page={next_page}">下一页</a>')

        # ========== 尾页 ==========
        if self.page == self.total_page:
            page_list.append('<button class="btn btn-default">尾页</button>')
        else:
            if self.query_str:
                page_list.append(f'<a class="btn btn-default" href="?{self.query_str}&page={self.total_page}">尾页</a>')
            else:
                page_list.append(f'<a class="btn btn-default" href="?page={self.total_page}">尾页</a>')

        html = "".join(page_list)
        return mark_safe(html)
