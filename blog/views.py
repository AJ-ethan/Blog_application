from django.shortcuts import render, get_object_or_404
from blog.models import Post,Comment
from django.core.paginator import Paginator, EmptyPage,PageNotAnInteger
from django.views.generic import ListView

from .forms import EmailPostForm,CommentForm,PostForm
from django.core.mail import send_mail
#class PostListView(ListView):
#	qu

# Create your views here.
def post_list(request):
	object_list = Post.published.all()
	paginator = Paginator(object_list, 3) # 3 posts in each page
	page = request.GET.get('page')
	try:
		posts = paginator.page(page)
	except PageNotAnInteger:
	# If page is not an integer deliver the first page
		posts = paginator.page(1)
	except EmptyPage:
	# If page is out of range deliver last page of results
		posts = paginator.page(paginator.num_pages)
	return render(request,'blog/post/file.html',
						{'page':page,
						'posts':posts})

def post_detail(request,title):
	post = get_object_or_404(Post, title=title)

	#return render(request,'blog/post/detail.html',
							#{'post':post}) old 

	# List of active comments for this post
	comments = post.comments.filter(active=True)
	new_comment = None
	if request.method == 'POST':
	# A comment was posted
		comment_form = CommentForm(data=request.POST)
		if comment_form.is_valid():
	# Create Comment object but don't save to database yet
			new_comment = comment_form.save(commit=False)
	# Assign the current post to the comment
			new_comment.post = post
	# Save the comment to the database
			new_comment.save()
	else:
		comment_form = CommentForm()
	return render(request,
	'blog/post/detail.html',
	{'post': post,'comments': comments,
				'new_comment': new_comment,
				'comment_form': comment_form})
def post_postDetail(request):
	post = get_object_or_404(Post)

	#return render(request,'blog/post/detail.html',
							#{'post':post}) old 

	# List of active posts for this post
	#p = post.filter(active=True)
	new_post = None
	if request.method == 'POST':
	# A comment was posted
		post_form = PostForm(data=request.POST)
		if post_form.is_valid():
	# Create Comment object but don't save to database yet
			new_post = post_form.save(commit=False)
			new_post.save()
	else:
		post_form = PostForm()
	return render(request,
	'blog/post/addBlog.html',
	{'post': post,
				'new_post': new_post,
				'post_form': post_form})

def exp(request):
	post = Post.published.all()
	return render(request,'blog/post/exp.html',{'post':post})


def post_share(request, id):
	#print(id)
	post = get_object_or_404(Post,id=id) #status='published')
	sent = False

	#print(post.publish)
	if request.method == 'POST':
		#print("yes")
		form = EmailPostForm(request.POST) #or None, instance=post)
		#print(form)
		#print(form.is_valid())
		if form.is_valid():
			cd = {
			'name': form.cleaned_data['name'], 
			'to': form.cleaned_data['to'], 
			'email': form.cleaned_data['email'], 
			'comments':form.cleaned_data['comments'], 
			}
			#print(cd)
			post_url = request.build_absolute_uri(post.get_absolute_url())
			#print(post_url)
			subject = '{} ({}) recommends you reading "{}"'.format(cd['name'], cd['email'], post.title)
			message = 'Read "{}" at {}\n\n{}\'s comments:{}'.format(post.title,post_url,cd['name'], cd['comments'])

			send_mail(subject, message, 'jainv6464@gmail.com',[cd['to']],fail_silently=False)
			sent = True

	else:
		form= EmailPostForm()

	return render(request,'blog/post/share.html', {'post':post,'form':form, 'sent':sent })
