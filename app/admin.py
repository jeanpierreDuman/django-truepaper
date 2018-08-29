from django.contrib import admin
from .models import *
import xadmin


xadmin.site.register(ArticleInterrest)
xadmin.site.register(HaveImageArticle)
xadmin.site.register(AuthorRecognize)
xadmin.site.register(Parameter)
xadmin.site.register(ArticleToCorrect)
xadmin.site.register(Article)
xadmin.site.register(Component)
xadmin.site.register(Fact)
xadmin.site.register(Justification)
xadmin.site.register(ArticleLike)
xadmin.site.register(ArticleReadAfter)
xadmin.site.register(Follow)
xadmin.site.register(Commentary)
xadmin.site.register(Point)
