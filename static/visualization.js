var map;
var mapOverlays = [];
var colours = ['#E41A1C', '#377EB8', '#4DAF4A', '#984EA3', '#FF7F00', '#FFFF33', '#A65628', '#F781BF', '#999999'];
var currentPopup;
var epsilon = 1e-6;
var startLatitude = 34.01841;
var startLongitude = -118.29130;
var endLatitude = 34.02540;
var endLongitude = -118.28022;

/*
startLatitude = 34.01105;
startLongitude = -118.30010;
endLatitude = 34.03463;
endLongitude = -118.27201;
*/


function initialize()
{
    var mapOptions = {
        center: new google.maps.LatLng(34.02067, -118.285342),
        zoom: 16,
        scrollwheel: false,
        mapTypeId: google.maps.MapTypeId.ROADMAP };
    map = new google.maps.Map(document.getElementById('map_canvas'), mapOptions);
    dropMarkersOnMap();
}

function clearOverlays()
{
    if (currentPopup)
        currentPopup.close();
    for (var i = 0; i < mapOverlays.length; i++)
        mapOverlays[i].setMap(null);
    mapOverlays = [];
}

function convertToGrid(latLng)
{
    return [(latLng[0] - startLatitude) * 1e4, (latLng[1] - startLongitude) * 1e4];
}

function convertToLatLng(gridPoint)
{
    return[gridPoint[0] / 1e4 + startLatitude, gridPoint[1] / 1e4 + startLongitude];
}

function setPopupOnClick(point, popup)
{
    google.maps.event.addListener(point, 'click', function(e)
    {
        if (currentPopup)
            currentPopup.close();
        popup.setPosition(e.latLng);
        popup.open(map);
        currentPopup = popup;
    });
}

function dropMarkersOnMap()
{
    clearOverlays();
    var markerData = JSON.parse(jsonData);
    var weightedDataPoints = [];
    var dataPointOwners = [];
    var boundingRectangle = [convertToGrid([startLatitude, startLongitude]),
        convertToGrid([startLatitude, endLongitude]),
        convertToGrid([endLatitude, endLongitude]),
        convertToGrid([endLatitude, startLongitude])];
    for (var markerIndex = 0; markerIndex < markerData.length; markerIndex++)
    {
        var latitude = markerData[markerIndex]['latitude'];
        var longitude = markerData[markerIndex]['longitude'];
        var content = markerData[markerIndex]['content'];
        var regionContentID = markerData[markerIndex]['regionContentID'];
        var votes = markerData[markerIndex]['votes'];
        var voted = markerData[markerIndex]['voted'];
        var isModerator = markerData[markerIndex]['isModerator'];
        var currentOwner = markerData[markerIndex]['currentOwner'];
        var isVerified = markerData[markerIndex]['isVerified'];
        if (content && content != '')
        {
            dropMarkerOnMap(latitude, longitude, content, regionContentID, votes, voted, isModerator, currentOwner, isVerified);
            var gridPoint = convertToGrid([latitude, longitude]);
            if (votes > 0)
            {
                weightedDataPoints.push([gridPoint[0], gridPoint[1], votes]);
                dataPointOwners.push(markerData[markerIndex]['owner']);
            }
        }
    }
    drawVoronoiDiagram(weightedDataPoints, dataPointOwners, boundingRectangle);
}

