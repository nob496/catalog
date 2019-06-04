from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Hiking, TrailInfo, User

engine = create_engine('sqlite:///hikingtrailinfo.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# Create dummy user
User1 = User(name="Noboru Ooike", email="noboru.ooike@icloud.com",
             picture='https://en.wikipedia.org/wiki/Intel#/media/File:Intel-logo.svg')
session.add(User1)
session.commit()


park1 = Hiking(user_id=1, park="Big Basin Readwoods State Park")
session.add(park1)
session.commit()

trailInfo1 = TrailInfo(user_id=1,
                       trail="Skyline to the Sea, Berry Creak Falls, Hammond Read Road Loop",
                       date="2017.12.02", 
                       url="https://www.alltrails.com/trail/us/california/skyline-to-the-sea-berry-creek-falls-hammond-road-loop",
                       address="21600 Big Basin Way, Boulder Creek, CA 95006", 
                       distance="10.5 miles",
                       elevation="2785 feet",
                       level="HARD",
                       hiking=park1)
session.add(trailInfo1)
session.commit()

trailInfo2 = TrailInfo(user_id=1,
                       trail="Sequoia Trail",
                       date="-", 
                       url="https://www.alltrails.com/trail/us/california/sequoia-trail",
                       address="21600 Big Basin Way, Boulder Creek, CA 95006", 
                       distance="4.3 miles",
                       elevation="603 feet",
                       level="MODERATE",
                       hiking=park1)
session.add(trailInfo2)
session.commit()

trailInfo3 = TrailInfo(user_id=1,
                       trail="Skyline to the Sea and Meteor Trail Loop",
                       date="-", 
                       url="https://www.alltrails.com/trail/us/california/meteor-loop-trail",
                       address="21600 Big Basin Hwy, Boulder Creek, CA 95006", 
                       distance="4.7 miles",
                       elevation="879 feet",
                       level="MODERATE",
                       hiking=park1)
session.add(trailInfo3)
session.commit()

park2 = Hiking(user_id=1, park="Mission Peak Regional Preserve")
session.add(park2)
session.commit()

trailInfo1 = TrailInfo(user_id=1,
                       trail="Mission Peak from Ohlone College",
                       date="2017.12.16", 
                       url="https://www.alltrails.com/trail/us/california/mission-peak-from-ohlone-college",
                       address="Trail parking, 43628, 43660 Mission Blvd, Fremont, CA 94539", 
                       distance="7.3 miles",
                       elevation="2145 feet",
                       level="HARD",
                       hiking=park2)
session.add(trailInfo1)
session.commit()

trailInfo2 = TrailInfo(user_id=1,
                       trail="Mission Peak Loop from Stanford Avenue Staging Area",
                       date="-", 
                       url="https://www.alltrails.com/trail/us/california/mission-peak-loop-from-stanford-avenue-staging-area",
                       address="1880 Stanford Ave, Fremont, CA 94539", 
                       distance="5.8 miles",
                       elevation="2135 feet",
                       level="HARD",
                       hiking=park2)
session.add(trailInfo2)
session.commit()

park3 = Hiking(user_id=1, park="Castle Rock State Park")
session.add(park3)
session.commit()

trailInfo1 = TrailInfo(user_id=1,
                       trail="Castle Rock Trail to Saratoga Gap Trail and Ridge Trail Loop",
                       date="2018.01.28", 
                       url="https://www.alltrails.com/trail/us/california/saratoga-gap-trail-and-ridge-trail-loop",
                       address="15000 Skyline Blvd, Los Gatos, CA 95033", 
                       distance="5.5 miles",
                       elevation="1213 feet",
                       level="MODERATE",
                       hiking=park3)
session.add(trailInfo1)
session.commit()

trailInfo2 = TrailInfo(user_id=1,
                       trail="Ridge Trail to Goat Rock Overlook, Emily Smith Observation Point, and Saratoga Gap Trail",
                       date="-", 
                       url="https://www.alltrails.com/trail/us/california/ridge-trail-to-goat-rick-overlook-emily-smith-observation-point-and-saratoga-gap-trail",
                       address="Saratoga Gap Trail, Los Gatos, CA 95033", 
                       distance="3.7 miles",
                       elevation="816 feet",
                       level="MODERATE",
                       hiking=park3)
session.add(trailInfo2)
session.commit()

park4 = Hiking(user_id=1, park="Windy Hill Open Space Preserve")
session.add(park4)
session.commit()

trailInfo1 = TrailInfo(user_id=1,
                       trail="Hamms Gulch to Spring Ridge Trail Loop",
                       date="2018.03.04", 
                       url="https://www.alltrails.com/trail/us/california/hamms-gulch-to-spring-ridge-trail-loop",
                       address="555 Portola Rd, Portola Valley, CA 94028", 
                       distance="6.8 miles",
                       elevation="1443 feet",
                       level="MODERATE",
                       hiking=park4)
session.add(trailInfo1)
session.commit()

trailInfo2 = TrailInfo(user_id=1,
                       trail="Windy Hill Loop",
                       date="-", 
                       url="https://www.alltrails.com/trail/us/california/windy-hill-loop",
                       address="4860 Alpine Rd, Portola Valley, CA 94028", 
                       distance="5.5 miles",
                       elevation="1371 feet",
                       level="HARD",
                       hiking=park4)
session.add(trailInfo2)
session.commit()

park5 = Hiking(user_id=1, park="Point Reyes National Seashore")
session.add(park5)
session.commit()

trailInfo1 = TrailInfo(user_id=1,
                       trail="Alamere Falls via Coast Trail from Palomarin Trail head",
                       date="2018.04.14", 
                       url="https://www.alltrails.com/trail/us/california/alamere-falls-via-coast-trail-from-palomarin-trailhead",
                       address="Mesa Rd, Bolinas, CA 94924", 
                       distance="8.8 miles",
                       elevation="1335 feet",
                       level="MODERATE",
                       hiking=park5)
session.add(trailInfo1)
session.commit()

trailInfo2 = TrailInfo(user_id=1,
                       trail="Tomales Point Trail",
                       date="2018.10.14", 
                       url="https://www.alltrails.com/trail/us/california/tomales-point-trail",
                       address="Tomales Point Trail, Inverness, CA 94937", 
                       distance="9.4 miles",
                       elevation="1177 feet",
                       level="MODERATE",
                       hiking=park5)
session.add(trailInfo2)
session.commit()

park6 = Hiking(user_id=1, park="Alum Rock State Park")
session.add(park6)
session.commit()

trailInfo1 = TrailInfo(user_id=1,
                       trail="Alum Rock South Rim Trail",
                       date="2018.04.29", 
                       url="https://www.alltrails.com/trail/us/california/alum-rock-south-rim-trail",
                       address="15288-15294 Alum Rock Falls Rd, San Jose, CA 95132", 
                       distance="4.3 miles",
                       elevation="770 feet",
                       level="MODERATE",
                       hiking=park6)
session.add(trailInfo1)
session.commit()

trailInfo2 = TrailInfo(user_id=1,
                       trail="Penitencia Creek Trail",
                       date="-", 
                       url="https://www.alltrails.com/trail/us/california/penitencia-creek-trail",
                       address="16260 Penitencia Creek Rd, San Jose, CA 95127", 
                       distance="3.5 miles",
                       elevation="262 feet",
                       level="EASY",
                       hiking=park6)
session.add(trailInfo2)
session.commit()

park7 = Hiking(user_id=1, park="Purisima Creek Redwoods Open Space Preserve")
session.add(park7)
session.commit()

trailInfo1 = TrailInfo(user_id=1,
                       trail="North Ridge Trail",
                       date="2018.05.27", 
                       url="https://www.alltrails.com/trail/us/california/north-ridge-trail--2",
                       address="13130 Skyline Blvd, Redwood City, CA 94062", 
                       distance="4.3 miles",
                       elevation="1230 feet",
                       level="MODERATE",
                       hiking=park7)
session.add(trailInfo1)
session.commit()

trailInfo2 = TrailInfo(user_id=1,
                       trail="Whittemore Gulch and Purisima Creek Loop Trail",
                       date="-", 
                       url="https://www.alltrails.com/trail/us/california/whittemore-gulch-and-purisima-creek-loop-trail",
                       address="13184 Skyline Blvd, Redwood City, CA 94062", 
                       distance="9.3 miles",
                       elevation="2109 feet",
                       level="MODERATE",
                       hiking=park7)
session.add(trailInfo2)
session.commit()

park8 = Hiking(user_id=1, park="Mount Diablo State Park")
session.add(park8)
session.commit()

trailInfo1 = TrailInfo(user_id=1,
                       trail="Waterfalls of Mount Diablo Loop Trail",
                       date="2018.07.01", 
                       url="https://www.alltrails.com/trail/us/california/waterfalls-of-mount-diablo-loop-trail",
                       address="96 Mitchell Canyon Rd, Clayton, CA 94517", 
                       distance="7.9 miles",
                       elevation="1709 feet",
                       level="HARD",
                       hiking=park8)
session.add(trailInfo1)
session.commit()

park9 = Hiking(user_id=1, park="Point Lobos State Natural Reserve")
session.add(park9)
session.commit()

trailInfo1 = TrailInfo(user_id=1,
                       trail="Point Lobos Loop Trail",
                       date="2018.07.22", 
                       url="https://www.alltrails.com/trail/us/california/point-lobos-loop-trail",
                       address="62 CA-1, Carmel-By-The-Sea, CA 93923", 
                       distance="6.7 miles",
                       elevation="741 feet",
                       level="EASY",
                       hiking=park9)
session.add(trailInfo1)
session.commit()

trailInfo2 = TrailInfo(user_id=1,
                       trail="Cypress Grove Trail",
                       date="-", 
                       url="https://www.alltrails.com/trail/us/california/cypress-grove-trail",
                       address="62 CA-1, Carmel-By-The-Sea, CA 93923", 
                       distance="0.8 miles",
                       elevation="59 feet",
                       level="EASY",
                       hiking=park9)
session.add(trailInfo2)
session.commit()

park10 = Hiking(user_id=1, park="Sanborn County Park")
session.add(park10)
session.commit()

trailInfo1 = TrailInfo(user_id=1,
                       trail="Sanborn Trails",
                       date="2018.09.03", 
                       url="https://www.alltrails.com/trail/us/california/sanborn-trails",
                       address="San Andreas Trail, Saratoga, CA 95070", 
                       distance="4.5 miles",
                       elevation="1541 feet",
                       level="MODERATE",
                       hiking=park10)
session.add(trailInfo1)
session.commit()

trailInfo2 = TrailInfo(user_id=1,
                       trail="Summit Rock Loop Trail",
                       date="-", 
                       url="https://www.alltrails.com/trail/us/california/skyline-summit-rock-loop-bonjetti-creek-loop-trail",
                       address="15000 Skyline Blvd, Los Gatos, CA 95033", 
                       distance="2.4 miles",
                       elevation="580 feet",
                       level="MODERATE",
                       hiking=park10)
session.add(trailInfo2)
session.commit()

park11 = Hiking(user_id=1, park="Henry Cowell Redwoods State Park")
session.add(park11)
session.commit()

trailInfo1 = TrailInfo(user_id=1,
                       trail="Fall Creek to Lime Kilns Trail",
                       date="2018.09.08", 
                       url="https://www.alltrails.com/trail/us/california/fall-creek-to-lime-kilns-trail",
                       address="824 Ley Rd, Felton, CA 95018", 
                       distance="4.8 miles",
                       elevation="744 feet",
                       level="EASY",
                       hiking=park11)
session.add(trailInfo1)
session.commit()

trailInfo2 = TrailInfo(user_id=1,
                       trail="Fall Creek",
                       date="-", 
                       url="https://www.alltrails.com/trail/us/california/fall-creek",
                       address="1047 Fetherston Ln, Felton, CA 95018", 
                       distance="8.7 miles",
                       elevation="1837 feet",
                       level="MODERATE",
                       hiking=park11)
session.add(trailInfo2)
session.commit()

trailInfo3 = TrailInfo(user_id=1,
                       trail="Redwood Grove Loop Trail",
                       date="-", 
                       url="https://www.alltrails.com/trail/us/california/redwood-grove-loop-trail--2",
                       address="121 Beth Dr, Felton, CA 95018", 
                       distance="0.8 miles",
                       elevation="36 feet",
                       level="EASY",
                       hiking=park11)
session.add(trailInfo3)
session.commit()

park12 = Hiking(user_id=1, park="Huddart Park")
session.add(park12)
session.commit()

trailInfo1 = TrailInfo(user_id=1,
                       trail="Crystal Springs & Dean Trails",
                       date="2018.10.20", 
                       url="https://www.alltrails.com/trail/us/california/crystal-springs-dean-trails",
                       address="1100 Kings Mountain Rd, Redwood City, CA 94062", 
                       distance="4.5 miles",
                       elevation="935 feet",
                       level="EASY",
                       hiking=park12)
session.add(trailInfo1)
session.commit()

trailInfo2 = TrailInfo(user_id=1,
                       trail="Lonely Trail to Richards Road Loop",
                       date="-", 
                       url="https://www.alltrails.com/trail/us/california/crystal-springs-to-lonely-trail-loop",
                       address="1100 Kings Mountain Rd, Redwood City, CA 94062", 
                       distance="8.4 miles",
                       elevation="1827 feet",
                       level="MODERATE",
                       hiking=park12)
session.add(trailInfo2)
session.commit()
