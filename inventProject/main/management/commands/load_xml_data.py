"""
Загрузка данных о сотрудниках, орг. единицах и должностях из XML.

Порядок загрузки ВАЖЕН:
  1) *org*.xml       — орг. единицы (родители/дети);
  2) *post*.xml      — должности;
  3) *employee*.xml  — сотрудники (ссылаются на org и post).

Upsert выполняется по полю `external_id` (то самое `id` из XML):
если запись с таким id есть — обновляем, нет — создаём.

Запуск:
    python manage.py load_xml_data --dir /path/to/xml_incoming
"""
import glob
import os
from datetime import datetime

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction
from defusedxml import ElementTree as ET

from main.models import Organization, Post, Employee


def _parse_date(value):
    """'11.06.1985' -> date(1985, 6, 11). Пусто/None -> None."""
    if not value:
        return None
    value = value.strip()
    if not value:
        return None
    try:
        return datetime.strptime(value, '%d.%m.%Y').date()
    except ValueError:
        return None


def _text(node, tag):
    """Безопасно достаёт текст тега; пустая строка если тега/текста нет."""
    if node is None:
        return ''
    value = node.findtext(tag)
    return (value or '').strip()


class Command(BaseCommand):
    help = 'Загружает из XML файлов орг. единицы, должности и сотрудников (upsert по id).'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dir',
            default=None,
            help='Каталог с XML-файлами. По умолчанию settings.XML_IMPORT_DIR.',
        )

    def handle(self, *args, **options):
        import_dir = options.get('dir') or getattr(settings, 'XML_IMPORT_DIR', '')
        if not import_dir or not os.path.isdir(import_dir):
            self.stderr.write(f'Каталог не найден: {import_dir!r}')
            return

        org_files = self._pick_newest(import_dir, '*org*.xml')
        post_files = self._pick_newest(import_dir, '*post*.xml')
        emp_files = self._pick_newest(import_dir, '*employee*.xml')

        if not (org_files and post_files and emp_files):
            self.stderr.write(
                f'Не найдены все три файла в {import_dir}: '
                f'org={org_files!r} post={post_files!r} employee={emp_files!r}'
            )
            return

        # Всё в одной транзакции: если что-то упадёт — БД останется прежней.
        with transaction.atomic():
            self._load_org(org_files[0])
            self._load_post(post_files[0])
            self._load_employee(emp_files[0])

        self.stdout.write(self.style.SUCCESS(
            f'OK: org={os.path.basename(org_files[0])}, '
            f'post={os.path.basename(post_files[0])}, '
            f'employee={os.path.basename(emp_files[0])}'
        ))

    @staticmethod
    def _pick_newest(directory, pattern):
        """Все файлы по маске, отсортированные по времени изменения (новые в конце)."""
        files = glob.glob(os.path.join(directory, pattern))
        return sorted(files, key=os.path.getmtime)

    # ------------------------------------------------------------------ org
    def _load_org(self, path):
        self.stdout.write(f'[ORG] {path}')
        tree = ET.parse(path)
        root = tree.getroot()

        # Проход 1: создать/обновить все записи без parent.
        rows = []
        for node in root.findall('ORG'):
            ext_id = _text(node, 'id')
            if not ext_id:
                continue
            rows.append({
                'ext_id': ext_id,
                'name': _text(node, 'Name'),
                'full_name': _text(node, 'fullName'),
                'parent_code': _text(node, 'ParentCode'),
                'is_root': _text(node, 'Istop') == '1',
            })

        for r in rows:
            Organization.objects.update_or_create(
                external_id=r['ext_id'],
                defaults={
                    'name': r['name'],
                    'full_name': r['full_name'],
                    'is_root': r['is_root'],
                },
            )

        # Проход 2: проставить родителей (могли встретиться ниже ребёнка в файле).
        for r in rows:
            parent = None
            if r['parent_code']:
                parent = Organization.objects.filter(
                    external_id=r['parent_code']
                ).first()
            Organization.objects.filter(
                external_id=r['ext_id']
            ).update(parent=parent)

    # ----------------------------------------------------------------- post
    def _load_post(self, path):
        self.stdout.write(f'[POST] {path}')
        tree = ET.parse(path)
        root = tree.getroot()
        for node in root.findall('Post'):
            ext_id = _text(node, 'id')
            if not ext_id:
                continue
            Post.objects.update_or_create(
                external_id=ext_id,
                defaults={'name': _text(node, 'Name')},
            )

    # ------------------------------------------------------------- employee
    def _load_employee(self, path):
        self.stdout.write(f'[EMPLOYEE] {path}')
        tree = ET.parse(path)
        root = tree.getroot()
        for node in root.findall('Person'):
            ext_id = _text(node, 'id')
            if not ext_id:
                continue

            section_code = _text(node, 'section')
            position_code = _text(node, 'position')

            section = None
            if section_code:
                section = Organization.objects.filter(
                    external_id=section_code
                ).first()

            position = None
            if position_code:
                position = Post.objects.filter(
                    external_id=position_code
                ).first()

            Employee.objects.update_or_create(
                external_id=ext_id,
                defaults={
                    'tab_id': _text(node, 'Tab_id'),
                    'lastname': _text(node, 'lastname'),
                    'firstname': _text(node, 'firstname'),
                    'middlename': _text(node, 'middlename'),
                    'date_of_birth': _parse_date(node.findtext('dateofbirth')),
                    'section': section,
                    'position': position,
                    'state': _text(node, 'state'),
                    'feature': _text(node, 'feature'),
                    'start_date': _parse_date(node.findtext('startdate')),
                    'fire_date': _parse_date(node.findtext('firedate')),
                    'vacation_start': _parse_date(node.findtext('vacationstart')),
                    'vacation_end': _parse_date(node.findtext('vacationend')),
                    'gender': _text(node, 'gender'),
                    'office_location': _text(node, 'officelocation'),
                },
            )