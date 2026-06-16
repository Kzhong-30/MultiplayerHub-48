from app.database import SessionLocal, engine
from app import models, auth
from datetime import date, datetime, timedelta

models.Base.metadata.create_all(bind=engine)

db = SessionLocal()

try:
    existing = db.query(models.User).count()
    if existing > 0:
        print("已有数据，跳过初始化")
        db.close()
        exit()

    hashed_pwd = auth.get_password_hash("123456")

    users = [
        {
            "username": "petlover",
            "email": "petlover@example.com",
            "hashed_password": hashed_pwd,
            "avatar": "https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=100",
            "phone": "13800138001",
            "address": "北京市朝阳区建国路",
            "latitude": 39.9042,
            "longitude": 116.4074,
            "bio": "热爱宠物，家有金毛"
        },
        {
            "username": "catfan",
            "email": "catfan@example.com",
            "hashed_password": hashed_pwd,
            "avatar": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=100",
            "phone": "13800138002",
            "address": "北京市海淀区中关村",
            "latitude": 39.9842,
            "longitude": 116.3074,
            "bio": "猫咪爱好者，养了两只英短"
        },
        {
            "username": "dogdad",
            "email": "dogdad@example.com",
            "hashed_password": hashed_pwd,
            "avatar": "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=100",
            "phone": "13800138003",
            "address": "北京市西城区西单",
            "latitude": 39.9142,
            "longitude": 116.3674,
            "bio": "哈士奇铲屎官"
        }
    ]

    created_users = []
    for user_data in users:
        user = models.User(**user_data)
        db.add(user)
        db.flush()
        created_users.append(user)

    pets_data = [
        {
            "owner_id": 1,
            "name": "大黄",
            "species": "dog",
            "breed": "金毛寻回犬",
            "gender": "male",
            "birthday": date(2020, 5, 15),
            "weight": 32.5,
            "avatar": "https://images.unsplash.com/photo-1552053831-71594a27632d?w=200",
            "bio": "温顺的大暖男"
        },
        {
            "owner_id": 2,
            "name": "小咪",
            "species": "cat",
            "breed": "英国短毛猫",
            "gender": "female",
            "birthday": date(2021, 8, 20),
            "weight": 4.2,
            "avatar": "https://images.unsplash.com/photo-1573865526739-10659fec78a5?w=200",
            "bio": "高冷的蓝猫"
        },
        {
            "owner_id": 3,
            "name": "二哈",
            "species": "dog",
            "breed": "哈士奇",
            "gender": "male",
            "birthday": date(2021, 3, 10),
            "weight": 28.0,
            "avatar": "https://images.unsplash.com/photo-1605568427561-40dd23c2acea?w=200",
            "bio": "拆家小能手"
        },
        {
            "owner_id": 2,
            "name": "布丁",
            "species": "cat",
            "breed": "布偶猫",
            "gender": "female",
            "birthday": date(2022, 1, 5),
            "weight": 3.8,
            "avatar": "https://images.unsplash.com/photo-1592194996308-7b43878e84a6?w=200",
            "bio": "温柔的小仙女"
        }
    ]

    for pet_data in pets_data:
        pet = models.Pet(**pet_data)
        db.add(pet)
        db.flush()

        for i in range(5):
            wr = models.WeightRecord(
                pet_id=pet.id,
                weight=pet_data["weight"] - i * 0.5,
                record_date=date.today() - timedelta(days=30 * i),
                note=f"第 {i+1} 次称重"
            )
            db.add(wr)

        vaccines = ["狂犬疫苗", "四联疫苗", "六联疫苗"]
        for i, v in enumerate(vaccines):
            vr = models.VaccineRecord(
                pet_id=pet.id,
                vaccine_name=v,
                vaccine_date=date.today() - timedelta(days=90 * i),
                next_due_date=date.today() + timedelta(days=90 * (i + 1)),
                hospital="爱宠动物医院",
                note=f"{v} 接种"
            )
            db.add(vr)

        for i in range(3):
            photo = models.PetPhoto(
                pet_id=pet.id,
                url=f"https://loremflickr.com/400/300/{pet_data['species']}?lock={pet.id * 10 + i}",
                description=f"{pet_data['name']} 的照片 {i+1}",
                is_avatar=(i == 0)
            )
            db.add(photo)

    posts_data = [
        {
            "author_id": 1,
            "pet_id": 1,
            "content": "今天带大黄去公园玩，它开心得不行！分享给大家看看~",
            "media_type": "image",
            "media_url": "https://images.unsplash.com/photo-1583511655857-d19b40a7a54e?w=600",
            "tags": ["金毛", "公园", "日常"],
            "latitude": 39.9042,
            "longitude": 116.4074,
            "location_name": "朝阳公园"
        },
        {
            "author_id": 2,
            "pet_id": 2,
            "content": "小咪今天又在窗台晒太阳了，真是一只懒猫~",
            "media_type": "image",
            "media_url": "https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba?w=600",
            "tags": ["英短", "猫咪", "日常"],
            "latitude": 39.9842,
            "longitude": 116.3074,
            "location_name": "中关村"
        },
        {
            "author_id": 3,
            "pet_id": 3,
            "content": "二哈今天又把沙发拆了，我真的要崩溃了...",
            "media_type": "video",
            "media_url": "https://sample-videos.com/video321/mp4/720/big_buck_bunny_720p_1mb.mp4",
            "tags": ["哈士奇", "拆家", "吐槽"],
            "latitude": 39.9142,
            "longitude": 116.3674,
            "location_name": "西单"
        },
        {
            "author_id": 2,
            "pet_id": 4,
            "content": "布丁的新窝到了，她看起来很喜欢！",
            "media_type": "image",
            "media_url": "https://images.unsplash.com/photo-1545249390-6bdfa286032f?w=600",
            "tags": ["布偶猫", "新窝", "日常"],
            "latitude": 39.9842,
            "longitude": 116.3074,
            "location_name": "中关村"
        }
    ]

    for post_data in posts_data:
        post = models.Post(**post_data)
        db.add(post)
        db.flush()

        for i in range(2):
            comment = models.Comment(
                post_id=post.id,
                author_id=((i % 3) + 1),
                content=f"评论内容 {i+1}：好可爱！" if i % 2 == 0 else "哈哈哈太萌了~",
                likes_count=i
            )
            db.add(comment)

        for i in range(1, 4):
            if i != post_data["author_id"]:
                like = models.Like(post_id=post.id, user_id=i)
                db.add(like)
        post.likes_count = 2

    breeds_data = [
        {
            "name": "金毛寻回犬",
            "species": "dog",
            "origin": "英国",
            "lifespan": "10-12年",
            "weight_range": "25-34kg",
            "height_range": "55-61cm",
            "temperament": "友善、聪明、温顺、忠诚",
            "appearance": "体型匀称，被毛浓密有光泽，颜色多为金色或奶油色",
            "care_guide": "每天需要1-2小时运动，定期梳毛，注意髋关节发育问题",
            "health_issues": "髋关节发育不良、肘部发育不良、心脏病、眼部问题",
            "feeding_guide": "每天2-3餐，注意控制体重，避免肥胖",
            "exercise_needs": "高能量犬种，需要大量运动和智力训练",
            "image_url": "https://images.unsplash.com/photo-1552053831-71594a27632d?w=400"
        },
        {
            "name": "哈士奇",
            "species": "dog",
            "origin": "西伯利亚",
            "lifespan": "12-14年",
            "weight_range": "20-27kg",
            "height_range": "51-60cm",
            "temperament": "活泼、友善、独立、精力旺盛",
            "appearance": "中等体型，被毛厚实，眼色多样，耳朵直立",
            "care_guide": "需要大量运动，会嚎叫，注意夏天防暑",
            "health_issues": "眼部问题、髋关节发育不良、皮肤病",
            "feeding_guide": "高蛋白饮食，注意不要过度喂食",
            "exercise_needs": "非常高，每天至少2小时高强度运动",
            "image_url": "https://images.unsplash.com/photo-1605568427561-40dd23c2acea?w=400"
        },
        {
            "name": "英国短毛猫",
            "species": "cat",
            "origin": "英国",
            "lifespan": "12-20年",
            "weight_range": "4-8kg",
            "height_range": "30-35cm",
            "temperament": "温和、独立、安静、亲人",
            "appearance": "圆脸、圆眼、短而密的被毛，体型健壮",
            "care_guide": "每周梳毛1-2次，注意口腔护理，控制体重",
            "health_issues": "多囊肾病、心脏病、肥胖",
            "feeding_guide": "定时定量喂食，避免过度喂食",
            "exercise_needs": "适度，每天15-30分钟互动玩耍",
            "image_url": "https://images.unsplash.com/photo-1573865526739-10659fec78a5?w=400"
        },
        {
            "name": "布偶猫",
            "species": "cat",
            "origin": "美国",
            "lifespan": "12-17年",
            "weight_range": "4-9kg",
            "height_range": "23-28cm",
            "temperament": "温顺、粘人、安静、喜欢被抱",
            "appearance": "大型猫，被毛长而柔软，蓝色眼睛，毛色多样",
            "care_guide": "每天梳毛，定期洗澡，注意毛发打结",
            "health_issues": "心肌病、多囊肾病、泌尿系统问题",
            "feeding_guide": "优质猫粮，适量湿粮，保证水分摄入",
            "exercise_needs": "适度，喜欢安静的环境，不需要大量运动",
            "image_url": "https://images.unsplash.com/photo-1592194996308-7b43878e84a6?w=400"
        }
    ]

    for breed_data in breeds_data:
        breed = models.BreedEncyclopedia(**breed_data)
        db.add(breed)

    diseases_data = [
        {
            "name": "犬瘟热",
            "species": "dog",
            "symptoms": "发热、咳嗽、流鼻涕、眼部分泌物、腹泻、呕吐、神经症状",
            "causes": "犬瘟热病毒感染，通过呼吸道传播",
            "diagnosis": "临床症状结合实验室检测，如ELISA、PCR",
            "treatment": "支持治疗，抗病毒药物，抗生素预防继发感染",
            "prevention": "定期接种疫苗，避免接触患病动物",
            "severity": "high"
        },
        {
            "name": "细小病毒",
            "species": "dog",
            "symptoms": "剧烈呕吐、血便、发热、脱水、精神萎靡",
            "causes": "犬细小病毒感染，通过粪口途径传播",
            "diagnosis": "临床症状，粪便抗原检测",
            "treatment": "输液治疗，止吐止泻，抗生素，支持治疗",
            "prevention": "疫苗接种，环境消毒，避免接触病犬",
            "severity": "high"
        },
        {
            "name": "猫瘟",
            "species": "cat",
            "symptoms": "发热、呕吐、腹泻、脱水、白细胞减少",
            "causes": "猫泛白细胞减少症病毒感染",
            "diagnosis": "临床症状，血常规，病毒检测",
            "treatment": "支持治疗，输液，抗生素，干扰素",
            "prevention": "疫苗接种，环境消毒",
            "severity": "high"
        },
        {
            "name": "皮肤病",
            "species": "dog,cat",
            "symptoms": "瘙痒、红斑、脱毛、皮屑、结痂",
            "causes": "真菌、细菌、寄生虫、过敏、内分泌问题",
            "diagnosis": "皮肤刮片、伍德灯检查、真菌培养、过敏原检测",
            "treatment": "根据病因使用抗真菌、抗生素、驱虫药、抗过敏药",
            "prevention": "定期驱虫，保持皮肤清洁，注意营养均衡",
            "severity": "moderate"
        },
        {
            "name": "牙结石",
            "species": "dog,cat",
            "symptoms": "口臭、牙齿变黄、牙龈红肿、进食困难",
            "causes": "食物残渣、细菌矿化形成牙结石",
            "diagnosis": "口腔检查",
            "treatment": "超声波洁牙，必要时拔牙",
            "prevention": "定期刷牙，使用洁牙零食，定期口腔检查",
            "severity": "low"
        }
    ]

    for disease_data in diseases_data:
        disease = models.DiseaseGuide(**disease_data)
        db.add(disease)

    meetups_data = [
        {
            "organizer_id": 1,
            "title": "周末朝阳公园狗狗聚会",
            "description": "周末带狗狗来朝阳公园一起玩吧！欢迎所有品种的狗狗~",
            "location": "朝阳公园西门草坪",
            "latitude": 39.9342,
            "longitude": 116.4774,
            "meetup_date": datetime.now() + timedelta(days=3),
            "max_participants": 20
        },
        {
            "organizer_id": 2,
            "title": "猫咪爱好者线下交流会",
            "description": "分享养猫经验，交流猫咪养护知识，还有小礼品哦~",
            "location": "中关村创业大街咖啡厅",
            "latitude": 39.9842,
            "longitude": 116.3074,
            "meetup_date": datetime.now() + timedelta(days=7),
            "max_participants": 15
        }
    ]

    for meetup_data in meetups_data:
        meetup = models.Meetup(**meetup_data)
        db.add(meetup)
        db.flush()

        participant = models.MeetupParticipant(
            meetup_id=meetup.id,
            user_id=meetup_data["organizer_id"]
        )
        db.add(participant)

    db.commit()
    print("数据初始化成功！")
    print("默认账号：petlover / catfan / dogdad，密码均为：123456")

except Exception as e:
    print(f"初始化失败: {e}")
    db.rollback()
finally:
    db.close()
