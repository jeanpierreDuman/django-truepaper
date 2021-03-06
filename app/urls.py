from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.listArticle, name='article_list'),
    url(r'^user/article$', views.listArticleUser, name='article_list_user'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^logout/$', views.logoutAction, name='logout'),
    url(r'^login/$', views.login, name='login'),
    url(r'^accounts/profile/$', views.profileAction, name='profile'),
    url(r'^user/follow/(?P<id>[0-9]+)/$', views.follow, name='follow'),
    url(r'^user/unfollow/(?P<id>[0-9]+)/$', views.unfollow, name='unfollow'),
    url(r'^list/follow/$', views.listFollow, name='follow_list'),
    url(r'^list/article/from/user/(?P<id>[0-9]+)/$', views.listArticleFromUser, name='list_article_from_user'),
    url(r'^user/choose/corrector/article/(?P<id>[0-9]+)/$', views.chooseFollowForCorrection, name='choose_corrector'),
    url(r'^article/(?P<id>[0-9]+)/accept/(?P<id2>[0-9]+)/$', views.acceptCorrection, name='correction_accept'),
    url(r'^article/(?P<id>[0-9]+)/refuse/(?P<id2>[0-9]+)/$', views.refuseCorrection, name='correction_refuse'),
    url(r'^article/preview$', views.previewArticle, name='article_preview'),
    url(r'^article/add$', views.addArticle, name='article_add'),
    url(r'^list/article/correct', views.listCorrectArticle, name='list_correct_article'),
    url(r'^article/edit/(?P<id>[0-9]+)/$', views.editArticle, name='article_edit'),
    url(r'^article/like/(?P<id>[0-9]+)/$', views.likeArticle, name='article_like'),
    url(r'^article/dislike/(?P<id>[0-9]+)/$', views.dislikeArticle, name='article_dislike'),
    url(r'^article/read/(?P<id>[0-9]+)/$', views.readArticle, name='article_read'),
    url(r'^article/(?P<id>[0-9]+)/interrest/$', views.interrestArticle, name='article_interrest'),
    url(r'^article/unread/(?P<id>[0-9]+)/$', views.unreadArticle, name='article_unread'),
    url(r'^article/read', views.listReadArticle, name='article_read_list'),
    url(r'^article/like', views.listLikeArticle, name='article_list_like'),
    url(r'^article/(?P<id>[0-9]+)/$', views.selectArticle, name='article_select'),
    url(r'^article/published/(?P<id>[0-9]+)/$', views.publishArticle, name='article_publish'),
    url(r'^article/(?P<idA>[0-9]+)/fact/(?P<idF>[0-9]+)/$', views.selectFact, name='article_select_fact'),
    url(r'^article/(?P<idA>[0-9]+)/fact/(?P<idF>[0-9]+)/justification/(?P<idJ>[0-9]+)/agree$', views.justificationAgree, name='justification_agree'),
    url(r'^article/(?P<idA>[0-9]+)/fact/(?P<idF>[0-9]+)/justification/(?P<idJ>[0-9]+)/disagree$', views.justificationDisagree, name='justification_disagree'),
    url(r'^article/(?P<id>[0-9]+)/image/accept$', views.imageAcceptArticle, name='article_image_accept'),
    url(r'^article/(?P<id>[0-9]+)/image/refuse$', views.imageRefuseArticle, name='article_image_refuse'),
    url(r'^profile/question/secret/?', views.chooseSecretQuestion, name='choose_question_secret'),
    url(r'^profile/password/forget/?', views.forgetPassword, name='forget_password'),
    url(r'^profile/(?P<id>[0-9]+)/question/response/?', views.responseSecretQuestion, name='response_secret_question'),
    url(r'^profile/(?P<id>[0-9]+)/password/change/?', views.changePassword, name='password_change'),
    url(r'^article/(?P<idA>[0-9]+)/author/(?P<id>[0-9]+)/recognize/accept/?', views.acceptAuthorRecognize, name='author_recognize_accept'),
    url(r'^article/(?P<idA>[0-9]+)/author/(?P<id>[0-9]+)/recognize/refuse/?', views.refuseAuthorRecognize, name='author_recognize_refuse'),
    url(r'^search/$', views.search, name='search'),
    url(r'^article/category/$', views.listArticleCategory, name='article_category'),
]
