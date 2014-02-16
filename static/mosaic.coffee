pixels = []

w = new WebSocket('ws://localhost:8000/mosaic/')

d3.select("body").append("div")

w.onopen = (e) ->
  w.send("start")

w.onmessage = (e) ->

  message = JSON.parse(e.data)
  pixels.push message

  data = d3.select('body > div').selectAll("img").data(pixels)
  data.enter().append("img").attr("src", (d) -> d.url).style('border-style', 'dotted')
  data.exit().remove()

window.onUnload = (e) ->
  w.close()
