pixels = []

w = new WebSocket('ws://localhost:8000/mosaic/')

[width, height] = [1920,1080]
RESOLUTION = 30

getX = (d) -> JSON.parse(d.url).x

getY = (d) -> JSON.parse(d.url).y

getImage = (d) ->
  JSON.parse(d.url).url.replace(/_8\.jpg/g, '_5.jpg')

svg = d3.select('body').append('svg').attr('width', width).attr('height', height)

w.onopen = (e) ->
  w.send('start')

w.onmessage = (e) ->
  message = JSON.parse(e.data)
  pixels.push message

  images = svg.selectAll('image').data(pixels)
  images.enter().append('svg:image').attr
    'xlink:href': getImage
    x:      (d) -> (getX(d) + RESOLUTION) / 2
    y:      (d) -> (getY(d) + RESOLUTION) / 2
    width:  0
    height: 0
  .transition().attr
    x:      getX
    y:      getY
    width:  RESOLUTION
    height: RESOLUTION

  images.exit().remove()

window.onUnload = (e) ->
  w.close()
