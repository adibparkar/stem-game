from django.contrib.auth.models import User
from models import Team, Player, Content
from random import choice
from datetime import datetime
from django.utils.timezone import utc


def seedTeams():
    teamNames = ['No Team', 'Winterfell', 'Casterly Rock', 'The Night\'s Watch']
    users = User.objects.all()
    for teamName in teamNames:
        randomUser = choice(users)
        Team.objects.create(name=teamName, owner=randomUser, adminApproved=True)


def seedPlayers():
    players = [
        {
            'username': 'Jon',
            'password': 'snow',
            'first_name': 'Jon',
            'last_name': 'Snow',
            'email': 'jon@snow.com',
            'playerID': '123456789',
            'team': 'The Night\'s Watch'
        },
        {
            'username': 'Ned',
            'password': 'stark',
            'first_name': 'Ned',
            'last_name': 'Stark',
            'email': 'ned@stark.com',
            'playerID': '123456789',
            'team': 'Winterfell'
        },
        {
            'username': 'Tywin',
            'password': 'lannister',
            'first_name': 'Tywin',
            'last_name': 'Lannister',
            'email': 'tywin@lannister.com',
            'playerID': '123456789',
            'team': 'Casterly Rock'
        },
        {
            'username': 'Tyrion',
            'password': 'lannister',
            'first_name': 'Tyrion',
            'last_name': 'Lannister',
            'email': 'tyrion@lannister.com',
            'playerID': '123456789',
            'team': 'Casterly Rock'
        },
        {
            'username': 'Cersei',
            'password': 'lannister',
            'first_name': 'Cersei',
            'last_name': 'Lannister',
            'email': 'cersei@lannister.com',
            'playerID': '123456789',
            'team': 'Casterly Rock'
        },
        {
            'username': 'Jaime',
            'password': 'lannister',
            'first_name': 'Jaime',
            'last_name': 'Lannister',
            'email': 'jaime@lannister.com',
            'playerID': '123456789',
            'team': 'Casterly Rock'
        },
        {
            'username': 'Joffrey',
            'password': 'baratheon',
            'first_name': 'Joffrey',
            'last_name': 'Baratheon',
            'email': 'joffrey@baratheon.com',
            'playerID': '123456789',
            'team': 'No Team'
        },
        {
            'username': 'Theon',
            'password': 'greyjoy',
            'first_name': 'Theon',
            'last_name': 'Greyjoy',
            'email': 'theon@greyjoy',
            'playerID': '123456789',
            'team': 'No Team'
        },
        {
            'username': 'Robb',
            'password': 'stark',
            'first_name': 'Robb',
            'last_name': 'Stark',
            'email': 'robb@stark.com',
            'playerID': '123456789',
            'team': 'Winterfell'
        },
        {
            'username': 'Arya',
            'password': 'stark',
            'first_name': 'Arya',
            'last_name': 'Stark',
            'email': 'arya@stark.com',
            'playerID': '123456789',
            'team': 'Winterfell'
        }
    ]
    for player in players:
        user = User.objects.create_user(username=player['username'], email=player['email'], password=player['password'])
        user.first_name = player['first_name']
        user.last_name = player['last_name']
        user.save()
        team = Team.objects.get(name=player['team'])
        Player.objects.create(playerID=player['playerID'], user=user, team=team)


