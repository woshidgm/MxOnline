# -*- coding: utf-8 -*-
from django.shortcuts import render, HttpResponse
from django.views.generic.base import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q


from .models import Course, CourseResource
from operation.models import UserFavorite, CourseComment, UserCourse
from utils.mixin_utils import LoginRequiredMixin


class CourseListView(View):
    def get(self, request):
        all_courses = Course.objects.all().order_by("-add_time")

        hot_courses = Course.objects.all().order_by("-click_nums")[:3]

        # 课程搜索
        search_keywords = request.GET.get('keywords', "")
        if search_keywords:
            all_courses = all_courses.filter(Q(name__icontains=search_keywords) |
                                             Q(desc__icontains=search_keywords) |
                                             Q(detail__icontains=search_keywords))  # i表示不区分大小写

        # 课程排序功能
        sort = request.GET.get('sort', "")
        if sort:
            if sort == "students":
                all_courses = all_courses.order_by("-students")
            elif sort == "hot":
                all_courses = all_courses.order_by("-click_nums")


        # 对课程分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_courses, 6, request=request)
        courses = p.page(page)

        return render(request, 'course-list.html', {
            "all_courses": courses,
            "hot_courses": hot_courses,
            "sort": sort,
        })


class CourseDetailView(View):
    """
    课程详情页
    """
    def get(self, request, course_id):
        course = Course.objects.get(id=course_id)

        # 增加课程点击数
        course.click_nums += 1
        course.save()

        has_fav_course = False
        has_fav_org = False

        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course.id, fav_type=1):
                has_fav_course = True

            if UserFavorite.objects.filter(user=request.user, fav_id=course.course_org.id, fav_type=2):
                has_fav_org = True

        tag = course.tag
        if tag:
            relate_courses = Course.objects.filter(tag=tag)[:1]
        else:
            relate_courses = []  # 空数组
        return render(request, 'course-detail.html', {
            'course': course,
            'relate_courses': relate_courses,
            'has_fav_course': has_fav_course,
            'has_fav_org': has_fav_org
        })


class CourseInfoView(LoginRequiredMixin, View):
    """
    课程章节信息
    """
    def get(self, request, course_id):
        course = Course.objects.get(id=course_id)

        # 增加学习人数 即点击开始学习后加1
        course.students += 1
        course.save()

        # 查询用户是否已经关联该课程
        user_course = UserCourse.objects.filter(user=request.user, course=course)
        if not user_course:
            user_course = UserCourse()
            user_course.user = request.user
            user_course.course = course
            user_course.save()

        user_courses = UserCourse.objects.filter(course=course)   # 获取学过该课程的 所有用户课程
        user_ids = [user_couser.user.id for user_couser in user_courses]  # 获取所有学过该课程的 用户课程 对应的用户的id
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids) # 根据用户id 获取这些用户的 用户课程 信息
        # 取出所有课程的id
        course_ids = [user_couser.course.id for user_couser in all_user_courses]
        # 获取学过该用户学过其他的所有课程
        relate_courses = Course.objects.filter(id__in=course_ids).order_by("-click_nums")
        all_resources = CourseResource.objects.filter(course=course)

        return render(request, "course-video.html", {
            "course": course,
            "course_resources": all_resources,
            "relate_courses": relate_courses,

        })


class CommentsView(LoginRequiredMixin, View):
    """
    课程评论
    """
    def get(self, request, course_id):
        course = Course.objects.get(id=course_id)
        all_resources = CourseResource.objects.filter(course=course)
        all_comments = CourseComment.objects.all()
        return render(request, "course-comment.html", {
            "course": course,
            "course_resources": all_resources,
            "all_comments": all_comments
        })


class AddCommentsView(View):
    """
    用户添加评论
    """
    def post(self, request):
        if not request.user.is_authenticated():
            # 判断用户登录状态
            return HttpResponse('{"status": "fail", "msg":"用户未登录"}', content_type='application/json')

        course_id = request.POST.get('course_id', '')
        comments = request.POST.get('comments', '')
        if course_id > 0 and comments:
            course_comment = CourseComment()
            course = Course.objects.get(id=course_id)
            course_comment.course = course
            course_comment.comments = comments
            course_comment.user = request.user
            course_comment.save()
            return HttpResponse('{"status": "success", "msg":"添加成功"}', content_type='application/json')
        else:
            return HttpResponse('{"status": "fail", "msg":"提交失败"}', content_type='application/json')