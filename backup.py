#!/usr/bin/python

import os
import time
import tkinter


def backup():
	global entry_source
	global entry_target
	source = entry_source.get()
	target_dir = entry_target.get()

	today_dir = target_dir + time.strftime('%Y%m%d')
	time_dir = time.strftime('%H%M%S')

	target =today_dir + os.sep + time_dir + '.zip'

	#command_touch = 'zip -rq' +' ' +target + ' '+ source
	#command_touch = '"C:\Program Files\WinRAR\Rar.exe" a' +' '+'\"'+target+'\"'+ ' '+'\"'+source+'\"'
	command_touch = 'rar a' +' '+'"'+target+'"'+ ' '+'"'+source+'"'

	#command = '"C:/Program Files (x86)/WinRAR/WinRAR" x %s * %s\\ -y' % (filename, filename)

	print('target=', target)
	print('source=', source)
	print('command_touch=', command_touch)

	if not os.path.exists(today_dir):
		os.mkdir(today_dir)
		print("今日文件夹不存在，新建！")

	if os.system(command_touch) == 0:
		print('success!')
	else:
		print('Fail!')


root = tkinter.Tk()
root.title('Backup')
root.geometry('200x200')

#下面定义source标签相关内容

#tkinter.Label方法创建一个source标签
lbl_source = tkinter.Label(root, text='source')
#位置
lbl_source.grid(row=0, column=0)
#输入来自
entry_source = tkinter.Entry(root)
entry_source.grid(row=0, column=1)

#下面定义target标签相关内容
lbl_target = tkinter.Label(root, text='target')
lbl_target.grid(row=1, column=0)
entry_target = tkinter.Entry(root)
entry_target.grid(row=1, column=1)

but_back = tkinter.Button(root, text='backup')
but_back.grid(row=3, column=0)
but_back['command'] = backup
# 点击这个按钮，启动backup函数

root.mainloop()