def seedContent():
    points = [
        {
            'latitude':'34.02039',
            'longitude': '-118.28932',
            'regionName': 'Viterbi School of Engineering',
            'regionImageURL': 'http://upload.wikimedia.org/wikipedia/commons/thumb/0/0f/USC_Viterbi_School_Of_Engineering_Logo.jpg/220px-USC_Viterbi_School_Of_Engineering_Logo.jpg',
            'regionDescription': 'The Viterbi School of Engineering (formerly the USC School of Engineering) is located at the University of Southern California in the United States. It was renamed following a $52 million donation by Andrew Viterbi. The USC Viterbi School of Engineering celebrated its 100th birthday in conjunction with the universitys 125th birthday.'
        },
        {
            'latitude':'34.02050',
            'longitude': '-118.28540',
            'regionName': 'Tommy Trojan',
            'regionImageURL': 'http://upload.wikimedia.org/wikipedia/commons/thumb/f/f1/Trojan_shrine.jpg/300px-Trojan_shrine.jpg',
            'regionDescription': 'Tommy Trojan, officially known as the Trojan Shrine, is one of the most recognizable figures of school pride at the University of Southern California. The life-size bronze statue of a Trojan warrior sits in the center of campus and serves as a popular meeting spot, as well as a centerpiece for a number of campus events. It is the most popular unofficial mascot of the university.'
        },
        {
            'latitude':'34.01887',
            'longitude': '-118.28576',
            'regionName': 'USC Marshall School of Business',
            'regionImageURL': 'http://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/Msb.logoaaa_190346.jpg/120px-Msb.logoaaa_190346.jpg',
            'regionDescription': 'The USC Marshall School of Business is a private research and academic institution at the University of Southern California. It is the largest of USCs 17 professional schools. The current Dean is James G. Ellis. In 1997 the school was renamed following a US$35 million donation from alumnus Gordon S. Marshall.'
        },
        {
            'latitude':'34.01883',
            'longitude': '-118.28621',
            'regionName': 'George Tirebiter',
            'regionImageURL': '',
            'regionDescription': 'George Tirebiter was the unofficial mascot of the University of Southern California in the 1940s. When a stray dog was discovered by a group of USC students at Curries Ice Cream parlor, one student remarked that the dog looked like a Navy V-12 student named George Kuhns. Thus, the dog was dubbed "George." He received the surname "Tirebiter" because he would bite at the tires of cars he chased down Trousdale Parkway, which bisects the campus. (Today Trousdale is only open to foot traffic.) His pastime ultimately led to his demise, as he was eventually run over and killed by a car in 1950. A public funeral was held on campus. The original George Tirebiter was succeeded by a handful of subsequent Tirebiters until 1957.'
        },
        {
            'latitude':'34.01993',
            'longitude': '-118.28620',
            'regionName': 'Ronald Tutor Campus Center',
            'regionImageURL': 'https://encrypted-tbn3.gstatic.com/images?q=tbn:ANd9GcSaBPse4upEP2w5Jdcp578vHMkzopDe66yH_hFAaGA8stYkNG61jg',
            'regionDescription': 'Located in the heart of the campus, the Campus Center is used by virtually every current and prospective student, professor, staff member, family member, alumni, and visitor on campus.'
        },
        {
            'latitude':'34.02086',
            'longitude': '-118.28298',
            'regionName': 'McCarthy Quad',
            'regionImageURL': 'https://mw2.google.com/mw-panoramio/photos/small/2237536.jpg',
            'regionDescription': 'An expanse of pristine grass and deciduous trees, McCarthy Quad offers an attractive setting for resting, studying or socializing. Additionally, a variety of special events and concerts are held at the Quad. Located between Doheny Library and Leavey Library, McCarthy Quad and the reflecting pool that borders its north side were made possible by a gift from USC Trustee Kathleen Leavey McCarthy.'
        },
        {
            'latitude':'34.02188',
            'longitude': '-118.28312',
            'regionName': 'Leavey Library',
            'regionImageURL': 'http://cisoft.usc.edu/assets/007/63952.jpg',
            'regionDescription': 'The Thomas and Dorothy Leavey Library provides a state-of-the-art learning environment for students and faculty at the University of Southern California. Leaveys print and electronic collections, services, and technology are designed to facilitate coursework, studying, and research.'
        },
        {
            'latitude':'34.02259',
            'longitude': '-118.28085',
            'regionName': 'University Gateway',
            'regionImageURL': 'http://s3-media2.ak.yelpcdn.com/bphoto/Fvu2TXcCSN9siwrI5iHghg/l.jpg',
            'regionDescription': 'University Gateway was opened in 2010 as the largest student housing facility in the nation.  Holding 1,642 residents while offering easy access to Food, Banking, Groceries and Pharmacy needs; located mere steps from the USC campus University Gateway strives to deliver the highest level of luxury living to the USC community.'
        },
        {
            'latitude':'34.02355',
            'longitude': '-118.28650',
            'regionName': 'USC School of Cinematic Arts',
            'regionImageURL': 'http://upload.wikimedia.org/wikipedia/en/thumb/9/99/USC-SCA-logo.png/150px-USC-SCA-logo.png',
            'regionDescription': 'The USC School of Cinematic Arts (formerly the USC School of Cinema-Television, or CNTV) is a film school within the University of Southern California in Los Angeles, California. It is the oldest and largest such school in the United States, established in 1929 as a joint venture with the Academy of Motion Picture Arts and Sciences, and is widely recognized as one of the most prestigious film programs in the world.'
        },
        {
            'latitude':'34.02430',
            'longitude': '-118.28841',
            'regionName': 'Lyon Center',
            'regionImageURL': 'http://sait.usc.edu/Recsports/files/photos/facilities/055.jpg',
            'regionDescription': 'The Lyon Center features the Main Gym, 21,800 sq. ft. for basketball, badminton, volleyball; the Klug Family Fitness Center (weight room); an auxiliary gym (cardiovascular equipment); the Robinson Fitness Room (SCycling bikes); a stretching room; racquetball and squash courts; a climbing wall; ping pong tables; a group exercise studio; Jacuzzi; and a Pro Shop for equipment rentals and sales.'
        },
        {
            'latitude':'34.02095',
            'longitude': '-118.28544',
            'regionName': 'Bovard Auditorium',
            'regionImageURL': 'http://allanmccollum.net/amcimages/bovard_auditorium.jpg',
            'regionDescription': 'Bovard Auditorium has a rich and enduring history as a performance venue. The recent renovation of Bovard enhanced the audience experience by improving on the overall design of the space and theatrical systems upgrades. Celebrate Bovard with us and experience first hand world-class performers, improved acoustics, and comfort.'
        },
        {
            'latitude':'34.02204',
            'longitude': '-118.28816',
            'regionName': 'Cromwell Field',
            'regionImageURL': 'http://www.usc.edu/bus-affairs/ticketoffice/images/g_cromwell.jpg',
            'regionDescription': 'Used as a training and warm-up facility during the 1984 Olympic Games in Los Angeles, Cromwell Track & Field Stadium underwent a complete refurbishing in fall of 1983. Not only was the track resurfaced, but a new drainage system was also added. In the summer of 1991, the track was resurfaced again. A new Rekortan surface, the same one that was installed for the Olympic track and field competition at the Los Angeles Memorial Coliseum, has eight, 42-inch lanes. The high jump area is larger than before and there are two new sandpits for the horizontal jumps.'
        },
        {
            'latitude':'34.02224',
            'longitude': '-118.28453',
            'regionName': 'Mark Taper Hall of Humanities',
            'regionImageURL': '',
            'regionDescription': 'Taper Hall houses the EALC department.'
        },
        {
            'latitude':'34.02112',
            'longitude': '-118.28413',
            'regionName': 'Von Kleinsmid Center Library',
            'regionImageURL': '',
            'regionDescription': 'The Von KleinSmid Center Library for International and Public Affairs (VKC Library) is an interdisciplinary, graduate-level learning center that supports the current and anticipated research needs of students, faculty, staff, and alumni in political science, international relations, public administration, spatial science, public diplomacy, and urban and regional planning.'
        },
        {
            'latitude':'34.01940',
            'longitude': '-118.28912',
            'regionName': 'Seaver Science Library',
            'regionImageURL': '',
            'regionDescription': 'The Science & Engineering Library in the Seaver Science Center opened in January 1970. Before that time there were two separate libraries, one for science, which opened in the early 1920s, and one for engineering, which opened in 1942. In 2003, a Science & Engineering Library Planning Task Force, comprised of USC faculty and students in the sciences, was convened. That groups final report was completed in December 2003.'
        },
        {
            'latitude':'34.01911',
            'longitude': '-118.29026',
            'regionName': 'Parkside Apartments',
            'regionImageURL': 'http://inertiaengineers.com/wp-content/uploads/2011/03/USC-Parkside.jpg',
            'regionDescription': 'Part of the Parkside Residential Community, Parkside Apartments two six-story buildings offer a variety of choices to students of all class standings.Parkside has a lounge and residents have access to all the common facilities and cultural opportunities of the residential colleges.'
        },
        {
            'latitude':'34.01975',
            'longitude': '-118.29011',
            'regionName': 'Salvatori Computer Science Center',
            'regionImageURL': '',
            'regionDescription': 'The computing centers are open for student use and also contain classrooms that can be reserved for hands-on instruction. All computers run both Mac OSX and Windows 7.'
        },
        {
            'latitude':'34.01996',
            'longitude': '-118.28962',
            'regionName': 'Ronald Tutor Hall',
            'regionImageURL': '',
            'regionDescription': 'The USC Viterbi Schools Ronald Tutor Hall - a six-story, state-of-the-art instructional and research complex on the south side of the engineering quad.'
        },
        {
            'latitude':'34.02084',
            'longitude': '-118.28948',
            'regionName': 'Olin Hall of Engineering',
            'regionImageURL': 'http://www.bernards.com/wp-content/uploads/2012/09/bernards_usc_olin_hall_4_491-x-375-px.jpg',
            'regionDescription': 'DEN (Distance Education Classes) are held in this building at USC.'
        },
        {
            'latitude':'34.02103',
            'longitude': '-118.29010',
            'regionName': 'Parking Structure A',
            'regionImageURL': '',
            'regionDescription': 'This is the parking structure at USC which is closest to the Engineering section.'
        },
        {
            'latitude':'34.02395',
            'longitude': '-118.28851',
            'regionName': 'McDonalds Olympic Swim Stadium',
            'regionImageURL': 'http://upload.wikimedia.org/wikipedia/en/7/70/Uscswimstadium.jpg',
            'regionDescription': 'The McDonalds Swim Stadium is an outdoor aquatics venue located on the campus of the University of Southern California in Los Angeles, USA. The facility features two pools: a long course pool (50x25 meters), and a diving well (25x25 yards), which features, with towers. The facility is the home pool for the USC Trojans Swimming and Diving teams.'
        },
        {
            'latitude':'34.02071',
            'longitude': '-118.28646',
            'regionName': 'USC University Bookstore',
            'regionImageURL': 'https://lh4.googleusercontent.com/-ws70CBBfgkI/UB1w0UQxJiI/AAAAAAAAAI8/gPG3hsypTbc/s250-c-k/USC%2BUniversity%2BBookstore',
            'regionDescription': 'The USC Bookstores are a university owned and operated resource that provide students, faculty and staff members with a variety of products and services, including general books, textbooks, school supplies, spirit and fashion clothing, gift items, flowers, computer equipment and much more.'
        },
        {
            'latitude':'34.02507',
            'longitude': '-118.28562',
            'regionName': 'University Village',
            'regionImageURL': 'http://re.usc.edu/assets_c/2009/03/University%20Village%20002-thumb-220x165.jpg',
            'regionDescription': 'University Village is the shopping center directly adjacent to USCs University Park Campus. Vehicles and pedestrians can easily access the center by Hoover Street, Jefferson Boulevard, McClintock Avenue, or 30th Street. Its been operating in its current form for 20 years, and will be redeveloped starting in 2013.'
        },
        {
            'latitude':'34.02041',
            'longitude': '-118.28214',
            'regionName': 'Parking Structure X',
            'regionImageURL': '',
            'regionDescription': 'This USC Parking structure houses the offices of USCard and Housing services.'
        },
        {
            'latitude':'34.02012',
            'longitude': '-118.28351',
            'regionName': 'Edward L Doheny Memorial Library',
            'regionImageURL': 'http://www.usc.edu/libraries/locations/doheny/times_reference.jpg',
            'regionDescription': 'The historic Edward L. Doheny Jr. Memorial Library has served as an intellectual center and cultural treasure for generations of students, faculty and staff since it opened in 1932. Created as a memorial to Edward L. Doheny Jr., a USC trustee and alumnus, this landmark building was USCs first freestanding library. 75 years since its doors first opened, it remains one of the universitys most important and popular academic facilities.'
        },
        {
            'latitude':'34.02320',
            'longitude': '-118.29088',
            'regionName': 'Marks Tennis Stadium',
            'regionImageURL': '',
            'regionDescription': 'The David X. Marks Tennis Stadium on the USC campus is one of the intimate and historical collegiate tennis facilities in the country. During winter of 2006, a sixth court was added to the main stadium, allowing for dual-match competition to be played out entirely in front of fans within the 1,000-seat venue, which also boasts a large scoreboard to allow fans to follow each match point-for-point from their stadium seat and online.'
        },
        {
            'latitude':'34.02260',
            'longitude': '-118.28378',
            'regionName': 'JEP House',
            'regionImageURL': 'http://farm5.static.flickr.com/4120/4743914113_bbee7d33da.jpg',
            'regionDescription': 'Founded in 1972, the Joint Educational Project (JEP) is one of the oldest and largest service-learning programs in the United States. Each year over 2,000 USC students enroll in one of several JEP courses that combine academic coursework with hands-on experience in neighborhoods surrounding the university. Students may also participate as volunteers on a non-credit basis.'
        },
        {
            'latitude':'34.02034',
            'longitude': '-118.28892',
            'regionName': 'Archimedes Plaza',
            'regionImageURL': 'http://www.usc.edu/ext-relations/news_service/FilmJPEGS/147.jpg',
            'regionDescription': 'This plaza is found at the heart of the Viterbi School of Engineering at USC.'
        },
        {
            'latitude':'34.02506',
            'longitude': '-118.28795',
            'regionName': 'University Computing Center',
            'regionImageURL': '',
            'regionDescription': 'The USC Computing Center includes collaborative spaces for students, a classroom with 33 computers, 16 open computers, 30 loaner laptops, wireless printing, eco-friendly mobile furniture and a more interactive layout.'
        },
        {
            'latitude':'34.02463',
            'longitude': '-118.28778',
            'regionName': 'Webb Tower',
            'regionImageURL': 'http://scec.usc.edu/internships/useit/sites/scec.usc.edu.internships.useit/files/imagecache/large/images/470737720zNXEOn_ph.jpg',
            'regionDescription': 'Fully renovated in 2006, Webb Tower is the flagship of USC Housings upperclassmen apartments. Centrally located on campus with all the modern amenities, Webb Tower has 108 apartments and houses over 300 students. At 15 stories it boasts one of the best views of Los Angeles.'
        }
    ]
    players = Player.objects.all()
    for point in points:
        randomPlayer = choice(players)
        content = Content.objects.create(name=point['regionName'],
                                        photo=point['regionImageURL'],
                                        description=point['regionDescription'],
                                        latitude='%.6f' % float(point['latitude']),
                                        longitude='%.6f' % float(point['longitude']),
                                        creationTime=datetime.utcnow().replace(tzinfo=utc),
                                        player=randomPlayer)
        content.upVote(randomPlayer)


def seed():
    allContent = Content.objects.all()
    for content in allContent:
        content.delete()
    players = Player.objects.all()
    for player in players:
        player.user.delete()
        player.delete()
    teams = Team.objects.all()
    for team in teams:
        team.delete()
    seedTeams()
    seedPlayers()
    seedContent()