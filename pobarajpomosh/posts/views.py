"""
posts/views.py

Controller Responsible for Handling the posts

"""

from flask import render_template, request, jsonify, abort
from pobarajpomosh.posts import posts_bp
from pobarajpomosh.auth.models import User
from pobarajpomosh.volunteers.views import send_slack_message
from pobarajpomosh.posts.models import Post, Like, posts_schema, post_schema, Comment, comments_schema, LikeComment
from pobarajpomosh.notifications.models import DevicesNotificationHandlers
from pobarajpomosh.notifications.views import sendNotification
from pobarajpomosh.decorators import check_valid_token, check_missing_fields, check_access_rights, check_valid_method
from sqlalchemy import desc
from pobarajpomosh import db
import os

admins = User.query.filter_by(role_id=1).all()
moderators = User.query.filter_by(role_id=2).all()

moderationTeam = admins + moderators


@posts_bp.route('/api/post/create', methods=['POST'])
@check_missing_fields(["token", "title", "body", "category"])
@check_valid_token
def create():
    """
    <url>/api/post/create

    Create Posts
    """
    token = request.json.get('token')
    title = request.json.get('title')
    body = request.json.get('body')
    category = request.json.get('category')

    user = User.query.filter_by(token=token).first()

    approved = 0

    if user.approved == 1:
        approved = 1

    post = Post(author_id=user.id, title=title, body=body, category=category, approved=approved, likes=0,
                reported=1)  # todo: Not having to report posts, just list all posts with a delete button

    db.session.add(post)
    db.session.commit()

    for moderator in moderationTeam:
        # Get The User to send the notification too
        device = DevicesNotificationHandlers.query.filter_by(user_id=moderator.id).first()

        # Send a Notification if we have a valid user with a valid notificationToken
        if device is not None:
            token = device.notificationToken
            title = "Објавен е нов Пост од Корисник!"
            body = "Нов Пост е во Модерацискиот Ред! Ве молиме одобрете или избрешето го!"
            sendNotification(token, title, body, extraData={"post_id": post.id}, channelID="postModeration")

    return jsonify({"code": "Success", "post_id": post.id})


@posts_bp.route('/api/post/<id>', methods=['GET'])
def show_post(id):
    """
    <url>/api/post/<id>

    Retrieve Post by Id
    """
    post = Post.query.filter_by(id=id).first()

    if post is None:
        return jsonify({"error": "Post not found!"})

    result = post_schema.dump(post)

    return jsonify({
        "posts": result
    })


@posts_bp.route('/api/post/list/approved', methods=['GET'])
def list():
    """
    <url>/posts/api/post/approve

    View that lists the approved posts
    """
    limit = request.args.get('length', default=25)
    posts = Post.query.filter_by(approved=1).order_by(desc('created')).limit(limit)
    result = posts_schema.dump(posts)

    return jsonify({
        "posts": result
    })


@posts_bp.route('/api/post/list/unapproved', methods=['GET'])
def list_unapproved():
    """
    <url>/posts/api/list/unapproved

    View that Lists all the unapproved posts
    """
    limit = request.args.get('length', default=25)
    token = request.args.get('token')

    user = User.query.filter_by(token=token).first()

    if user is None:
        return jsonify({"error": "Access Denied!"})

    # This is only limited to Moderators, Admins.
    if user.role_id in [3, 4]:
        return jsonify({"error": "Access Denied!"})

    posts = Post.query.filter_by(approved=0).order_by(desc('created')).limit(limit)
    result = posts_schema.dump(posts)

    return jsonify({
        "posts": result
    })


@posts_bp.route('/api/post/list/category/<id>', methods=['GET'])
def list_category(id):
    """
    <url>/api/post/list/category/<id>

    List posts based on the category assigned
    """
    limit = request.args.get('length', default=25)
    posts = Post.query.filter_by(approved=1, category=id).order_by(desc('created')).limit(limit)
    result = posts_schema.dump(posts)

    return jsonify({
        "posts": result
    })


