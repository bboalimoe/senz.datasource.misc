import urllib2
import json
import base64

def query_baidu_coords(lng, lat, coord_system):
    # in Hong Kong:
    if coord_system == "hk":
        url = "http://api.map.baidu.com/ag/coord/convert?from=0&to=4&x=%.5f&y=%.6f" % (lng, lat)
    elif coord_system == "cn":
        url = "http://api.map.baidu.com/ag/coord/convert?from=2&to=4&x=%.5f&y=%.6f" % (lng, lat)
    response = urllib2.urlopen(url)
    line = response.read()
    json_obj = json.loads(line)
    baidu_x = (float)(base64.b64decode(json_obj["x"]))
    baidu_y = (float)(base64.b64decode(json_obj["y"]))
    return (baidu_x, baidu_y)

def linear_approximate(target_baidu_x, target_baidu_y, guess_lng, guess_lat, converted_baidu_x, converted_baidu_y, coord_system):
    #(converted_baidu_x, converted_baidu_y) = query_baidu_coords(guess_lng, guess_lat, coord_system)
    delta = 0.1
    (new_baidu_x, new_baidu_y) = query_baidu_coords(guess_lng + delta, guess_lat + delta, coord_system)
    d_lng = delta / (new_baidu_x - converted_baidu_x)
    d_lat = delta / (new_baidu_y - converted_baidu_y)
    new_guess_lng = guess_lng + d_lng * (target_baidu_x - converted_baidu_x)
    new_guess_lat = guess_lat + d_lat * (target_baidu_y - converted_baidu_y)
    return (new_guess_lng, new_guess_lat)

def iterative_approximate(target_baidu_x, target_baidu_y, coord_system):
    guess_lng = target_baidu_x
    guess_lat = target_baidu_y
    (converted_baidu_x, converted_baidu_y) = query_baidu_coords(guess_lng, guess_lat, coord_system)
    err = ((target_baidu_x - converted_baidu_x)**2 + (target_baidu_y - converted_baidu_y)**2)**(0.5)
    print "initial err = %f    https://maps.google.com/maps?q=%f,%f" % (err, guess_lat, guess_lng)
    for i in range(3):
        (new_guess_lng, new_guess_lat) = linear_approximate(target_baidu_x, target_baidu_y, guess_lng, guess_lat, converted_baidu_x, converted_baidu_y, coord_system)
        (converted_baidu_x, converted_baidu_y) = query_baidu_coords(new_guess_lng, new_guess_lat, coord_system)
        err = ((target_baidu_x - converted_baidu_x)**2 + (target_baidu_y - converted_baidu_y)**2)**(0.5)
        #err = ((new_guess_lng - guess_lng)**2 + (new_guess_lat - guess_lat)**2)**(0.5)
        print "iteration %d    err = %f    https://maps.google.com/maps?q=%f,%f" % (i, err, new_guess_lat, new_guess_lng)
        guess_lng = new_guess_lng
        guess_lat = new_guess_lat

def test_query_baidu_coords():
    (baidu_x, baidu_y) = query_baidu_coords(114.172959, 22.283654, "hk")

def test_linear_approximate():
    (new_guess_lng, new_guess_lat) = linear_approximate(114.184466, 22.286569, 114.184466, 22.286569, 114.184466, 22.286569, "hk")
    print "https://maps.google.com/maps?q=%f,%f" % (new_guess_lat, new_guess_lng)

def test_iterative_apprixmate():
    print "HKCEC (hk):"
    iterative_approximate(114.184466, 22.286569, "hk")
    print "Forbidden city (cn):"
    iterative_approximate(116.40364, 39.91972, "cn")

test_iterative_apprixmate()
