var con = document.getElementById('console')
var console_is_open = false
var current_console_items = []
var queued_items = []
var is_typing = false
var ws = null

function type_line(tlen, text, target, timing) {
  var txt = text.substr(0, tlen++)
  target.innerHTML = txt
  if (tlen < text.length + 1) {
    setTimeout(type_line.bind(null, tlen, text, target), timing)
  } else {
    if (queued_items.length > 0) {
      is_typing = true
      show_message(queued_items.shift())
    } else {
      is_typing = false
    }
  }
}

function queue_message(msg) {
  if (!is_typing) {
    is_typing = true
    show_message(msg)
  } else {
    queued_items.push(msg)
  }
}

function show_message(msg) {
  var len = current_console_items.push(msg)
  var exist_msg = con.innerHTML
  var full_msg = exist_msg + msg + '\n'
  var redraw = false
  if (len > 6) {
    current_console_items.shift()
    redraw = true
  }
  open_console()
  if (redraw) {
    var exist_arr = current_console_items.slice(0,5)
    exist_msg = exist_arr.join('\n')
    full_msg = current_console_items.join('\n')
    con.innerHTML = exist_msg
  }
  type_line(exist_msg.length, full_msg, con, 100)
}

function send_message(msg) {
  ws.send(msg)
}

function close_console() {
  con.classList.add('hidden')
  console_is_open = false
}

function open_console() {
  con.classList.remove('hidden')
  console_is_open = true
}

document.addEventListener('keyup', function(ev) {
  if (ev.keyCode == 27) {
    if (con.classList.contains('hidden')) {
       open_console()
    } else {
      close_console()
    }
  }
})

document.getElementById('main-content').addEventListener('click', close_console)

window.onload = function() {
  var first = sessionStorage.first_message
  if (!first) {
    queue_message('Welcome to StreetNode.  Press ESC to toggle this console.')
    sessionStorage.first_message = "true"
  }
  var p = 'ws://'
  if (location.protocol === 'https:') p = 'wss://'
  ws = new WebSocket(p + location.host + '/pubsub')
  ws.onmessage = function(m) { queue_message(m.data) }
}
