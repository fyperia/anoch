from rules_db.models import RulesChapter


def rb_table_of_contents(request):
    contents_list = RulesChapter.objects.all()
    return {'rb_table_of_contents': contents_list}
