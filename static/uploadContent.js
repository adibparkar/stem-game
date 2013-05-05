var map, locationMarker;

function initialize()
{
    var mapOptions = {
        center: new google.maps.LatLng(34.02067, -118.285342),
        zoom: 20,
        minZoom: 20,
        maxZoom: 20,
        scrollwheel: false,
        draggable: false,
        mapTypeId: google.maps.MapTypeId.ROADMAP };
    map = new google.maps.Map(document.getElementById('map_canvas'), mapOptions);
    google.maps.event.addListener(map, "click", function(event) {
        var latitude = event.latLng.lat();
        var longitude = event.latLng.lng();
        document.getElementById('latitude').value = latitude;
        document.getElementById('longitude').value = longitude;
        document.getElementById('locationCell').innerHTML = latitude + ', ' + longitude;
        map.panTo(new google.maps.LatLng(latitude, longitude));
        if (locationMarker)
            locationMarker.setPosition(new google.maps.LatLng(latitude, longitude));
        else
        {
            locationMarker = new google.maps.Marker({
                map: map,
                animation: google.maps.Animation.DROP,
                position: new google.maps.LatLng(latitude, longitude)
            });
        }
    });
    var latitude = document.getElementById('latitude').value;
    var longitude = document.getElementById('longitude').value;
    if (latitude && longitude)
    {
        document.getElementById('locationCell').innerHTML = latitude + ', ' + longitude;
        if (locationMarker)
            locationMarker.setPosition(new google.maps.LatLng(latitude, longitude));
        else
        {
            map.panTo(new google.maps.LatLng(latitude, longitude));
            locationMarker = new google.maps.Marker({
                map: map,
                animation: google.maps.Animation.DROP,
                position: new google.maps.LatLng(latitude, longitude)
            });
        }
    }
    else if (navigator.geolocation)
    {
        navigator.geolocation.getCurrentPosition(function(position){
            var latitude = position.coords.latitude;
            var longitude = position.coords.longitude;
            document.getElementById('latitude').value = latitude;
            document.getElementById('longitude').value = longitude;
            document.getElementById('locationCell').innerHTML = latitude + ', ' + longitude;
            map.panTo(new google.maps.LatLng(latitude, longitude));
            if (locationMarker)
                locationMarker.setPosition(new google.maps.LatLng(latitude, longitude));
            else
            {
                locationMarker = new google.maps.Marker({
                    map: map,
                    animation: google.maps.Animation.DROP,
                    position: new google.maps.LatLng(latitude, longitude)
                });
            }
        });
    }
    if (navigator.geolocation)
        document.getElementById('myLocation').style.visibility = 'visible';
}

function gotoCurrentLocation()
{
    navigator.geolocation.getCurrentPosition(function(position){
        var latitude = position.coords.latitude;
        var longitude = position.coords.longitude;
        document.getElementById('latitude').value = latitude;
        document.getElementById('longitude').value = longitude;
        document.getElementById('locationCell').innerHTML = latitude + ', ' + longitude;
        map.panTo(new google.maps.LatLng(latitude, longitude));
        if (locationMarker)
            locationMarker.setPosition(new google.maps.LatLng(latitude, longitude));
        else
        {
            locationMarker = new google.maps.Marker({
                map: map,
                animation: google.maps.Animation.DROP,
                position: new google.maps.LatLng(latitude, longitude)
            });
        }
    });
}