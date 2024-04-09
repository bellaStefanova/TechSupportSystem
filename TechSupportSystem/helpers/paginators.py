from django.core.paginator import Paginator

class FlexiblePaginator(Paginator):
    
    def __init__(self, object_list, per_page, orphans=0, allow_empty_first_page=True):
        self.user_per_page = per_page
        super().__init__(object_list, per_page, orphans, allow_empty_first_page)


    def get_page(self, number):

        self.per_page = self.user_per_page
        return super().get_page(number)