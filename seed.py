from app import app
from models import db, User


db.drop_all()
db.create_all()

u1 = User.signup(username="user1",password="user1",email="user1@gmail.com",
                image_url=User.image_url.default.arg,
                is_trainer=User.is_trainer.default.arg)

u2 = User.signup(username="user2",password="user2",email="user2@gmail.com",
                image_url=User.image_url.default.arg,
                is_trainer=True)
            
u3 = User.signup(username="yoga",password="user3",email="user3@gmail.com",
                image_url="https://www.thelifestylejournalist.in/wp-content/uploads/2018/06/payal-gidwani-tiwari-the-lifestyle-journalist-magazine-1200x1304.jpg",
                is_trainer=True)

u4 = User.signup(username="user4",password="user4",email="user4@gmail.com",
                image_url=User.image_url.default.arg,
                is_trainer=False)

u5 = User(username="yoga",password="user3",email="user3@gmail.com",
                image_url="https://www.thelifestylejournalist.in/wp-content/uploads/2018/06/payal-gidwani-tiwari-the-lifestyle-journalist-magazine-1200x1304.jpg",
                is_trainer=True, about="I'm professional trainer")





db.session.add_all([u1,u2,u3,u4])
db.session.commit()