function dropMarkerOnMap(latitude, longitude, content, regionContentID, votes, voted, isModerator, currentOwner, isVerified)
{
    if (!content || content == '')
        return;
    if (voted == 'False')
        content += ('<table><tr><td><a href="#" onclick="attemptAjaxUpdateForJSON(\'/upVoteContent?regionContentID=' + regionContentID.trim() + '&mode=' + mode + '\');">UPVOTE</a></td><td><a href="#" onclick="attemptAjaxUpdateForJSON(\'/downVoteContent?regionContentID=' + regionContentID.trim() + '&mode=' + mode + '\');">DOWNVOTE</a></td><td>' + votes + ' vote(s)</td></tr></table>');
    else
        content += ('<table><tr><td><a href="#" onclick="attemptAjaxUpdateForJSON(\'/undoVoteContent?regionContentID=' + regionContentID.trim() + '&mode=' + mode + '\');">UNDO VOTE</a></td><td>' + votes + ' vote(s)</td></tr></table>');
    if (isVerified == 'False')
    {
        if (isModerator == 'True')
            content += ('<table><tr><td><a href="#" onclick="attemptAjaxUpdateForJSON(\'/verifyContent?regionContentID=' + regionContentID.trim() + '&mode=' + mode + '\');">VERIFY</a></td><td><a href="#" onclick="attemptAjaxUpdateForJSON(\'/deleteContent?regionContentID=' + regionContentID.trim() + '&mode=' + mode + '\');">DELETE</a></td></tr></table>');
        else if (currentOwner == 'True')
            content += ('<table><tr><td><a href="#" onclick="attemptAjaxUpdateForJSON(\'/deleteContent?regionContentID=' + regionContentID.trim() + '&mode=' + mode + '\');">DELETE</a></td></tr></table>');
    }
    else
    {
        if (isModerator == 'True')
            content += ('<table><tr><td><a href="#" onclick="attemptAjaxUpdateForJSON(\'/deleteContent?regionContentID=' + regionContentID.trim() + '&mode=' + mode + '\');">DELETE</a></td></tr></table>');
    }
    var marker = new google.maps.Marker({
        map: map,
        position: new google.maps.LatLng(latitude, longitude)
    });
    mapOverlays.push(marker);
    var popup = new google.maps.InfoWindow({
        content: content
    });
    popup.setOptions({maxWidth: 300, maxHeight: 500});
    setPopupOnClick(marker, popup);
}


function drawVoronoiDiagram(weightedDataPoints, dataPointOwners, boundingRectangle)
{
    var ownerColourMap = {};
    var colourIndex = 0;
    var calculatedPolygonsAndOwners = getPolygonsForPoints(weightedDataPoints, boundingRectangle, dataPointOwners);
    var polygons = calculatedPolygonsAndOwners[0];
    var updatedOwners = calculatedPolygonsAndOwners[1];
    for (var i = 0; i < polygons.length; i++)
    {
        var polygonCoordinates = [];
        for (var j = 0; j < polygons[i].length; j++)
        {
            var latLng = convertToLatLng(polygons[i][j]);
            polygonCoordinates.push(new google.maps.LatLng(latLng[0], latLng[1]));
        }
        var colour = '#FFFFFF';
        var owner = updatedOwners[i];
        if (owner && owner != '')
        {
            if(!(owner in ownerColourMap))
            {
                ownerColourMap[owner] = colours[colourIndex];
                colourIndex++;
                colourIndex %= colours.length;
            }
            colour = ownerColourMap[owner];
        }
        var polygon = new google.maps.Polygon({
            paths: polygonCoordinates,
            strokeColor: '#000000',
            strokeOpacity: 0.65,
            strokeWeight: 1,
            fillColor: colour,
            fillOpacity: 0.35
        });
        polygon.setMap(map);
        mapOverlays.push(polygon);
        var content = 'This region is owned by ' + owner + '.';
        var popup = new google.maps.InfoWindow({
            content: content
        });
        popup.setOptions({maxWidth: 200, maxHeight: 50});
        setPopupOnClick(polygon, popup);
    }
}

function getIntersectionPoint(l1, l2)
{
    var a1 = l1[0], b1 = l1[1], c1 = l1[2];
    var a2 = l2[0], b2 = l2[1], c2 = l2[2];
    var m1 = NaN, m2 = NaN;
    if (b1 != 0) m1 = -a1 / b1;
    if (b2 != 0) m2 = -a2 / b2;
    var x = NaN, y = NaN;
    if (m1 == m2 || (isNaN(m1) && isNaN(m2))) return [x, y];
    if (b2 != 0)
        x = (c1 - (b1 / b2) * c2) / (a1 - (b1 / b2) * a2);
    else
        x = (c2 - (b2 / b1) * c1) / (a2 - (b2 / b1) * a1);
    if (a2 != 0)
        y = (c1 - (a1 / a2) * c2) / (b1 - (a1 / a2) * b2);
    else
        y = (c2 - (a2 / a1) * c1) / (b2 - (a2 / a1) * b1);
    return [x, y];
}

function getLineEquation(m, p)
{
    if (isNaN(m))
        return [1, 0, p[0]];
    return [-m, 1, -m * p[0] + p[1]];
}

