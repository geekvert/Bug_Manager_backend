from backend.models import Bug, Comment

def meth(Bug):
    comments = Comment.objects.get(buggy=Bug)
    print(str(comments))

bg = Bug.objects.get(heading='test_bug')

meth(bg)
