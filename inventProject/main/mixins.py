# /home/administrator/Pro/Python/invent/inventProject/main/mixins.py
from django.shortcuts import redirect


class FilterPersistenceMixin:
    """
    Миксин (небольшой класс-примесь), который:
      * сохраняет GET-параметры фильтра в сессии пользователя;
      * восстанавливает их при возврате на страницу списка;
      * добавляет их к success_url после create/update/delete.
    В каждом наследнике ОБЯЗАТЕЛЬНО задать filter_session_key —
    разные ключи для оборудования и расходников, чтобы фильтры не смешивались.
    """

    # Переопределяется в наследниках, например 'equipment_filters'
    filter_session_key = None

    def _saved_query(self):
        if not self.filter_session_key:
            return ''
        return self.request.session.get(self.filter_session_key, '')

    def dispatch(self, request, *args, **kwargs):
        # У Create/Update/Delete этот метод тоже унаследован,
        # но там нам важна только перезапись get_success_url,
        # поэтому логику сессии выполняем лишь когда задан ключ.
        if not self.filter_session_key:
            return super().dispatch(request, *args, **kwargs)

        # 1. Явный сброс фильтров: ?reset=1
        if 'reset' in request.GET:
            request.session.pop(self.filter_session_key, None)
            return redirect(request.path)

        # 2. Если в URL есть параметры — запоминаем строку запроса
        query_string = request.META.get('QUERY_STRING', '')
        if query_string:
            request.session[self.filter_session_key] = query_string
            return super().dispatch(request, *args, **kwargs)

        # 3. Параметров нет, но есть сохранённые — переходим уже с ними
        saved = self._saved_query()
        if saved:
            return redirect(f'{request.path}?{saved}')

        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        # Стандартный URL из success_url + сохранённые параметры фильтра
        url = str(super().get_success_url())
        saved = self._saved_query()
        if not saved:
            return url
        separator = '&' if '?' in url else '?'
        return f'{url}{separator}{saved}'