function samePoint(p1, p2)
{
    if ((p1[0] == p2[0] && p1[1] == p2[1]) || (Math.abs(p1[0] - p2[0]) < epsilon && Math.abs(p1[1] - p2[1]) < epsilon))
        return true;
    return false;
}

function getSquaredDistance(p1, p2)
{
    if (isNaN(p1[0]) || isNaN(p1[1]) || isNaN(p2[0]) || isNaN(p2[1]))
        return NaN;
    return (p2[1] - p1[1]) * (p2[1] - p1[1]) + (p2[0] - p1[0]) * (p2[0] - p1[0]);
}

function addToSetOfPoints(set, newPoint)
{
    for (var i = 0; i < set.length; i++)
        if (samePoint(set[i], newPoint))
            return;
    set.push(newPoint);
}

function isPointInBounds(p, boundVertices)
{
    if (isNaN(p[0]) || isNaN(p[1]))
        return false;
    if (p[0] >= boundVertices[0][0] && p[0] <= boundVertices[2][0] && p[1] >= boundVertices[0][1] && p[1] <= boundVertices[2][1])
        return true;
    return false;
}

function arePointsOnSameSideOfLine(p1, p2, l)
{
    var r1 = l[0] * p1[0] + l[1] * p1[1] - l[2];
    var r2 = l[0] * p2[0] + l[1] * p2[1] - l[2];
    if ((r1 < 0 && r2 < 0) || (r1 > 0 && r2 > 0))
        return true;
    return false;
}

function getClippedPolygonFromEdges(boundVertices, polygonEdges, seedEdgeIndex, seedPoint, dataPoint)
{
    var vertices = [];
    var edges = [];
    for (var index = 0; index < polygonEdges.length; index++)
        edges.push(polygonEdges[index]);
    edges.push([0, 1, boundVertices[0][1]]);
    edges.push([1, 0, boundVertices[0][0]]);
    edges.push([0, 1, boundVertices[2][1]]);
    edges.push([1, 0, boundVertices[2][0]]);
    var previousEdgeIndex = null;
    if (seedEdgeIndex == null || seedPoint == null)
    {
        seedEdgeIndex = edges.length - 1;
        seedPoint = getIntersectionPoint(edges[edges.length - 1], edges[edges.length - 2]);
    }
    var currentEdgeIndex = seedEdgeIndex;
    var currentPoint = seedPoint;
    do
    {
        var closestDistance = null;
        var closestPoint = null;
        var nextEdgeIndex = null;
        for (var i = 0; i < edges.length; i++)
        {
            if (i == currentEdgeIndex || i == previousEdgeIndex)
                continue;
            var intersectionPoint = getIntersectionPoint(edges[currentEdgeIndex], edges[i]);
            if (!isPointInBounds(intersectionPoint, boundVertices))
                continue;
            if (previousEdgeIndex != null && !arePointsOnSameSideOfLine(dataPoint, intersectionPoint, edges[previousEdgeIndex]))
                continue;
            var distanceFromCurrentPoint = getSquaredDistance(currentPoint, intersectionPoint);
            if (closestDistance == null || distanceFromCurrentPoint < closestDistance)
            {
                closestDistance = distanceFromCurrentPoint;
                closestPoint = intersectionPoint;
                nextEdgeIndex = i;
            }
        }
        if (nextEdgeIndex == null)
            return [];
        addToSetOfPoints(vertices, closestPoint);
        previousEdgeIndex = currentEdgeIndex;
        currentEdgeIndex = nextEdgeIndex;
        currentPoint = closestPoint;
    }
    while(currentEdgeIndex != seedEdgeIndex);
    return vertices;
}

function weightFunction(value)
{
    return 10 * value;
}

function getEdgePoint(p1, p2)
{
    var multiplier = (p2[0] * p2[0] + p2[1] * p2[1]) - (p1[0] * p1[0] + p1[1] * p1[1]) + weightFunction(p1[2]) - weightFunction(p2[2]);
    var divisor = 2 * ((p2[0] - p1[0]) * (p2[0] - p1[0]) + (p2[1] - p1[1]) * (p2[1] - p1[1]));
    var p3 = new Array(2);
    p3[0] = multiplier / divisor * (p2[0] - p1[0]);
    p3[1] = multiplier / divisor * (p2[1] - p1[1]);
    var dx = p2[0] - p1[0];
    var dy = p2[1] - p1[1];
    var perpendicular = getLineEquation(-dx / dy, p3);
    var line = getLineEquation(dy / dx, p1);
    return getIntersectionPoint(perpendicular, line);
}

