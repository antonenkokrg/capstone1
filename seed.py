from app import app
from models import db, User, Trainings, Trainings_users


db.drop_all()
db.create_all()

u1 = User.signup(username="Trainer5",password="tester1",email="user1@gmail.com",
                image_url=User.image_url.default.arg,
                is_trainer=True)
u1.about = "I specialize in full body conditioning and strengthening, integrated flexibility training, core strengthening, rehabilitation therapy, sports specific training and performance training for all sports. "
u1.id = 111

u2 = User.signup(username="Demetrios",password="tester2",email="user2@gmail.com",
                image_url="https://hips.hearstapps.com/hmg-prod.s3.amazonaws.com/images/mh-trainer-2-1533576998.png",
                is_trainer=True)
u2.about = "I specialize in full body conditioning and strengthening, integrated flexibility training, core strengthening, rehabilitation therapy, sports specific training and performance training for all sports. "
u2.id = 222

u3 = User.signup(username="YogaTeacher",password="tester3",email="user3@gmail.com",
                image_url="https://www.thelifestylejournalist.in/wp-content/uploads/2018/06/payal-gidwani-tiwari-the-lifestyle-journalist-magazine-1200x1304.jpg",
                is_trainer=True)
u3.about = "I specialize in full body conditioning and strengthening, integrated flexibility training, core strengthening, rehabilitation therapy, sports specific training and performance training for all sports. "
u3.id = 333

u4 = User.signup(username="GeorgeT",password="tester4",email="user4@gmail.com",
                image_url=User.image_url.default.arg,
                is_trainer=True)
u4.about = "I specialize in full body conditioning and strengthening, integrated flexibility training, core strengthening, rehabilitation therapy, sports specific training and performance training for all sports. "
u4.id = 444

u5 = User.signup(username="YogaTrainer",password="tester5",email="user5@gmail.com",
                image_url="https://www.thelifestylejournalist.in/wp-content/uploads/2018/06/payal-gidwani-tiwari-the-lifestyle-journalist-magazine-1200x1304.jpg",
                is_trainer=True)

u5.about = "I specialize in full body conditioning and strengthening, integrated flexibility training, core strengthening, rehabilitation therapy, sports specific training and performance training for all sports. "
u5.id = 555

u6 = User.signup(username="LazyDog",password="tester6",email="user6@gmail.com",
                image_url="https://myanimals.com/wp-content/uploads/2018/10/Lazy-dog-sleeping.jpg",
                is_trainer=True)

u6.about = "I specialize in full body conditioning and strengthening, integrated flexibility training, core strengthening, rehabilitation therapy, sports specific training and performance training for all sports. "
u6.id = 666

u7 = User.signup(username="LazyDog1",password="tester7",email="user7@gmail.com",
                image_url="https://myanimals.com/wp-content/uploads/2018/10/Lazy-dog-sleeping.jpg",
                is_trainer=False)

u7.about = "I specialize in full body conditioning and strengthening, integrated flexibility training, core strengthening, rehabilitation therapy, sports specific training and performance training for all sports. "
u7.id = 777

u8 = User.signup(username="LazyDog2",password="tester8",email="user8@gmail.com",
                image_url="https://myanimals.com/wp-content/uploads/2018/10/Lazy-dog-sleeping.jpg",
                is_trainer=False)

u8.about = "I specialize in full body conditioning and strengthening, integrated flexibility training, core strengthening, rehabilitation therapy, sports specific training and performance training for all sports. "
u8.id = 888




t1 = Trainings(title="cardio 60 min", description="This free course, Exploring sport coaching and psychology, investigates how scientific and management ideas contribute...", 
                date=Trainings.date.default.arg,trainer_users_id=333)
t1.id = 111

t2 = Trainings(title="cardio 60 min", description="This free course, Exploring sport coaching and psychology, investigates how scientific and management ideas contribute...", 
                date=Trainings.date.default.arg,trainer_users_id=333)
t2.id = 222

t3 = Trainings(title="cardio 60 min", description="This free course, Exploring sport coaching and psychology, investigates how scientific and management ideas contribute...", 
                date=Trainings.date.default.arg,trainer_users_id=333)
t3.id = 333

t4 = Trainings(title="cardio 60 min", description="This free course, Exploring sport coaching and psychology, investigates how scientific and management ideas contribute...", 
                date=Trainings.date.default.arg,trainer_users_id=333)
t4.id = 444







db.session.add_all([u1,u2,u3,u4,u5,u6,u7,u8,t1,t2,t3,t4])
db.session.commit()

tu1 = Trainings_users(users_id=777,trainings_id=111)
tu2 = Trainings_users(users_id=777,trainings_id=222)
tu3 = Trainings_users(users_id=777,trainings_id=333)
tu4 = Trainings_users(users_id=777,trainings_id=444)
tu5 = Trainings_users(users_id=888,trainings_id=111)
tu6 = Trainings_users(users_id=888,trainings_id=222)
tu7 = Trainings_users(users_id=888,trainings_id=333)


db.session.add_all([tu1,tu2,tu3,tu4,tu5,tu6,tu7])
db.session.commit()