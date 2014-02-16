w = new WebSocket('ws://localhost:8000:/echo')
w.onmessage = function(e) {
  console.log(e);
}
w.send(task_id);