@posts_bp.route('/api/post/like', methods=['POST'])
@check_missing_fields(["token", "post_id"])
@check_valid_token
def like_post():
    """
    <url>/api/post/like

    Like Posts
    """
    token = request.json.get('token')
    post_id = request.json.get('post_id')

    user = User.query.filter_by(token=token).first()
    post = Post.query.filter_by(id=post_id).first()

    if post.author_id == user.id:
        return jsonify({"error": "You can't like your own post!"})

    if Like.query.filter_by(id=post_id, user_id=user.id).first() is not None:
        return jsonify({"error": "You have already liked this!"})

    post.likes += 1
    like = Like(post_id=post.id, user_id=user.id)
    db.session.add(like)
    db.session.commit()

    return jsonify({"code": "Success"})


@posts_bp.route('/api/comment/create', methods=['POST'])
@check_missing_fields(["token", "body", "post_id"])
@check_valid_token
def create_comment():
    """
    <url>/api/comment/create

    View that Creates Comments
    """
    token = request.json.get('token')
    body = request.json.get('body')
    post_id = request.json.get('post_id')

    user = User.query.filter_by(token=token).first()

    approved = 0

    if user.approved == 1:
        approved = 1

    # todo: Not having to report comments, just list all posts with a delete button
    comment = Comment(author_id=user.id, body=body, approved=approved, post_id=post_id, likes=0, reported=1)

    db.session.add(comment)
    db.session.commit()

    # Find The Original Poster
    op = Post.query.filter_by(id=post_id).first()
    op = op.author_id

    # Get The User to send the notification too
    device = DevicesNotificationHandlers.query.filter_by(user_id=op).first()

    # Send a Notification if we have a valid user with a valid notificationToken
    if device is not None:
        token = device.notificationToken
        title = "Имаш нов коментар на твојот пост!"
        body = "Анонимна личност ви остави коментар на еден од вашите постови!"
        sendNotification(token, title, body, extraData={"post_id": post_id, "comment_id": comment.id}, channelID="commentReply")

    for moderator in moderationTeam:
        # Get The User to send the notification too
        device = DevicesNotificationHandlers.query.filter_by(user_id=moderator.id).first()

        # Send a Notification if we have a valid user with a valid notificationToken
        if device is not None:
            token = device.notificationToken
            title = "Објавен е нов Коментар од Корисник!"
            body = "Нов Коментар е во Модерацискиот Ред! Ве молиме одобрете или избрешето го!"
            sendNotification(token, title, body, extraData={"post_id": post_id, "comment_id": comment.id}, channelID="commentModeration")

    return jsonify({"code": "Success", "comment_id": comment.id})


@posts_bp.route('/api/comment/like', methods=['POST'])
@check_missing_fields(["token", "comment_id"])
@check_valid_token
def like_comment():
    """
    <url>/posts/api/comment/like

    View that likes comments
    """
    token = request.json.get('token')
    comment_id = request.json.get('comment_id')

    user = User.query.filter_by(token=token).first()

    comment = Comment.query.filter_by(id=comment_id).first()

    if comment.author_id == user.id:
        return jsonify({"error": "You can't like your own post!"})

    if Like.query.filter_by(id=comment_id, user_id=user.id).first() is not None:
        return jsonify({"error": "You have already liked this!"})

    comment.likes += 1
    like = LikeComment(comment_id=comment.id, user_id=user.id)
    db.session.add(like)
    db.session.commit()

    return jsonify({"code": "Success"})


@posts_bp.route('/api/comments/list/<post_id>', methods=['GET'])
def list_comments_by_post(post_id):
    """
    <url>/posts/api/comments/list/<post_id>

    List the Comments for a post
    """
    limit = request.args.get('length', default=25)
    posts = Comment.query.filter_by(approved=1, post_id=post_id).limit(limit)
    result = comments_schema.dump(posts)

    return jsonify({
        "comments": result
    })


@posts_bp.route('/api/<method>/approve', methods=['POST'])
@check_valid_method
@check_valid_token
@check_access_rights([1, 2])
def approve_submission(method):
    """
    <url>/posts/api/<post|comment>/approve

    View that approves a post and deletes reports

    """
    submission = None

    # Determine if it's a post or comment and get the Submission reference
    if method == 'post':
        post_id = request.json.get('post_id')
        submission = Post.query.filter_by(id=post_id).first()
    else:
        # check_valid_method eliminates the rest so it must be a comment
        comment_id = request.json.get('comment_id')
        submission = Comment.query.filter_by(id=comment_id).first()

    if submission is None:
        return jsonify({'error': f'Invalid {method}'})

    if submission.approved == 1 and submission.reported == 0:
        return jsonify({'code': f'{method} has already been Approved!'})

    submission.approved = 1
    submission.reported = 0
    return jsonify({'code': 'Approval Succesful!'})