function isDominated(p1, p2)
{
    var p3 = getEdgePoint(p1, p2);
    var distanceP1P2 = getSquaredDistance(p1, p2);
    var distanceP1P3 = getSquaredDistance(p1, p3);
    var distanceP2P3 = getSquaredDistance(p2, p3);
    if (distanceP2P3 >= distanceP1P2 && distanceP1P3 < distanceP2P3)
        return true;
    return false;
}

function getEdgeEquation(p1, p2, p3)
{
    var dx = p2[0] - p1[0];
    var dy = p2[1] - p1[1];
    return getLineEquation(-dx / dy, p3);
}

function getPolygonsForPoints(weightedDataPoints, boundingRectangle, dataPointOwners)
{
    var dominated = new Array(weightedDataPoints.length);
    for (var a = 0; a < dominated.length; dominated[a++] = false);
    for (var p = 0; p < weightedDataPoints.length; p++)
        for (var q = 0; q < weightedDataPoints.length; q++)
        {
            if (p == q)
                continue;
            if (isDominated(weightedDataPoints[p], weightedDataPoints[q]))
            {
                dominated[p] = true;
                break;
            }
        }
    var dataPoints = [];
    var updatedOwners = [];
    for (var b = 0; b < weightedDataPoints.length; b++)
        if (!dominated[b])
        {
            dataPoints.push(weightedDataPoints[b]);
            updatedOwners.push(dataPointOwners[b])
        }
    var polygons = [];
    for (var i = 0; i < dataPoints.length; i++)
    {
        var edges = [];
        var seedPoint = null;
        var seedEdgeIndex = null;
        var closestDistance = null;
        var edgeIndex = 0;
        for (var j = 0; j < dataPoints.length; j++)
        {
            if (i == j)
                continue;
            var point = getEdgePoint(dataPoints[i], dataPoints[j]);
            var distance = getSquaredDistance(dataPoints[i], point);
            edges.push(getEdgeEquation(dataPoints[i], dataPoints[j], point));
            if (closestDistance == null || distance < closestDistance)
            {
                seedPoint = point;
                closestDistance = distance;
                seedEdgeIndex = edgeIndex;
            }
            edgeIndex++;
        }
        var vertices = getClippedPolygonFromEdges(boundingRectangle, edges, seedEdgeIndex, seedPoint, dataPoints[i]);
        polygons.push(vertices);
    }
    return [polygons, updatedOwners];
}

function attemptAjaxUpdateForJSON(updateURL)
{
    if (window.XMLHttpRequest)
    {
        ajaxRequest = new XMLHttpRequest();
        ajaxRequest.open('GET', updateURL, true);
        ajaxRequest.onreadystatechange = function(){
            if (ajaxRequest.readyState == 4 && ajaxRequest.status == 200)
            {
                jsonData = ajaxRequest.responseText;
                dropMarkersOnMap();
            }
        };
        ajaxRequest.send();
    }
    else
    {
        document.location.href = updateURL + '&noAjax=true';
    }
}

function getAreaOfTriangle(vertexA, vertexB, vertexC)
{
    return Math.abs((vertexA[0] * (vertexB[1] - vertexC[1]) + vertexB[0] * (vertexC[1] - vertexA[1]) + vertexC[0] * (vertexA[1] - vertexB[1])) / 2.0);
}

function getAreaOfPolygon(coordinates)
{
    if (coordinates.length < 3)
        return 0.0;
    var area = 0.0;
    for (var i = 1; i < coordinates.length - 1; i++)
        area += getAreaOfTriangle(coordinates[0], coordinates[i], coordinates[i + 1]);
    return area;
}

function getIndexForValue(array, value)
{
    for (var i = 0; i < array.length; i++)
        if (array[i] == value)
            return i;
    return -1;
}

