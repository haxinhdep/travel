try:
    from urllib import quote_plus #python 2
except:
    pass

try:
    from urllib.parse import quote_plus #python 3
except: 
    pass

from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from comments.forms import CommentForm
from comments.models import Comment
from .forms import PostForm
from .models import Post
import requests
from bs4 import BeautifulSoup


def url_link_spider(url_link, title, img):
    url = url_link
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text)
    content = ''
    draw = Post()
    i = 1
    for h4 in soup.findAll('h4', {'style': 'text-align: justify;'}):
        content1 = h4.string
        if content1 is not None:
           content +=content1
        i += 1
    i = 1
    for p in soup.findAll('p', {'style': 'text-align: justify;'}):
        content2 = p.string
        if content2 is not None:
           content += content2
        i += 1
    i = 1
    for p in soup.findAll('p'):
        content3 = p.string
        if content3 is not None:
           content += content3
    i += 1
    for date in soup.find('div', {'class': 'date'}):
        date = date.string
        if date is not None:
            draw.publish = '2017-06-12'
        i += 1
    draw.content = content
    draw.title = title
    # draw.image = img
    draw.is_browse = True
    draw.save()

def trade_spider():
    url = 'http://tourism.danang.vn/su-kien-noi-bat'
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text)

    i = 1
    for div in soup.findAll('div', {'class': 'post-thumb preload image-loading zoom-img-in'}):
        title = div.img.get('alt')
        href = div.a.get('href')
        img = div.img.get('src')
        url_link_spider(href, title, img)
        i += 1


def draw(request):
    if not request.user.is_superuser:
        raise Http404
    trade_spider()
    return render(request, "post_form.html")


def post_create(request):
    if not request.user.is_staff :
        raise Http404

    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user

        if(instance.is_browse and request.user.is_superuser):
            instance.save()
            return HttpResponseRedirect(instance.get_absolute_url())
        if (instance.is_browse == False  and request.user.is_staff):
            instance.save()
            messages.success(request, "Post event thành công, chờ kiểm duyệt")
        if(instance.is_browse and request.user.is_staff):
            messages.warning(request, "Bạn không có quyền thực hiện kiểm duyệt")

    context = {
     "form": form,
    }
    return render(request, "post_form.html", context)

def post_detail(request, slug=None):
	instance = get_object_or_404(Post, slug=slug)
	if instance.publish > timezone.now().date() or instance.draft:
		if not request.user.is_staff or not request.user.is_superuser:
			raise Http404
	share_string = quote_plus(instance.content)

	initial_data = {
			"content_type": instance.get_content_type,
			"object_id": instance.id
	}
	form = CommentForm(request.POST or None, initial=initial_data)
	if form.is_valid() and request.user.is_authenticated():
		c_type = form.cleaned_data.get("content_type")
		content_type = ContentType.objects.get(model=c_type)
		obj_id = form.cleaned_data.get('object_id')
		content_data = form.cleaned_data.get("content")
		parent_obj = None
		try:
			parent_id = int(request.POST.get("parent_id"))
		except:
			parent_id = None

		if parent_id:
			parent_qs = Comment.objects.filter(id=parent_id)
			if parent_qs.exists() and parent_qs.count() == 1:
				parent_obj = parent_qs.first()


		new_comment, created = Comment.objects.get_or_create(
							user = request.user,
							content_type= content_type,
							object_id = obj_id,
							content = content_data,
							parent = parent_obj,
						)
		return HttpResponseRedirect(new_comment.content_object.get_absolute_url())


	comments = instance.comments
	context = {
		"title": instance.title,
		"instance": instance,
		"share_string": share_string,
		"comments": comments,
		"comment_form":form,
	}
	return render(request, "post_detail.html", context)

def post_list(request):
	today = timezone.now().date()
	queryset_list = Post.objects.active().order_by("-timestamp")
	if request.user.is_staff or request.user.is_superuser:
		queryset_list = Post.objects.all()

	query = request.GET.get("q")
	if query:
		queryset_list = queryset_list.filter(
				Q(title__icontains=query)|
				Q(content__icontains=query)|
				Q(user__first_name__icontains=query) |
				Q(user__last_name__icontains=query)
				).distinct()
	paginator = Paginator(queryset_list, 8) # Show 25 contacts per page
	page_request_var = "page"
	page = request.GET.get(page_request_var)
	try:
		queryset = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		queryset = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		queryset = paginator.page(paginator.num_pages)


	context = {
		"object_list": queryset,
		"title": "List",
		"page_request_var": page_request_var,
		"today": today,
	}
	return render(request, "event.html", context)





def post_update(request, slug=None):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404
	instance = get_object_or_404(Post, slug=slug)
	form = PostForm(request.POST or None, request.FILES or None, instance=instance)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		messages.success(request, "<a href='#'>Item</a> Saved", extra_tags='html_safe')
		return HttpResponseRedirect(instance.get_absolute_url())

	context = {
		"title": instance.title,
		"instance": instance,
		"form":form,
	}
	return render(request, "post_form.html", context)



def post_delete(request, slug=None):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404
	instance = get_object_or_404(Post, slug=slug)
	instance.delete()
	messages.success(request, "Successfully deleted")
	return redirect("posts:list")
