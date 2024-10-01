# TODO: Исправить Миксины


class CommonMixin:
    title = None
    categories = None

    def get_context_data(self, **kwargs):
        context = super(CommonMixin, self).get_context_data(**kwargs)
        context['title'] = self.title
        context['category_id'] = self.kwargs.get('category_id')
        return context


class TitleMixin:
    title = None

    def get_context_data(self, **kwargs):
        context = super(TitleMixin, self).get_context_data(**kwargs)
        context['title'] = self.title
        return context
