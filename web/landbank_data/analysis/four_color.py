from models import CommunityArea, Ward, Municipality, CensusTract
import collections
import pprint
import operator

# Compares geometries and greedily determines a map-coloring reuslting in non-
# adjacent colors for adjacent areas. Inspired by the 'four-color theorem'
# and the Welsh-Poewll algorithm from graphy theory and described here: 
# http://en.wikipedia.org/wiki/Graph_coloring#Greedy_coloring
# The "color_id" field was used as conditional styling for TileMill maps.

# Define all geographical models to be used
all_geographies = [{
  'name':'communityarea'
  ,'queryset':CommunityArea.objects.all()
  ,'geom_field_name':'geom'
  },{ 
  'name':'ward'
  ,'queryset':Ward.objects.all()
  ,'geom_field_name':'geom'
  },{ 
  'name':'municipality'
  ,'queryset':Municipality.objects.all()
  ,'geom_field_name':'geom'
  },{ 
  'name':'censustract'
  ,'queryset':CensusTract.objects.all()
  ,'geom_field_name':'loc'
  }]

# Determine coloring of all geometries in each of the above models
for geography in all_geographies:
  area_degrees = {}
  area_neighbors = {}
  area_colors = {}
  max_color = 1
  area_queryset = geography['queryset']
  for a in area_queryset:
    area_degrees[a.id] = 0
    area_neighbors[a.id] = []
    area_colors[a.id] = None
    params = {geography['geom_field_name'] + '__intersects': getattr(a, geography['geom_field_name'])}
    neighbors = area_queryset.filter(**params).values('id')
    for n in neighbors:
      if n['id'] != a.id:
        area_degrees[a.id] += 1
        area_neighbors[a.id].append(n['id'])
  # sort areas in increasing order of number of neighbors
  sorted_by_deg = collections.deque(sorted(area_degrees.iteritems(), key=operator.itemgetter(1)))
  # use least-at-the-end heuristic for four color greedy algorithm
  sorted_by_deg.rotate(-1)
  # try to color each area
  for sbd in sorted_by_deg:
    area_id = sbd[0]
    print str(sbd[0]) + ", " + str(sbd[1]) + ":"
    # neighbors' colors?
    neighbor_colors = []
    for neighbor in area_neighbors[area_id]:
      neighbor_colors.append(area_colors[neighbor])
    print "  neighbors have colors: " + str(neighbor_colors)
    # try a color
    for color in range(1,max_color+1):
      print "  trying color " + str(color)
      if color not in neighbor_colors:
        area_colors[area_id] = color
        break
    if area_colors[area_id] == None:
      max_color += 1
      area_colors[area_id] = max_color
      print "    had to add color " + str(max_color)

  # Save results
  for a in area_queryset:
    a.color_id = area_colors[a.id]
    a.save()
