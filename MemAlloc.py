from tabulate import tabulate
import copy
class Segment:
	def __init__(self, name, size):
		self.name = name
		self.address = "null"
		self.size = size
		
class Process:
	def __init__(self, name):
		self.name = name
		self.seg = []

	def addSeg(self, name, size):
		if self.name == "": self.seg.append(Segment("{s}".format(s = name), size))
		else: self.seg.append(Segment("{p}: {s}".format(p = self.name, s = name), size))
	
	def getSeg(self):
		if self.seg != []: return self.seg[0]
		else: return 0
	
	def delSeg(self):
		del self.seg[0]
	
	def getNum(self):
		return len(self.seg)
	
class Hole:
	def __init__(self, address, size):
		self.name = "Hole"
		self.address = address
		self.size = size
	
#prints memory content
def showMem(mem):
	n = len(mem)
	s = [[i.address, i.name + " ({s})".format(s=i.size)] for i in mem]
	print(tabulate(s, tablefmt="grid"))

#allocates process with allocation method and return mem list after allocation
def palloc(t, m, method):
	p = copy.deepcopy(t)
	mem = copy.deepcopy(m)
	holes = [x for x in mem if isinstance(x, Hole)]
	def alloc(s):
		s.address = fit[0].address
		fit[0].size = fit[0].size - s.size
		fit[0].address = fit[0].address + s.size
		loc = mem.index(fit[0])
		if fit[0].size == 0: del mem[loc]
		mem.insert(loc, s)

	k = p.getNum()
	for i in range(k):
		s = p.getSeg()
		fit = [x for x in holes if x.size >= s.size]
		if fit ==[]:
			print("can't allocate {p}".format(p=p.name))
			return m
		if method == "b": fit = sorted(fit, key=lambda x: x.size)
		elif method == "w": fit = sorted(fit, key=lambda x: x.size, reverse=True)
		alloc(s)
		p.delSeg()

	return mem

# deallocates process, doesn't return anything
def dealloc(t, m):
	p = copy.deepcopy(t)
	mem = [x.name for x in m]
	if p.getSeg().name not in mem:
		print("{p} is not in memory".format(p=p.name))
		return
	s = p.getSeg()
	while s != 0:
		i = mem.index(s.name)
		if isinstance(m[i-1], Hole):
			m[i-1] = Hole(m[i-1].address, m[i-1].size+m[i].size)
			del m[i]
		elif isinstance(m[i+1], Hole):
			m[i] = Hole(m[i].address, m[i].size+m[i+1].size)
			del m[i+1]
		else: m[i] = Hole(m[i].address, m[i].size)
		p.delSeg()
		s = p.getSeg()

#for deallocating old processes, doesn't return anything
def dalloc(p, m):
	mem = [x.name for x in m]
	if p not in mem:
		print("{p} is not in memory".format(p=p))
		return

	i = mem.index(p)
	if isinstance(m[i+1], Hole):
		m[i] = Hole(m[i].address, m[i].size+m[i+1].size)
		del m[i+1]
	if isinstance(m[i-1], Hole):
		m[i-1] = Hole(m[i-1].address, m[i-1].size+m[i].size)
		del m[i]
	else: m[i] = Hole(m[i].address, m[i].size)

#adds old processes to memory space, doesn't return anything
def addOldProc(mem, size):
	n = len(mem)
	i = 0
	ind = 0
	while i < n:
		if i == n-1: slack = size - (mem[-1].address + mem[-1].size)
		else: slack = mem[i+1].address - (mem[i].address + mem[i].size)
		if slack != 0:
			p = Process("")
			p.addSeg("Old Process {p}".format(p=ind), slack)
			s = p.getSeg()
			s.address = mem[i].address + mem[i].size
			mem.insert(i+1, s)
			n = n+1
			ind = ind+1
		i =i+1

#combines all holes into one hole and put in last memory location, returns mem list
def compact(memory, size):
	mem = copy.deepcopy(memory)
	m = []
	addr = 0
	for i in mem:
		if not isinstance(i, Hole):
			i.address = addr
			m.append(i)
			addr = addr + i.size
	m.append(Hole(addr, size-addr))
	return m
			
#المين عشان اجرب الفانكشنز بس

def main():
	size = 780
	mem = [Hole(0, 20), Hole(50, 40), Hole(125, 300), Hole(480, 200)]
	p1 = Process("P1")
	p1.addSeg("Code", 301)
	p1.addSeg("data", 100)
	p2 = Process("P2")
	p2.addSeg("Code", 20)
	p2.addSeg("Data", 40)
	p3 = Process("P3")
	p3.addSeg("Code", 50)
	p3.addSeg("data", 60)
	queue = [p1, p2, p3]
	mem = sorted(mem, key= lambda x: x.address)
	addOldProc(mem, size)
	#mem = compact(mem, size)
	dalloc("Old Process 2", mem)
	for i in queue: mem = palloc(i, mem, "f")
	showMem(mem)

main()