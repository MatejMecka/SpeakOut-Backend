"""
test_posts/test_posts.py

Test all the Posts views
"""
from tests.base import BaseTestCase
from pobarajpomosh.auth.models import User, Role
from pobarajpomosh.posts.models import Post, Comment
from pobarajpomosh import db
import mock
import json
import uuid

class TestControllers(BaseTestCase):
    def test_post_create_invalid_token(self):
        """
        Test post Creation with invalid token
        """

        data = {
            "token": "LookAtMeImPickleRiiiiiick",
            "title": "Test",
            "body": "Testing 1,2,3",
            "category": "1"
        }

        response = self.app.test_client().post('/posts/api/post/create', json=data, content_type='application/json')
        self.assertEqual(json.loads(response.data), {"error": "Access Denied!"})

    def test_post_create_missing_field(self):
        """
        Test post Creation with invalid token
        """

        data = {
            "token": "LookAtMeImPickleRiiiiiick",
            "title": "Test",
            "body": "Testing 1,2,3",
        }

        response = self.app.test_client().post('/posts/api/post/create', json=data, content_type='application/json')
        self.assertEqual(json.loads(response.data), {"error": "A Field is missing!"})

    def test_post_creation(self):
        """
        Test post Creation
        """
        token = str(uuid.uuid4().hex)
        user = User(username='danche', role_id=4, token=token, approved=1)
        user.hash_password('dancingdanche')  # :))

        db.session.add(user)
        db.session.commit()

        data = {
            "token": token,
            "title": "Test",
            "body": "Testing 1,2,3",
            "category": "1"
        }

        response = self.app.test_client().post('/posts/api/post/create', json=data, content_type='application/json')
        data = json.loads(response.data)
        self.assertEqual(data['code'], 'Success')
        self.assertEqual(data['post_id'], 1)

        post = Post.query.filter_by(id=data['post_id']).first()
        self.assertEqual(post.approved, 1)

    def test_post_invalid(self):
        """
        Try to get invalid post
        """
        response = self.app.test_client().get('/posts/api/post/52', content_type='application/json')
        self.assertEqual(json.loads(response.data), {"error": "Post not found!"})

    def test_get_single_post(self):
        """
        Try to get an individual post
        """

        # Create New Account
        token = str(uuid.uuid4().hex)
        user = User(username='very_random_username', role_id=4, token=token, approved=1)
        user.hash_password('this_is_a_password')

        db.session.add(user)
        db.session.commit()

        # Create New Post
        data = {
            "token": token,
            "title": "Test",
            "body": "Testing 1,2,3",
            "category": "1"
        }

        writePost = self.app.test_client().post('/posts/api/post/create', json=data, content_type='application/json')
        postData = json.loads(writePost.data)

        postId = postData['post_id']

        # Test
        response = self.app.test_client().get('/posts/api/post/{}'.format(postId), content_type='application/json')
        data = json.loads(response.data)
        print(data)
        self.assertEqual(data['posts'][0]['title'], "Test")
        self.assertEqual(data['posts'][0]['body'], "Testing 1,2,3")
        self.assertEqual(data['posts'][0]['category'], 1)
        self.assertEqual(data['posts'][0]['approved'], 1)

    def test_posts_wall(self):
        """
        Test Post Wall
        """
        response = self.app.test_client().get('/posts/')
        self.assertEqual(response.status_code, 200)
        self.assert_template_used('posts.html')

    def test_comment_create_invalid_token(self):
        """
        Test comment Creation with invalid token
        """

        data = {
            "token": "JabolkoBanana",
            "body": "Testing 1,2,3",
            "post_id": "1"
        }

        response = self.app.test_client().post('/posts/api/comment/create', json=data, content_type='application/json')
        self.assertEqual(json.loads(response.data), {"error": "Access Denied!"})

    def test_comment_create_missing_field(self):
        """
        Test comment Creation with invalid token
        """

        data = {
            "title": "Test",
            "body": "#SpodeliLjubov<3",
        }

        response = self.app.test_client().post('/posts/api/comment/create', json=data, content_type='application/json')
        self.assertEqual(json.loads(response.data), {"error": "A Field is missing!"})

    def test_comment_creation(self):
        """
        Test comment Creation
        """
        token = str(uuid.uuid4().hex)
        user = User(username='amra', role_id=4, token=token, approved=1)
        user.hash_password('todothinkofsomething')  # :))

        db.session.add(user)
        db.session.commit()

        # Make New Post
        dataMakePost = {
            "token": token,
            "title": "Test",
            "body": "Testing 1,2,3",
            "category": "1"
        }

        makePost = self.app.test_client().post('/posts/api/post/create', json=dataMakePost,
                                               content_type='application/json')
        makePostData = json.loads(makePost.data)

        data = {
            "token": token,
            "body": "Testing 1,2,3",
            "post_id": makePostData['post_id']
        }

        response = self.app.test_client().post('/posts/api/comment/create', json=data, content_type='application/json')
        data = json.loads(response.data)
        self.assertEqual(data['code'], 'Success')
        self.assertEqual(data['comment_id'], 1)

        comment = Comment.query.filter_by(id=data['comment_id']).first()
        self.assertEqual(comment.approved, 1)

    def test_comment_invalid_token(self):
        """
        Test Post Approval with invalid token
        """

        data = {
            "token": "ToploChokolado",  # Mi se pieeeee mnooguuuuu
            "body": "Bananana",
            "post_id": "1"
        }

        response = self.app.test_client().post('/posts/api/comment/create', json=data, content_type='application/json')
        self.assertEqual(json.loads(response.data), {"error": "Access Denied!"})

    def test_post_invalid(self):
        """
        Try to get invalid post
        """
        response = self.app.test_client().get('/posts/api/post/52', content_type='application/json')
        self.assertEqual(json.loads(response.data), {"error": "Post not found!"})

    def test_post_approval_invalid_token(self):
        """
        Test Post Approval with invalid token
        """

        data = {
            "token": "ToploChokolado",  # Mi se pieeeee mnooguuuuu
            "post_id": "1"
        }

        response = self.app.test_client().post('/posts/api/post/approve', json=data, content_type='application/json')
        self.assertEqual(json.loads(response.data), {'error': 'Access Denied!'})

    def test_approval_post_approval(self):
        """
        Test Post Approval
        """

        # Create New Account
        response = self.app.test_client().post('/auth/api/login',
                                               json={'username': 'milche', 'password': 'muzikalnatamilche'},
                                               content_type='application/json')
        data = json.loads(response.data)

        # Make New Post
        dataMakePost = {
            "token": data['token'],
            "title": "Test",
            "body": "Testing 1,2,3",
            "category": "1"
        }

        makePost = self.app.test_client().post('/posts/api/post/create', json=dataMakePost,
                                               content_type='application/json')
        makePostData = json.loads(makePost.data)

        data = {
            "token": data['token'],
            "post_id": makePostData['post_id']
        }

        response = self.app.test_client().post('/posts/api/post/approve', json=data, content_type='application/json')
        self.assertEqual(json.loads(response.data), {'code': 'Approval Succesful!'})

        #### Test Non Approved Posts

        # Create New Post
        post = Post(author_id=1, title='Blablabla', body="nanananana", category=1, approved=1, likes=0)
        db.session.add(post)
        db.session.commit()

        data["post_id"] = post.id

        # Test A Post posted by non approved user
        second_response = self.app.test_client().post('/posts/api/post/approve', json=data,
                                                      content_type='application/json')
        self.assertEqual(json.loads(second_response.data), {'code': 'post has already been Approved!'})

        # Test with Invalid Post ID
        data['post_id'] = 50
        second_response = self.app.test_client().post('/posts/api/post/approve', json=data,
                                                      content_type='application/json')
        self.assertEqual(json.loads(second_response.data), {'error': 'Invalid post'})

        # Create New Account
        response = self.app.test_client().post('/auth/api/login',
                                               json={'username': 'randomusername', 'password': 'randompassword'},
                                               content_type='application/json')
        dat = json.loads(response.data)

        data['token'] = dat['token']
        data['post_id'] = 1

        second_response = self.app.test_client().post('/posts/api/post/approve', json=data,
                                                      content_type='application/json')
        self.assertEqual(json.loads(second_response.data), {'error': 'Access Denied!'})

    def test_invalid_approval(self):
        """
        Approve Post with a missing field
        """
        data = {"post_id": "1"}

        response = self.app.test_client().post('/posts/api/banana/approve', json=data, content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def test_lists_of_approved_posts(self):
        """
        Test List of Approved Posts
        """
        response = self.app.test_client().get('/posts/api/post/list/approved', content_type='application/json')
        data = json.loads(response.data)
        self.assertEqual(data, {'posts': [[], {}]})

    def test_lists_of_unapproved_posts_invalid_token(self):
        """
        Test Lists of Unapproved Posts with invalid token
        """
        response = self.app.test_client().get('/posts/api/post/list/unapproved?token=banana',
                                              content_type='application/json')
        self.assertEqual(json.loads(response.data), {"error": "Access Denied!"})

    def test_lists_of_unapproved_posts_invalid_permissions(self):
        """
        Test Lists of Unapproved Posts with invalid permissions
        """
        token = str(uuid.uuid4().hex)
        token2 = str(uuid.uuid4().hex)

        user = User(username='thisisajoke', role_id=3, token=token, approved=1)
        user2 = User(username='someusername', role_id=4, token=token, approved=1)
        user.hash_password('randomrandom')  # :))
        user2.hash_password('abetterpasswordbutnotthebest')

        db.session.add_all([user, user2])
        db.session.commit()

        response = self.app.test_client().get('/posts/api/post/list/unapproved?token={}'.format(token),
                                              content_type='application/json')
        self.assertEqual(json.loads(response.data), {"error": "Access Denied!"})

        response2 = self.app.test_client().get('/posts/api/post/list/unapproved?token={}'.format(token2),
                                              content_type='application/json')
        self.assertEqual(json.loads(response2.data), {"error": "Access Denied!"})



    def test_lists_of_unapproved_posts(self):
        """
        Test Lists of Unapproved Posts
        """
        # Create New Account
        token = str(uuid.uuid4().hex)
        user = User(username='randomsomething', role_id=1, token=token, approved=1)
        user.hash_password('randomrandom')  # :))

        db.session.add(user)
        db.session.commit()

        response = self.app.test_client().get('/posts/api/post/list/unapproved?token={}'
                                              .format(token), content_type='application/json')

        data = json.loads(response.data)

        self.assertEqual(data, {'posts': [[], {}]})

    def test_lists_of_comments_based_on_post(self):
        """
        Test List of Approved Comments based on Post
        """
        response = self.app.test_client().get('/posts/api/comments/list/1', content_type='application/json')
        data = json.loads(response.data)
        self.assertEqual(data, {'comments': [[], {}]})

    def test_lists_of_approved_posts_based_on_category(self):
        """
        Test List of Approved Posts
        """
        response = self.app.test_client().get('/posts/api/post/list/category/1', content_type='application/json')
        data = json.loads(response.data)
        self.assertEqual(data, {'posts': [[], {}]})

    def test_post_like(self):
        """
        Test Post Like
        """
        # Create Post with new account
        loginData = {
            "username": "randomusername",
            "password": "randompassword"
        }

        responseLogin = self.app.test_client().post('/auth/api/login', json=loginData, content_type='application/json')
        loginData = json.loads(responseLogin.data)

        dataPost = {
            'token': loginData['token'],
            'title': 'nesho',
            'body': 'nesho',
            'category': '1',
            'approved': '0',
        }

        post = self.makePost(dataPost)

        # Login to the platform to generate token
        loginData = {
            "username": "milche",
            "password": "muzikalnatamilche"
        }

        responseLogin = self.app.test_client().post('/auth/api/login', json=loginData, content_type='application/json')
        loginData = json.loads(responseLogin.data)

        # Like the Post

        dataPost = {
            'token': loginData['token'],
            'title': 'nesho',
            'body': 'nesho',
            'category': '1',
            'approved': '0',
        }

        post2 = self.makePost(dataPost)

        data = {
            "token": loginData['token'],
            "post_id": post
        }

        response = self.app.test_client().post('/posts/api/post/like', json=data, content_type='application/json')
        print('RESPONSE LIKE:' + str(response.data))
        self.assertEqual(json.loads(response.data), {"code": "Success"})

        # Like your own post to test if it will trigger an error
        data["post_id"] = post2
        thirdResponse = self.app.test_client().post('/posts/api/post/like', json=data, content_type='application/json')
        self.assertEqual(json.loads(thirdResponse.data), {"error": "You can't like your own post!"})

        data["post_id"] = post
        # Relike the post to test if it will trigger an error
        response = self.app.test_client().post('/posts/api/post/like', json=data, content_type='application/json')
        self.assertEqual(json.loads(response.data), {'error': 'You have already liked this!'})

    def test_post_like_missing_field(self):
        """
        Test like with missing field
        """
        data = {
            "post_id": 4
        }

        response = self.app.test_client().post('/posts/api/post/like', json=data, content_type='application/json')
        self.assertEqual(json.loads(response.data), {"error": "A Field is missing!"})

    def test_post_like_invalid_token(self):
        """
        Test like with missing field
        """
        data = {
            "token": "Machor",
            "post_id": 4
        }

        response = self.app.test_client().post('/posts/api/post/like', json=data, content_type='application/json')
        self.assertEqual(json.loads(response.data), {"error": "Access Denied!"})

    def test_comment_like(self):
        """
        Test Comment Like
        """
        # Create Commment with new account
        loginData = {
            "username": "randomusername",
            "password": "randompassword"
        }

        responseLogin = self.app.test_client().post('/auth/api/login', json=loginData, content_type='application/json')
        loginData = json.loads(responseLogin.data)

        # Make New Post
        dataMakePost = {
            "token": loginData['token'],
            "title": "Test",
            "body": "Testing 1,2,3",
            "category": "1"
        }

        makePost = self.app.test_client().post('/posts/api/post/create', json=dataMakePost,
                                               content_type='application/json')
        makePostData = json.loads(makePost.data)

        dataComment = {
            'token': loginData['token'],
            'body': 'nesho',
            'post_id': makePostData['post_id'],
            'approved': '0',
        }

        comment = self.makeComment(dataComment)

        # Login to the platform to generate token
        loginData = {
            "username": "milche",
            "password": "muzikalnatamilche"
        }

        responseLogin = self.app.test_client().post('/auth/api/login', json=loginData, content_type='application/json')
        loginData = json.loads(responseLogin.data)

        # Like the Comment
        data = {
            "token": loginData['token'],
            "comment_id": comment
        }

        response = self.app.test_client().post('/posts/api/comment/like', json=data, content_type='application/json')
        self.assertEqual(json.loads(response.data), {"code": "Success"})

        # Like your own post to test if it will trigger an error
        commentData = {
            "token": loginData['token'],
            "post_id": "1",
            "body": "Comment"
        }

        cmment = self.app.test_client().post('/posts/api/comment/create', json=commentData,
                                             content_type='application/json')
        dataComment = json.loads(cmment.data)
        data["comment_id"] = dataComment['comment_id']

        secondResponse = self.app.test_client().post('/posts/api/comment/like', json=data,
                                                     content_type='application/json')
        self.assertEqual(json.loads(secondResponse.data), {"error": "You can't like your own post!"})

    def test_comment_like_missing_field(self):
        """
        Test comment like with missing field
        """
        data = {
            "comment_id": 4
        }

        response = self.app.test_client().post('/posts/api/comment/like', json=data, content_type='application/json')
        self.assertEqual(json.loads(response.data), {"error": "A Field is missing!"})

    def test_comment_like_invalid_token(self):
        """
        Test comment like with invalid token
        """
        data = {
            "token": "Machor",
            "comment_id": 4
        }

        response = self.app.test_client().post('/posts/api/comment/like', json=data, content_type='application/json')
        self.assertEqual(json.loads(response.data), {"error": "Access Denied!"})

    def test_report_invalid_token(self):
        """
        Test comment like with invalid token
        """
        data = {
            "token": "Machor",
            "post_id": 4
        }

        response = self.app.test_client().post('/posts/api/post/report', json=data, content_type='application/json')
        self.assertEqual(json.loads(response.data), {'error': 'Access Denied!'})

    @mock.patch('pobarajpomosh.volunteers.views.send_slack_message')
    @mock.patch('slack.WebClient.chat_postMessage')
    def test_report_post(self, mock_get, mock_sc):
        mock_get.return_value.status_code = 200
        mock_sc.return_value.status_code = 200
        # Login to the platform to generate token
        loginData = {
            "username": "milche",
            "password": "muzikalnatamilche"
        }

        responseLogin = self.app.test_client().post('/auth/api/login', json=loginData, content_type='application/json')
        loginData = json.loads(responseLogin.data)

        # Create Post
        dataPost = {
            'token': loginData['token'],
            'title': 'nesho',
            'body': 'nesho',
            'category': '1',
            'approved': '0',
        }

        post = self.makePost(dataPost)

        # Flag Post
        data = {
            'token': loginData['token'],
            'post_id': post
        }

        response = self.app.test_client().post('/posts/api/post/report', json=data, content_type='application/json')
        self.assertEqual(json.loads(response.data), {'code': 'Report Successful!'})

        data['post_id'] = 50

        response = self.app.test_client().post('/posts/api/post/report', json=data, content_type='application/json')
        self.assertEqual(json.loads(response.data), {'error': 'Invalid post'})

    def test_report_comment_invalid_token(self):
        """
        Test comment like with invalid token
        """
        data = {
            "token": "Machor",
            "comment_id": 4
        }

        response = self.app.test_client().post('/posts/api/comment/report', json=data, content_type='application/json')
        self.assertEqual(json.loads(response.data), {'error': 'Access Denied!'})

    @mock.patch('pobarajpomosh.volunteers.views.send_slack_message')
    @mock.patch('slack.WebClient.chat_postMessage')
    def test_report_comment(self, mock_get, mock_sc):
        mock_get.return_value.status_code = 200
        mock_sc.return_value.status_code = 200
        # Login to the platform to generate token
        loginData = {
            "username": "milche",
            "password": "muzikalnatamilche"
        }

        responseLogin = self.app.test_client().post('/auth/api/login', json=loginData, content_type='application/json')
        loginData = json.loads(responseLogin.data)

        # Create Comment
        dataComment = {
            'token': loginData['token'],
            'body': 'nesho',
            'post_id': '1',
            'approved': '0',
        }

        comment = self.makeComment(dataComment)

        # Flag Post
        data = {
            'token': loginData['token'],
            'comment_id': comment
        }

        response = self.app.test_client().post('/posts/api/comment/report', json=data, content_type='application/json')
        self.assertEqual(json.loads(response.data), {'code': 'Report Successful!'})

        # Test With Invalid ID
        data['comment_id'] = 50
        response = self.app.test_client().post('/posts/api/comment/report', json=data, content_type='application/json')
        self.assertEqual(json.loads(response.data), {'error': 'Invalid comment'})

    def test_post_unapproval_invalid_token(self):
        """
        Test Post Approval with invalid token
        """

        data = {
            "token": "ToploChokolado",  # Mi se pieeeee mnooguuuuu
            "post_id": "1"
        }

        response = self.app.test_client().post('/posts/api/post/unapprove', json=data, content_type='application/json')
        self.assertEqual(json.loads(response.data), {'error': 'Access Denied!'})

    def test_unapproval_post_approval(self):
        """
        Test Post Approval
        """

        # Create New Account
        response = self.app.test_client().post('/auth/api/login',
                                               json={'username': 'milche', 'password': 'muzikalnatamilche'},
                                               content_type='application/json')
        data = json.loads(response.data)

        # Make New Post
        dataMakePost = {
            "token": data['token'],
            "title": "Test",
            "body": "Testing 1,2,3",
            "category": "1"
        }

        makePost = self.app.test_client().post('/posts/api/post/create', json=dataMakePost,
                                               content_type='application/json')
        makePostData = json.loads(makePost.data)

        # Approve Posts
        post = Post.query.filter_by(id=makePostData['post_id']).first()
        post.approved += 1

        data = {
            "token": data['token'],
            "post_id": makePostData['post_id']
        }

        response = self.app.test_client().post('/posts/api/post/unapprove', json=data, content_type='application/json')
        self.assertEqual(json.loads(response.data), {'code': 'Unapproval Succesful!'})

        #### Test Non Approved Posts

        # Create New Post
        post = Post(author_id=1, title='Blablabla', body="nanananana", category=1, approved=0, likes=0)
        db.session.add(post)
        db.session.commit()

        data["post_id"] = post.id

        # Test A Post posted by non approved user
        second_response = self.app.test_client().post('/posts/api/post/unapprove', json=data,
                                                      content_type='application/json')
        self.assertEqual(json.loads(second_response.data), {'code': 'post has not been approved yet!'})

        # Test with Invalid Post ID
        data['post_id'] = 50
        second_response = self.app.test_client().post('/posts/api/post/unapprove', json=data,
                                                      content_type='application/json')
        self.assertEqual(json.loads(second_response.data), {'error': 'Invalid post'})

        # Test With Invalid Permission

        # Create New Account
        response = self.app.test_client().post('/auth/api/login',
                                               json={'username': 'randomusername', 'password': 'randompassword'},
                                               content_type='application/json')
        dat = json.loads(response.data)

        data['token'] = dat['token']
        data['post_id'] = 1

        second_response = self.app.test_client().post('/posts/api/post/unapprove', json=data,
                                                      content_type='application/json')
        self.assertEqual(json.loads(second_response.data), {'error': 'Access Denied!'})


    def test_comment_unapproval_invalid_token(self):
        """
        Test Post Approval with invalid token
        """

        data = {
            "token": "ToploChokolado",  # Mi se pieeeee mnooguuuuu
            "comment_id": "1"
        }

        response = self.app.test_client().post('/posts/api/comment/unapprove', json=data,
                                               content_type='application/json')
        self.assertEqual(json.loads(response.data), {'error': 'Access Denied!'})

    def test_unapproval_comment(self):
        """
        Test Post Approval
        """

        # Create New Account
        response = self.app.test_client().post('/auth/api/login',
                                               json={'username': 'milche', 'password': 'muzikalnatamilche'},
                                               content_type='application/json')
        data = json.loads(response.data)

        # Make New Post
        dataMakePost = {
            "token": data['token'],
            "title": "Test",
            "body": "Testing 1,2,3",
            "category": "1"
        }

        makePost = self.app.test_client().post('/posts/api/post/create', json=dataMakePost,
                                               content_type='application/json')
        makePostData = json.loads(makePost.data)

        # Make New Post
        dataMakeComment = {
            "token": data['token'],
            "body": "Testing 1,2,3",
            "post_id": "1"
        }

        makeComment = self.app.test_client().post('/posts/api/comment/create', json=dataMakeComment,
                                                  content_type='application/json')
        makeCommentData = json.loads(makeComment.data)

        # Approve Posts
        comment = Comment.query.filter_by(id=makeCommentData['comment_id']).first()
        comment.approved += 1

        data = {
            "token": data['token'],
            "comment_id": makeCommentData['comment_id']
        }

        response = self.app.test_client().post('/posts/api/comment/unapprove', json=data,
                                               content_type='application/json')
        self.assertEqual(json.loads(response.data), {'code': 'Unapproval Succesful!'})

        #### Test Non Approved Posts

        # Create New Comment
        comment = Comment(author_id=1, post_id=1, body="nanananana", approved=0, likes=0)
        db.session.add(comment)
        db.session.commit()

        data["comment_id"] = comment.id

        # Test A Post posted by non approved user
        second_response = self.app.test_client().post('/posts/api/comment/unapprove', json=data,
                                                      content_type='application/json')
        self.assertEqual(json.loads(second_response.data), {'code': 'comment has not been approved yet!'})

        # Test with Invalid Post ID
        data['comment_id'] = 50
        second_response = self.app.test_client().post('/posts/api/comment/unapprove', json=data,
                                                      content_type='application/json')
        self.assertEqual(json.loads(second_response.data), {'error': 'Invalid comment'})

        # Create New Account
        response = self.app.test_client().post('/auth/api/login',
                                               json={'username': 'randomusername', 'password': 'randompassword'},
                                               content_type='application/json')
        dat = json.loads(response.data)

        data['token'] = dat['token']
        data['comment_id'] = 1

        second_response = self.app.test_client().post('/posts/api/comment/unapprove', json=data,
                                                      content_type='application/json')
        self.assertEqual(json.loads(second_response.data), {'error': 'Access Denied!'})

    def test_comment_approval_invalid_token(self):
        """
        Test Post Approval with invalid token
        """

        data = {
            "token": "ToploChokolado",  # Mi se pieeeee mnooguuuuu
            "comment_id": "1"
        }

        response = self.app.test_client().post('/posts/api/comment/approve', json=data, content_type='application/json')
        self.assertEqual(json.loads(response.data), {'error': 'Access Denied!'})

    def test_approval_comment_approval(self):
        """
        Test Post Approval
        """

        # Create New Account
        response = self.app.test_client().post('/auth/api/login',
                                               json={'username': 'milche', 'password': 'muzikalnatamilche'},
                                               content_type='application/json')
        data = json.loads(response.data)

        # Make New Post
        dataMakePost = {
            "token": data['token'],
            "title": "Test",
            "body": "Testing 1,2,3",
            "category": "1"
        }

        makePost = self.app.test_client().post('/posts/api/post/create', json=dataMakePost,
                                               content_type='application/json')
        makePostData = json.loads(makePost.data)

        # Make New Comment
        dataMakeComment = {
            "token": data['token'],
            "body": "Testing 1,2,3",
            "post_id": makePostData['post_id']
        }

        makeComment = self.app.test_client().post('/posts/api/comment/create', json=dataMakeComment,
                                                  content_type='application/json')
        makeCommentData = json.loads(makeComment.data)

        data = {
            "token": data['token'],
            "comment_id": makeCommentData['comment_id']
        }

        response = self.app.test_client().post('/posts/api/comment/approve', json=data, content_type='application/json')
        self.assertEqual(json.loads(response.data), {'code': 'Approval Succesful!'})

        #### Test Non Approved Posts

        # Create New Post
        comment = Comment(author_id=1, body="nanananana", post_id=1, approved=1, likes=0)
        db.session.add(comment)
        db.session.commit()

        data["comment_id"] = comment.id

        # Test A Post posted by non approved user
        second_response = self.app.test_client().post('/posts/api/comment/approve', json=data,
                                                      content_type='application/json')
        self.assertEqual(json.loads(second_response.data), {'code': 'comment has already been Approved!'})

        # Test with Invalid Post ID
        data["comment_id"] = 50
        second_response = self.app.test_client().post('/posts/api/comment/approve', json=data,
                                                      content_type='application/json')
        self.assertEqual(json.loads(second_response.data), {'error': 'Invalid comment'})

        # Create New Account
        response = self.app.test_client().post('/auth/api/login',
                                               json={'username': 'randomusername', 'password': 'randompassword'},
                                               content_type='application/json')
        dat = json.loads(response.data)

        data['token'] = dat['token']
        data['comment_id'] = 1

        second_response = self.app.test_client().post('/posts/api/comment/approve', json=data,
                                                      content_type='application/json')
        self.assertEqual(json.loads(second_response.data), {'error': 'Access Denied!'})

    def test_list_user_posts(self):
        """
        Test Lists of Unapproved Posts
        """
        # Create New Account
        token = str(uuid.uuid4().hex)
        user = User(username='randomsomething', role_id=1, token=token, approved=1)
        user.hash_password('randomrandom')  # :))

        db.session.add(user)
        db.session.commit()

        response = self.app.test_client().get('/posts/api/post/list/user?token={}'
                                              .format(token), content_type='application/json')

        data = json.loads(response.data)

        self.assertEqual(data, {'posts': [[], {}]})

    def test_list_user_invalid_user_id(self):
        """
        Test Lists of Unapproved Posts
        """
        response = self.app.test_client().get('/posts/api/post/list/user?token={}'
                                              .format('banana'), content_type='application/json')

        data = json.loads(response.data)

        self.assertEqual(data, {'error': 'Access Denied!'})

    def test_invalid_token_post_removal(self):
        """
        Test Post Removal with invalid token
        """
        response = self.app.test_client().post('/posts/api/post/remove',
                                               json={'post_id': '5', 'token': 'nesho'}, content_type='application/json')
        self.assertEqual(json.loads(response.data), {'error': 'Access Denied!'})

    def test_post_removal(self):
        """
        Test Post Removal
        """

        # Create New Account
        response = self.app.test_client().post('/auth/api/login',
                                               json={'username': 'milche', 'password': 'muzikalnatamilche'},
                                               content_type='application/json')
        data = json.loads(response.data)

        # Create Another Account to get permission denied
        responseLogin = self.app.test_client().post('/auth/api/login',
                                                    json={'username': 'randomusername', 'password': 'randompassword'},
                                                    content_type='application/json')
        dataLogin = json.loads(responseLogin.data)

        token = data['token']

        # Make New Post
        dataMakePost = {
            "token": token,
            "title": "Test",
            "body": "Testing 1,2,3",
            "category": "1"
        }

        makePost = self.app.test_client().post('/posts/api/post/create', json=dataMakePost,
                                               content_type='application/json')
        makePostData = json.loads(makePost.data)

        data = {
            "token": token,
            "post_id": 50
        }

        # Send an Invalid Post ID

        response = self.app.test_client().post('/posts/api/post/remove', json=data, content_type='application/json')
        self.assertEqual(json.loads(response.data), {'error': 'Invalid post'})

        data['post_id'] = makePostData['post_id']
        data['token'] = dataLogin['token']

        response = self.app.test_client().post('/posts/api/post/remove', json=data, content_type='application/json')
        self.assertEqual(json.loads(response.data), {'error': 'Access Denied!'})

        data["token"] = token

        response = self.app.test_client().post('/posts/api/post/remove', json=data, content_type='application/json')
        self.assertEqual(json.loads(response.data), {'code': 'Deletion Succesful!'})

    def test_invalid_token_comment_removal(self):
        """
        Test Comment Removal with invalid token
        """
        response = self.app.test_client().post('/posts/api/comment/remove',
                                               json={'comment_id': '5', 'token': 'nesho'},
                                               content_type='application/json')
        self.assertEqual(json.loads(response.data), {'error': 'Access Denied!'})

    def test_comment_removal(self):
        """
        Test Comment Removal
        """

        # Create New Account
        response = self.app.test_client().post('/auth/api/login',
                                               json={'username': 'milche', 'password': 'muzikalnatamilche'},
                                               content_type='application/json')
        data = json.loads(response.data)

        # Create Another Account to get permission denied
        responseLogin = self.app.test_client().post('/auth/api/login',
                                                    json={'username': 'randomusername', 'password': 'randompassword'},
                                                    content_type='application/json')
        dataLogin = json.loads(responseLogin.data)

        token = data['token']

        # Make New Post
        dataMakePost = {
            "token": token,
            "title": "Test",
            "body": "Testing 1,2,3",
            "category": "1"
        }

        makePost = self.app.test_client().post('/posts/api/post/create', json=dataMakePost,
                                               content_type='application/json')
        makePostData = json.loads(makePost.data)

        # Make New Post
        dataMakeComment = {
            "token": token,
            "body": "Testing 1,2,3",
            "post_id": makePostData['post_id']
        }

        makeComment = self.app.test_client().post('/posts/api/comment/create', json=dataMakeComment,
                                                  content_type='application/json')
        makeCommentData = json.loads(makeComment.data)

        data = {
            "token": token,
            "comment_id": 50
        }

        # Send an Invalid Post ID

        response = self.app.test_client().post('/posts/api/comment/remove', json=data, content_type='application/json')
        self.assertEqual(json.loads(response.data), {'error': 'Invalid comment'})

        data['comment_id'] = makeCommentData['comment_id']
        data['token'] = dataLogin['token']

        response = self.app.test_client().post('/posts/api/comment/remove', json=data, content_type='application/json')
        self.assertEqual(json.loads(response.data), {'error': 'Access Denied!'})

        data["token"] = token

        response = self.app.test_client().post('/posts/api/comment/remove', json=data, content_type='application/json')
        self.assertEqual(json.loads(response.data), {'code': 'Deletion Succesful!'})