@posts_bp.route('/api/<method>/unapprove', methods=['POST'])
@check_valid_method
@check_valid_token
@check_access_rights([1, 2])
def unapprove_submission(method):
    """
    <url>/posts/api/<post|comment>/unapprove

    View that approves a post

    """
    submission = None

    # Determine if it's a post or comment and get the Submission reference
    if method == 'post':
        post_id = request.json.get('post_id')
        submission = Post.query.filter_by(id=post_id).first()
    else:
        # check_valid_method eliminates the rest so it must be a comment
        comment_id = request.json.get('comment_id')
        submission = Comment.query.filter_by(id=comment_id).first()

    if submission is None:
        return jsonify({'error': f'Invalid {method}'})

    if submission.approved == 0:
        return jsonify({'code': f'{method} has not been approved yet!'})

    submission.approved = 0
    return jsonify({'code': 'Unapproval Succesful!'})

@posts_bp.route('/api/<method>/report', methods=['POST'])
@check_valid_method
@check_valid_token
def report_submission(method):
    """
    <url>/posts/api/<post|method>/report

    View that report a post

    """
    token = request.json.get('token')
    user = User.query.filter_by(token=token).first()

    submission = None

    # Determine if it's a post or comment and get the Submission reference
    if method == 'post':
        post_id = request.json.get('post_id')
        submission = Post.query.filter_by(id=post_id).first()
    else:
        # check_valid_method eliminates the rest so it must be a comment
        comment_id = request.json.get('comment_id')
        submission = Comment.query.filter_by(id=comment_id).first()


    if submission is None:
        # No Post has been Located
        return jsonify({'error': f'Invalid {method}'})

    submission.reported = 1

    # Set the message based on the method
    if method == 'post':
        message = f'<!channel> {user.username} has reported a inappropriate post!\n\n Title: {submission.title}\n\n Body: {submission.body}\n\n ' \
                  'Please flag it via the website!'
    else:
        message = f'<!channel> {user.username} has reported a inappropriate comment!\n\n \n\n Body: {submission.body}\n\n ' \
              'Please flag it via the website!'


    send_slack_message(message, os.environ['SLACK_MODERATORS_CHAT_ID'])

    return jsonify({'code': 'Report Successful!'})


@posts_bp.route('/api/post/list/user', methods=['GET'])
def list_posts_by_user():
    """
    <url>/posts/api/list/user

    View that Lists all the posts by user
    """
    limit = request.args.get('length', default=25)
    token = request.args.get('token')

    user = User.query.filter_by(token=token).first()
    if user is None:
        return jsonify({"error": "Access Denied!"})

    posts = Post.query.filter_by(author_id=user.id).order_by(desc('created')).limit(limit)
    result = posts_schema.dump(posts)

    return jsonify({
        "posts": result
    })

@posts_bp.route('/api/<method>/remove', methods=['POST'])
@check_valid_method
@check_valid_token
def remove_submission(method):
    """
    <url>/posts/api/post/remove

    Remove your own post or others if you have the right permissions

    """
    token = request.json.get('token')
    user = User.query.filter_by(token=token).first()

    # Determine if it's a post or comment and get the Submission reference
    if method == 'post':
        post_id = request.json.get('post_id')
        submission = Post.query.filter_by(id=post_id).first()
    else:
        # check_valid_method eliminates the rest so it must be a comment
        comment_id = request.json.get('comment_id')
        submission = Comment.query.filter_by(id=comment_id).first()

    if submission is None:
        # No Submission has been located
        return jsonify({'error': f'Invalid {method}'})

    # Who can Approve Users
    if user.role_id in [1, 2] or user.id == submission.author_id:
        db.session.delete(submission)
        db.session.commit()
        return jsonify({'code': 'Deletion Succesful!'})
    else:
        return jsonify({'error': 'Access Denied!'})


@posts_bp.route('/', methods=['GET'])
def list_posts():
    """
    <url>/posts

    Display the beautiful posts :))
    """
    posts = Post.query.filter_by(approved=1).order_by(desc('created'))
    return render_template('posts.html', posts=posts)