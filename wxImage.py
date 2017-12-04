import itchat
itchat.auto_login()
import math
import math
import os
import PIL.Image as Image




def get_friends_lists():
	friends = itchat.get_friends(update=True)[0:]
	print(friends)
	user = friends[0]["UserName"]
	print(user)
	# @c5a69b45e0b9ad6f910f282847a69e08ffb83f77f91b33f5ba39868a3eb66ae3
	os.mkdir(user)
	return (friends,user)

def get_friend_image(i,friend,user):
	print("get_friend_image：进入函数")
	print("get_friend_image：获取img")
	img=itchat.get_head_img(userName=friend['UserName'])
	print("get_friend_image：img保存到文件")
	with open(user + "/" + str(i) + ".jpg",'wb') as f:
		f.write(img)
		f.close()
	print("get_friend_image：退出函数")

def count_for_distribution(friends):
	print("count_for_distribution:进入函数")
	numpic=len(friends)
	#eachsize=int(math.sqrt(float(640*640)/numpic))
	#numline=int(640/eachsize)
	numline=math.ceil(math.sqrt(float(numpic)))
	eachsize=int(640/numline)
	print("共有好友{0}个，每小图片的边长为{1},一行有{2}个图".format(numpic,eachsize,numline))
	print("count_for_distribution:退出函数")
	return(numpic,eachsize,numline)

def merge_to_total(friends,user):
	print("merge_to_total:开始进入函数")
	print("merge_to_total:下面计算布局")
	numpic, eachsize, numline = count_for_distribution(friends)
	print("merge_to_total:下面新建一张总图")
	total_image = Image.new('RGBA', (640, 640)).convert('RGB')
	#打开图片的时候，要转换成RGB格式，不然最后保存报错：
	#OSError: cannot write mode RGBA as JPEG
	print("merge_to_total:下面开始遍历子图")
	for (i,friend) in enumerate(friends):
	#for friend in friends:
		print("遍历中:第{0}个朋友开始了".format(i))
		print("下面开始获取第{0}个图片".format(i))
		print("fiend type===",type(friend))
		print("fiend===",friend)
		get_friend_image(i,friend,user)
		#get_friend_image(friend)
		print("下面开始合并第{0}个图片到总图片".format(i))
		each_to_total(i,friend, numline,eachsize,total_image,user)
		print("第{0}个图片处理完成，开始下一个".format(i))
	print("merge_to_total:遍历完成，下面开始保存总图")
	total_image.save(user + ".jpg")
	print("merge_to_total:退出函数")

def each_to_total(i,friend,numline,eachsize,total_image,user):
	print("each_to_total1:进入函数")
	try:
		# 打开图片
		img = Image.open(user + "/" + str(i)+ ".jpg").convert('RGB')
		#下载的图片本身是jpg格式，但是拼接前需要转换成rgb格式，否则报错
	except IOError:
		print("Error: 没有找到文件或读取文件失败")
	else:
		# 缩小图片
		img = img.resize((eachsize, eachsize), Image.ANTIALIAS)
		# 拼接图片
		# 第i个图片的位置是……
		#这里需要根据i算x和y
		x=int(i/numline)
		y=i%numline
		print("each_to_total2:位置信息{0} {1}".format(x,y))
		#假如numline=5，i=10，则x=2，y=0
		total_image.paste(img, (x * eachsize, y * eachsize))
	#total_image.save(user + ".jpg")
	print("each_to_total3:退出函数")




def send_to_user(user,total_image):
	itchat.send_image(user+".jpg",'filehelper')


def main():
	friends,user=get_friends_lists()
	print("main:已经获取到朋友们的信息了")
	print('main:共有好友{0}个'.format(len(friends)))
	print("main:下面开始生成总图片")
	print()
	total_image=merge_to_total(friends,user)
	print("main:下面把总图片发送给你")
	print()
	send_to_user(user,total_image)

if __name__=='__main__':
	main()