function generateLeaderboard()
{
    var markerData = JSON.parse(jsonData);
    var weightedDataPoints = [];
    var dataPointOwners = [];
    var boundingRectangle = [convertToGrid([startLatitude, startLongitude]),
        convertToGrid([startLatitude, endLongitude]),
        convertToGrid([endLatitude, endLongitude]),
        convertToGrid([endLatitude, startLongitude])];
    for (var markerIndex = 0; markerIndex < markerData.length; markerIndex++)
    {
        var latitude = markerData[markerIndex]['latitude'];
        var longitude = markerData[markerIndex]['longitude'];
        var content = markerData[markerIndex]['content'];
        var regionContentID = markerData[markerIndex]['regionContentID'];
        var votes = markerData[markerIndex]['votes'];
        var voted = markerData[markerIndex]['voted'];
        var isModerator = markerData[markerIndex]['isModerator'];
        var currentOwner = markerData[markerIndex]['currentOwner'];
        var isVerified = markerData[markerIndex]['isVerified'];
        if (content && content != '')
        {
            var gridPoint = convertToGrid([latitude, longitude]);
            if (votes > 0)
            {
                weightedDataPoints.push([gridPoint[0], gridPoint[1], votes]);
                dataPointOwners.push(markerData[markerIndex]['owner']);
            }
        }
    }
    var calculatedPolygonsAndOwners = getPolygonsForPoints(weightedDataPoints, boundingRectangle, dataPointOwners);
    var polygons = calculatedPolygonsAndOwners[0];
    var updatedOwners = calculatedPolygonsAndOwners[1];
    var uniqueOwners = [];
    for (var i = 0; i < dataPointOwners.length; i++)
        if (getIndexForValue(uniqueOwners, dataPointOwners[i]) == -1)
            uniqueOwners.push(dataPointOwners[i]);
    var votesForPlayer = [];
    for (var i = 0; i < uniqueOwners.length; i++)
        votesForPlayer.push(0);
    var areaForPlayer = [];
    for (var i = 0; i < uniqueOwners.length; i++)
        areaForPlayer.push(0);
    for (var i = 0; i < weightedDataPoints.length; i++)
        votesForPlayer[getIndexForValue(uniqueOwners, dataPointOwners[i])] += weightedDataPoints[i][2];
    for (var i = 0; i < polygons.length; i++)
        areaForPlayer[getIndexForValue(uniqueOwners, updatedOwners[i])] += getAreaOfPolygon(polygons[i]);
    for (var i = 0; i < uniqueOwners.length - 1; i++)
        for (var j = i + 1; j < uniqueOwners.length; j++)
            if (votesForPlayer[i] < votesForPlayer[j])
            {
                var temp = votesForPlayer[i];
                votesForPlayer[i] = votesForPlayer[j];
                votesForPlayer[j] = temp;
                temp = uniqueOwners[i];
                uniqueOwners[i] = uniqueOwners[j];
                uniqueOwners[j] = temp;
                temp = areaForPlayer[i];
                areaForPlayer[i] = areaForPlayer[j];
                areaForPlayer[j] = temp;
            }
    var limit = uniqueOwners.length < 10 ? uniqueOwners.length : 10;
    var html = '';
    for (var i = 0; i < limit; i++)
        html += ('<tr><td>' + uniqueOwners[i] + '</td><td>' + votesForPlayer[i] + '</td></tr>\n');
    document.getElementById('voteTable').innerHTML = html;
    for (var i = 0; i < uniqueOwners.length - 1; i++)
        for (var j = i + 1; j < uniqueOwners.length; j++)
            if (areaForPlayer[i] < areaForPlayer[j])
            {
                var temp = votesForPlayer[i];
                votesForPlayer[i] = votesForPlayer[j];
                votesForPlayer[j] = temp;
                temp = uniqueOwners[i];
                uniqueOwners[i] = uniqueOwners[j];
                uniqueOwners[j] = temp;
                temp = areaForPlayer[i];
                areaForPlayer[i] = areaForPlayer[j];
                areaForPlayer[j] = temp;
            }
    html = '';
    for (var i = 0; i < limit; i++)
        html += ('<tr><td>' + uniqueOwners[i] + '</td><td>' + areaForPlayer[i].toFixed(2) + '</td></tr>\n');
    document.getElementById('areaTable').innerHTML = html;
}