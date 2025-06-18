# comment_list/views.py

from django.http import JsonResponse
from .models import SocialCommentInteraction, SocialMediaPost

def get_user_comments(request):
    # 获取当前用户的ID
    current_user_id = request.GET.get('current_user_id')
    if not current_user_id:
        return JsonResponse(
            {'code': 400, 'message': '缺少current_user_id参数'},
            status=400
        )

    try:
        # 获取当前用户发布的所有帖子
        posts = SocialMediaPost.objects.filter(uid=current_user_id)

        # 获取每个帖子的评论
        comments = []
        for post in posts:
            post_comments = SocialCommentInteraction.objects.filter(post_id=post.post_id).values(
                'interact_id', 'uid', 'content', 'interact_time'
            )
            post_data = {
                'post_id': post.post_id,
                'post_title': post.post_title,
                'comments': [
                    {
                        'interact_id': comment['interact_id'],
                        'user_id': comment['uid'],  # 直接使用 uid，而不访问 uid_id
                        'content': comment['content'],
                        'interact_time': comment['interact_time'].strftime('%Y-%m-%d %H:%M')
                    }
                    for comment in post_comments
                ]
            }
            comments.append(post_data)

        return JsonResponse({'code': 200, 'message': 'Success', 'data': comments})

    except Exception as e:
        return JsonResponse(
            {'code': 500, 'message': f'服务器错误: {str(e)}'},
            status=500
        )
