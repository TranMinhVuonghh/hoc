"""
Custom template tags và filters cho ứng dụng courses
"""
from django import template

register = template.Library()

@register.filter
def filter_by_lesson(progress_queryset, lesson):
    """
    Filter progress queryset để lấy progress của một bài học cụ thể
    Args:
        progress_queryset: QuerySet các progress
        lesson: Lesson object
    Returns:
        Progress object hoặc None
    """
    try:
        return progress_queryset.get(lesson=lesson)
    except:
        return None

@register.filter
def completed_lessons_count(enrollment):
    """
    Đếm số bài học đã hoàn thành của một ghi danh
    Args:
        enrollment: Enrollment object
    Returns:
        int: Số bài học đã hoàn thành
    """
    return enrollment.progress_set.filter(completed=True).count()

@register.filter
def total_lessons_count(enrollment):
    """
    Đếm tổng số bài học của một khóa học
    Args:
        enrollment: Enrollment object
    Returns:
        int: Tổng số bài học
    """
    return enrollment.course.lessons.count()

@register.simple_tag
def calculate_progress(completed, total):
    """
    Tính phần trăm tiến độ học tập
    Args:
        completed: Số bài học đã hoàn thành
        total: Tổng số bài học
    Returns:
        int: Phần trăm hoàn thành
    """
    try:
        return int((completed / total) * 100)
    except (ZeroDivisionError, TypeError):
        return 0

@register.simple_tag
def get_next_lesson(course, current_lesson):
    """
    Lấy bài học tiếp theo
    Args:
        course: Course object
        current_lesson: Lesson object hiện tại
    Returns:
        Lesson object hoặc None
    """
    try:
        return course.lessons.filter(order__gt=current_lesson.order).first()
    except:
        return None

@register.simple_tag
def get_previous_lesson(course, current_lesson):
    """
    Lấy bài học trước đó
    Args:
        course: Course object
        current_lesson: Lesson object hiện tại
    Returns:
        Lesson object hoặc None
    """
    try:
        return course.lessons.filter(order__lt=current_lesson.order).last()
    except:
        return None