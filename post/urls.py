from django.urls import path
from post.views import index,contact2, desktop_only_page,save_post_text,student_placed,archives_view, NewPost,home,contact, gallery, events, alumni, faculty_notes, PostDetail, Tags, like, favourite, engg_professor, sc_professor, professors, comm_professor, ayush_professor, tc_professor, arch_professor, arts_professor, ss_professor, college, placement

urlpatterns = [
    path('', home, name='home'),
    path('index', index, name='index'),
    path('newpost', NewPost, name='newpost'),
    path('professors', professors, name='professors'),
    path('Enggprofessor', engg_professor, name='engg_professor'),
    path('scprofessor', sc_professor, name='sc_professor'),

    path('commprofessor', comm_professor, name='comm_professor'),
    path('ayushprofessor', ayush_professor, name='ayush_professor'),
    path('tcprofessor', tc_professor, name='tc_professor'),
    path('archprofessor', arch_professor, name='arch_professor'),
    path('artsprofessor', arts_professor, name='arts_professor'),
    path('ssprofessor', ss_professor, name='ss_professor'),

    # path('colleges', college, name='college'),


    path('<uuid:post_id>', PostDetail, name='post-details'),
    path('tag/<slug:tag_slug>', Tags, name='tags'),
    path('<uuid:post_id>/like', like, name='like'),
    path('<uuid:post_id>/favourite', favourite, name='favourite'),

    path('placement/', placement, name='placement'),
    path('faculty_notes/', faculty_notes, name='faculty_notes'),

    path('events/', events, name='events'),
    path('archives/', archives_view, name='archives'),
    path('alumni/', alumni, name='alumni'),

    path('contact/', contact, name='contact'),
    path('contact2/', contact2, name='contact2'),

    path('gallery/', gallery, name='gallery'),

    path('student_placed/', student_placed, name='student_placed'),

    path('save_post_text/<uuid:post_id>/', save_post_text, name='save_post_text'),

    path('desktop-only/', desktop_only_page, name='desktop_only_page'),






]
