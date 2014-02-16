pixels = []

w = new WebSocket('ws://localhost:8000/mosaic/')

width, height = 491,491

getX = (d) -> "#{JSON.parse(d.url).x}px"

getY = (d) -> "#{JSON.parse(d.url).y}px"

getImage = (d) ->
  JSON.parse(d.url).url.replace(/_8\.jpg/g, '_5.jpg')

d3.select('body').append('div')

w.onopen = (e) ->
  w.send('start')

w.onmessage = (e) ->
  message = JSON.parse(e.data)
  pixels.push message

  data = d3.select('body > div').selectAll('img').data(pixels)
  data.enter().append('img').attr('src', getImage)
    .style('position', 'absolute').style('top', getY, 'important').style('left', getX, 'important')
  data.exit().remove()

window.onUnload = (e) ->
  w.close()
