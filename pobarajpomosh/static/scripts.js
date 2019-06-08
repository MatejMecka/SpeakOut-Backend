const deletePost = function(id){
	const token = document.getElementById('deletePost').dataset.token
	const url = window.location.origin + '/posts/api/post/unapprove'

	const data = {'token': `${token}`, 'post_id': `${id}`}

	fetch(url, {
    	method: 'post',
    	body: JSON.stringify(data),
        headers: {
            "Content-Type": "application/json"
        }
  	}).then(function(response) {
    	return response.text();
  	}).then(function(data) {
        console.log(data)
        dat = JSON.parse(data)
        alert(dat['code'])
        window.location.reload(forceReload=true)
  	});

}

const approvePost = function(id){
	const token = document.getElementById('approvePost').dataset.token
	const url = window.location.origin + '/posts/api/post/approve'

	const data = {'token': `${token}`, 'post_id': `${id}`}

	fetch(url, {
    	method: 'post',
    	body: JSON.stringify(data),
        headers: {
            "Content-Type": "application/json"
        }
  	}).then(function(response) {
    	return response.text();
  	}).then(function(data) {
        console.log(data)
        dat = JSON.parse(data)
        alert(dat['code'])
        window.location.reload(forceReload=true)
  	});

}

const deleteComment = function(id){
	const token = document.getElementById('deleteComment').dataset.token
	const url = window.location.origin + '/posts/api/comment/unapprove'

	const data = {'token': `${token}`, 'comment_id': `${id}`}

	fetch(url, {
    	method: 'post',
    	body: JSON.stringify(data),
        headers: {
            "Content-Type": "application/json"
        }
  	}).then(function(response) {
    	return response.text();
  	}).then(function(data) {
        console.log(data)
        dat = JSON.parse(data)
        alert(dat['code'])
        window.location.reload(forceReload=true)
  	});

}

const approveComment = function(id){
	const token = document.getElementById('approveComment').dataset.token
	const url = window.location.origin + '/posts/api/comment/approve'

	const data = {'token': `${token}`, 'comment_id': `${id}`}

	fetch(url, {
    	method: 'post',
    	body: JSON.stringify(data),
        headers: {
            "Content-Type": "application/json"
        }
  	}).then(function(response) {
    	return response.text();
  	}).then(function(data) {
        console.log(data)
        dat = JSON.parse(data)
        alert(dat['code'])
        window.location.reload(forceReload=true)
  	});

}

const getUsername = function(token){
	const url = window.location.origin + '/auth/api/userinfo'
	const data = {'token': `${token}`}

	fetch(url, {
    	method: 'post',
    	body: JSON.stringify(data),
        headers: {
            "Content-Type": "application/json"
        }
  	}).then(function(response) {
    	return response.text();
  	}).then(function(data) {
        console.log(data)
        dat = JSON.parse(data)
		return dat['username']
  	});

}

