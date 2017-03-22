var con = document.getElementById('console')
var current_console_items = []
var queued_items = []
var is_typing = false

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
  con.classList.remove('hidden')
  if (redraw) {
    var exist_arr = current_console_items.slice(0,5)
    exist_msg = exist_arr.join('\n')
    full_msg = current_console_items.join('\n')
    con.innerHTML = exist_msg
  }
  type_line(exist_msg.length, full_msg, con, 100)
}

function close_console() {
  con.classList.add('hidden')
}

document.addEventListener('keyup', function(ev) {
  if (ev.keyCode == 27) close_console()
})

document.getElementById('main-content').addEventListener('click', close_console)

window.onload = function() {
  var p = 'ws://'
  if (location.protocol === 'https:') p = 'wss://'
  var ws = new WebSocket(p + location.host + '/pubsub')
  ws.onmessage = function(m) { queue_message(m.data) }
}
