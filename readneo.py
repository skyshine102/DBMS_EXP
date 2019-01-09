from py2neo import Graph, Node, Relationship
import sys
import csv
import random

uri = "bolt://localhost:7687"
user = "neo4j"
password = "3386"

graph = Graph(uri=uri, user=user, password=password)
graph.run("MATCH (n:Student),(c:Course) DETACH DELETE n,c")
graph.run("MATCH (cb:Club) , (i:Interest) , (r:Residence) DETACH DELETE cb,i,r")
stu_list = []
course_list = [('通信原理','電信'), ('EDA導論','電子'), ('積體電路設計','電子'), ('演算法','CS'), ('數位系統設計','電子'), ('數位語音處理概論','CS'), 
    ('電腦視覺','CS'), ('生醫工程概論','生醫'), ('固態電子學','電子'), ('近代物理','電子'), ('電力工程導論','電機') , ('控制系統','電機') ,('光電導論','光電'),
    ('電腦網路導論','CS'), ('平面顯示技術通論','光電'), ('資料結構','CS'), ('SQL-NoSQL','CS'), ('微波系統導論','電信')] 
club_list = ['魔術社', '陽光椰子服務社','山林服務社','漁村服務社','咖啡研究社','蛋糕研究社','Maker社','野餐社', '調酒社','熱舞社','椰風搖滾社','散打社','柔道社','劍道社','','','']
residence_list = ['台北','桃園','新竹','新北','台中','台南','高雄','雲林','花蓮','宜蘭','台北','中壢','新竹','新竹']
interest_list =['籃球','足球','睡覺','讀sql','打code','看小說','看電影','看動漫','聽音樂','逛書店','彈鋼琴','打工','實習','彈吉他','旅遊','購物','吃東西']
for i in range(len(course_list)):
	graph.run("MERGE (c:Course{name:{name},label:{label}})",name = course_list[i][0], label = course_list[i][1])
for i in range(len(club_list)):
	if club_list[i] == '':
		continue
	graph.run("MERGE (c:Club{name:{name}})",name = club_list[i])
for i in range(len(residence_list)):
	graph.run("MERGE (c:Residence{name:{name}})",name = residence_list[i])
for i in range(len(interest_list)):
	graph.run("MERGE (c:Interest{name:{name}})",name = interest_list[i])
with open("response.csv" , encoding='utf-8') as f:
	rows = csv.DictReader(f)
	for row in rows:
		student = row['name']
		grade = row['grade']
		if student not in stu_list:
			stu_list.append(student)
			graph.run("MERGE (s:Student{name:{name},grade:{grade},real_name:{rname}})",name = student[:1] + '?' + student[2:], grade = grade, rname = student)
		friend1 = row['friend1']
		friend2 = row['friend2']
		friend3 = row['friend3']
		friend4 = row['friend4']
		friend5 = row['friend5']
		course = row['course']
		courses = course.rstrip().split(', ')
		rand_club = random.randint(0 , len(club_list)-1)
		rand_interest = random.randint(0,len(interest_list)-1)
		rand_residence = random.randint(0,len(residence_list)-1)

		if club_list[rand_club] != '':
			graph.run("MATCH (m:Student{real_name:{name1}}),(n:Club{name:{name2}}) CREATE (m)-[:PARTICIPATE]->(n)",name1 = student, name2 = club_list[rand_club])
		graph.run("MATCH (m:Student{real_name:{name1}}),(n:Interest{name:{name2}}) CREATE (m)-[:INTERESTS]->(n)",name1 = student, name2 = interest_list[rand_interest])
		graph.run("MATCH (m:Student{real_name:{name1}}),(n:Club{name:{name2}}) CREATE (m)-[:FROM]->(n)",name1 = student, name2 = residence_list[rand_residence])
		for i in courses:
			graph.run("MATCH (m:Student{real_name:{name1}}),(n:Course{name:{name2}}) CREATE (m)-[:LIKES]->(n)",name1 = student, name2 = i)
		if friend1 not in stu_list:
			graph.run("MERGE (s:Student{name:{name},grade:{grade},real_name:{rname}})",name = friend1[:1] + '?' + friend1[2:], grade = grade, rname = friend1)	
			stu_list.append(friend1)
		graph.run("MATCH (m:Student{real_name:{name1}}),(n:Student{real_name:{name2}}) CREATE (m)-[:FRIENDS_OF]->(n)",name1 = student, name2 = friend1)
		if friend2 not in stu_list:
			graph.run("MERGE (s:Student{name:{name},grade:{grade},real_name:{rname}})",name = friend2[:1] + '?' + friend2[2:], grade = grade, rname = friend2)
			stu_list.append(friend2)
		graph.run("MATCH (m:Student{real_name:{name1}}),(n:Student{real_name:{name2}}) CREATE (m)-[:FRIENDS_OF]->(n)",name1 = student, name2 = friend2)
		if friend3 not in stu_list:
			graph.run("MERGE (s:Student{name:{name},grade:{grade},real_name:{rname}})",name = friend3[:1] + '?' + friend3[2:], grade = grade, rname = friend3)
			stu_list.append(friend3)
		graph.run("MATCH (m:Student{real_name:{name1}}),(n:Student{real_name:{name2}}) CREATE (m)-[:FRIENDS_OF]->(n)",name1 = student, name2 = friend3)
		if friend4:
			if friend4 not in stu_list:
				graph.run("MERGE (s:Student{name:{name},grade:{grade},real_name:{rname}})",name = friend4[:1] + '?' + friend4[2:], grade = grade, rname = friend4)
				stu_list.append(friend4)
			graph.run("MATCH (m:Student{real_name:{name1}}),(n:Student{real_name:{name2}}) CREATE (m)-[:FRIENDS_OF]->(n)",name1 = student, name2 = friend4)
		if friend5:
			if friend5 not in stu_list:
				graph.run("MERGE (s:Student{name:{name},grade:{grade},real_name:{rname}})",name = friend5[:1] + '?' + friend5[2:], grade = grade, rname = friend5)
				stu_list.append(friend5)
			graph.run("MATCH (m:Student{real_name:{name1}}),(n:Student{real_name:{name2}}) CREATE (m)-[:FRIENDS_OF]->(n)",name1 = student, name2 = friend5)



