import zlib,struct,re
import os

typeIndex={'ULONG':4,
	   'U24':3,
	   'USHORT':2,
	   'UBYTE':1,
	   'LINK':0,
	   'DATA':0}

class decompose:
	def parseFormat(self):
		select=0
		fconfig=open(os.path.join(self.dir,'config.cft'),'rt')
		for line in fconfig:
			result = re.match(r'\$(\S+)\s*=\s*(\S+)',line)
			if result:
				if result.group(1)=='CONTENT,OFFSET':
					self.formatStr[1]=typeIndex[result.group(2)]
					select=2
				else:
					self.formatStr[select]+=typeIndex[result.group(2)]
	def writeOffsetIndex(self):
		self.offsets=[]
		i=0
		fdata=open(os.path.join(self.dir,'files.dat'),'rb')
		while True:
			i+=1
			if(len(fdata.read(self.formatStr[0]))==0):
				break
			bytes_object = fdata.read(self.formatStr[1])
			for i in range(4 - self.formatStr[1]):
				bytes_object += b'\x00'
			self.offsets.append(struct.unpack('L',bytes_object)[0])
			fdata.read(self.formatStr[2])
	def inflateTDA(self):
		fin=open(os.path.join(self.dir,'CONTENT.tda'), 'rb')
		fdst=open(os.path.join(self.outdir,'output'), 'wb')
		findex=open(os.path.join(self.dir,'CONTENT.tda.tdz'),'rb')
		byte=[]
		while True:
			bin=findex.read(8)
			if len(bin)==0:break
			byte.append(struct.unpack('ii',bin))
		i=0
		print('Now decompressing...')
		for xi,bytei in byte:
			i+=1
			dedata=zlib.decompress(fin.read(bytei))
			fdst.write(dedata)
		print('Done!Total %d entries.' %i)
	def writeFiles(self):
		fin=open(os.path.join(self.dir,'NAME.tda'),'rb')
		raw=fin.read()
		name_bytes_obj_list=raw.split(b'\x00')
		fin=open(os.path.join(self.outdir,'output'),'rb')
		for i in range(len(self.offsets)):
			name_bytes_obj = name_bytes_obj_list[i]
			name = name_bytes_obj.decode('utf-8')
			fout=open(os.path.join(self.outdir,name),'wb')
			if(i==len(self.offsets)-1):
				fout.write(fin.read()[:-1])
			else:
				fout.write(fin.read(self.offsets[i+1]-self.offsets[i])[:-1])
			print('Now writing separate files:'+str(i+1)+'\r',)
		print('\nDone!')
	def __init__(self,dir,outdir):
		self.dir=dir
		self.outdir=outdir
		self.formatStr=[0,0,0]
		self.parseFormat()
		self.writeOffsetIndex()
