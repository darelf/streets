/* login code */
var login_name_elem = document.getElementById('login-welcome')
var login_form = document.getElementById('login-section')

login_name_elem.addEventListener('click', function() {
  login_name_elem.classList.add('hidden')
  login_form.classList.remove('hidden')
})

document.getElementById('pword').addEventListener('keyup', function(ev) {
  if (ev.which == 13) {
    var n = document.getElementById('username').value
    var p = document.getElementById('pword').value
    post_login(n, p)
  }
})

function post_verify() {
  var xhr = new XMLHttpRequest()
  xhr.open('POST', '/verify')
  xhr.onreadystatechange = function() {
    if (xhr.readyState === XMLHttpRequest.DONE) {
      var t = JSON.parse(xhr.responseText)
      if (t.username) {
        login_name_elem.innerHTML = 'Welcome, ' + t.username
        login_name_elem.classList.remove('hidden')
      } else {
        login_form.classList.remove('hidden')
      }
    }
  }
  xhr.send(null)
}

function post_login(name, pword) {
  var data = {
    username: name,
    password: pword
  }
  var xhr = new XMLHttpRequest()
  xhr.open('POST', '/login')
  xhr.setRequestHeader('content-type', 'application/json')
  xhr.onreadystatechange = function() {
    if (xhr.readyState === XMLHttpRequest.DONE) {
      var t = JSON.parse(xhr.responseText)
      if (t.result == 'success') {
        login_form.classList.add('hidden')
        login_name_elem.innerHTML = 'Welcome, ' + name
        login_name_elem.classList.remove('hidden')
      } else {
        login_form.classList.remove('hidden')
        login_name_elem.classList.add('hidden')
      }
    }
  }
  xhr.send( JSON.stringify(data) )
}

post_verify()
