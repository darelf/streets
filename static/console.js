var con = document.getElementById('console')

function type_line(tlen, text, target, timing) {
  var txt = text.substr(0, tlen++)
  target.innerHTML = txt
  if (tlen < text.length + 1) {
    setTimeout(type_line.bind(null, tlen, text, target), timing)
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

