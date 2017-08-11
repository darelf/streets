/* comment code */
var contact_key = document.getElementById('contact-key').value
var ctype = document.getElementById('contact-type').value
var comment_input = document.getElementById('comment-input')
var comment_wrap = document.getElementById('comment-wrapper')
if (document.getElementById('open-comment')) {
  document.getElementById('open-comment').addEventListener('click', function() {
    comment_wrap.classList.remove('hidden')
  })
}

if (document.getElementById('comment-btn')) {
  document.getElementById('comment-btn').addEventListener('click', function() {
    var txt = document.getElementById('comment-input').value
    post_comment(contact_key, txt)
  })
}

if (document.getElementById('comment-cancel')) {
  document.getElementById('comment-cancel').addEventListener('click', function() {
    comment_wrap.classList.add('hidden')
    comment_input.value = ''
  })
}

function post_comment(t, contact_name, text) {
  var data = {
    type: t,
    name: contact_name,
    msg: text
  }
  var xhr = new XMLHttpRequest()
  xhr.open('POST', '/comment')
  xhr.setRequestHeader('content-type', 'application/json')
  xhr.onreadystatechange = function() {
    if (xhr.readyState === XMLHttpRequest.DONE) {
      comment_wrap.classList.add('hidden')
      location.reload()
    }
  }
  xhr.send( JSON.stringify(data) )
}