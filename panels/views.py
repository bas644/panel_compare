from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .forms import ReportForm

fl1 = ''
fl2 = ''

def home(request):
	global fl1
	global fl2
	if request.method == 'POST':
		f1 = request.FILES['f1']
		f2 = request.FILES['f2']
		form = ReportForm(request.POST)
		rptType = form['reportType'].value()

		fl1 = f1.read()		
		fl1 = str(fl1)
		fl1 = list(fl1.split('\\r'))

		fl2 = f2.read()
		fl2 = str(fl2)
		fl2 = list(fl2.split('\\r'))

		if rptType == 'pplr':
			return redirect('panels-pplr')

		if rptType == 'pntDef':
			return redirect('panels-pntDef')

		if rptType == 'trndDef':
			return redirect('panels-trndDef')

			
	form = ReportForm()
	return render(request, 'panels/home.html', {'form': form})


def about(request):
	return render(request, 'panels/about.html')


def pplr_compare(request):	
	clnd_fl1 = []
	clnd_fl2 = []
	for item in fl1:		
		if 'MD Anderson Cancer Center' in item:
			continue
		if 'Panel Point Log Report' in item:
			continue
		if 'Selected' in item:
			continue
		if 'Filter' in item:
			continue
		if '***' in item:
			continue
		if 'Name:' in item:
			continue
		if 'Points' in item:
			fl1_points = item
			continue
		if '___' in item:
			continue
		clnd_fl1.append(item)

	for item in fl2:		
		if 'MD Anderson Cancer Center' in item:
			continue
		if 'Panel Point Log Report' in item:
			continue
		if 'Selected' in item:
			continue
		if 'Filter' in item:
			continue
		if '***' in item:
			continue
		if 'Name:' in item:
			continue
		if 'Points' in item:
			fl2_points = item
			continue
		if '___' in item:
			continue
		clnd_fl2.append(item)
	
	rng = 0
	extra = 0
	variences = []	
	pnt = []

	if len(clnd_fl1) > len(clnd_fl2):
		rng = len(clnd_fl2)
		extra = len(clnd_fl1)
	else:
		rng = len(clnd_fl1)
		extra = len(clnd_fl2)

	for x in range(0, rng):
		if '*F*' in clnd_fl2[x]:
			clnd_fl2[x] = clnd_fl2[x].replace('\\n', '', 1)
			a = 0				
			for char in clnd_fl2[x]:
				if char == '(':
					break
				a += 1
			b = a - 16
			c = clnd_fl2[x][0:b]
			for y in clnd_fl1:
				if c in y:
					if '*F*' in clnd_fl1[x]:
						pass
					else:
						variences.append(clnd_fl2[x])
	
	return render(request, 'panels/pplr.html', {'variences': variences})


def pntDef_compare(request):
	clnd_fl1 = {}
	clnd_fl2 = {}
	variences = {}
	pnts = []
	dkey = ''
	for item in fl1:
		if item == '':
			continue
		if item == ' ':
			continue
		if 'MD Anderson Cancer Center' in item:
			continue
		if 'Point Definition Report' in item:
			continue
		if 'Selection:' in  item:
			continue
		if 'Points)' in item:
			continue
		if '____' in item:
			continue
		if 'Revision Number:' in item:
			continue
		if 'Panel Name:' in item:
			continue
		if 'Point Address:' in item:
			continue
		if item[-1] == "-":
			continue
		if '****' in item:
			for b in range(len(pnts)):
				try:
					pnts.remove('')
				except:
					pass
				try:
					pnts.remove(' ')
				except:
					pass
			clnd_fl1[dkey] = pnts
			dkey = ''
			pnts = []
			continue
		if "\\n" in item:
			item = item.replace('\\n', '', 1)
		if 'Point System Name' in item:
			dkey = item
			continue
		pnts.append(item)
	
	pnts = []
	dkey = ''
	for item in fl2:
		if item == '':
			continue
		if item == ' ':
			continue
		if 'MD Anderson Cancer Center' in item:
			continue
		if 'Point Definition Report' in item:
			continue
		if 'Selection:' in  item:
			continue
		if 'Points)' in item:
			continue
		if '____' in item:
			continue
		if 'Revision Number:' in item:
			continue
		if 'Panel Name:' in item:
			continue
		if 'Point Address:' in item:
			continue
		if item[-1] == "-":
			continue
		if '****' in item:
			for b in range(len(pnts)):
				try:
					pnts.remove('')
				except:
					pass
				try:
					pnts.remove(' ')
				except:
					pass
			clnd_fl2[dkey] = pnts
			dkey = ''
			pnts = []
			continue
		if "\\n" in item:
			item = item.replace('\\n', '', 1)
		if 'Point System Name' in item:
			dkey = item
			continue
		pnts.append(item)

	first = []
	second = []
	nomatch = []
	
	for ky1 in clnd_fl1.keys():
		if ky1 not in clnd_fl2.keys():
			first.append((ky1, clnd_fl1[ky1]))
	if first:
		variences['1st file only'] = first
	for ky2 in clnd_fl2.keys():
		if ky2 not in clnd_fl1.keys():
			second.append((ky2, clnd_fl2[ky2]))
	if second:
		variences['2nd file only'] = second
	for ky3 in clnd_fl1.keys():
		if ky3 in clnd_fl2.keys():
			if clnd_fl1[ky3] != clnd_fl2[ky3]:
				pnt1 = ''
				pnt2 = ''
				v = 0
				if (len(clnd_fl1[ky3])) == (len(clnd_fl2[ky3])):
					for i in range(len(clnd_fl1[ky3])):
						if clnd_fl2[ky3][v] != clnd_fl1[ky3][v]:
							pnt1 = clnd_fl1[ky3][v]
							pnt2 = clnd_fl2[ky3][v]
							nomatch.append((ky3, pnt1, pnt2))
						v += 1
				else:
					nomatch.append((ky3, clnd_fl1[ky3], clnd_fl2[ky3]))

	variences["Files don't match"] = nomatch

	return render(request, 'panels/pntDef.html', {'variences': variences})


def trndDef_compare(request):
	clnd_fl1 = {}
	clnd_fl2 = {}
	variences = {}
	dfs = []
	totdfs = []
	dkey = ''
	for item in fl1:
		if 'MD Anderson Cancer Center' in item:
			continue
		if 'Trend Definition Report' in item:
			continue
		if 'Selection:' in  item:
			continue
		if 'Points)' in item:
			continue
		if '____' in item:
			continue
		if 'Supervised:' in item:
			continue
		if 'Revision Number:' in item:
			continue
		if 'Descriptor:' in item:
			continue
		if 'Last Collect' in item:
			continue
		if item[-1] == "-":
			continue
		if "\\n" in item:
			item = item.replace('\\n', '', 1)
		if 'Point Name:' in item:
			if 'Trigger Point Name:' not in item:
				dkey = item
				continue
		if 'Definition' in item:
			if dfs:
				for b in range(len(dfs)):
					try:
						dfs.remove('')
					except:
						pass
					try:
						dfs.remove(' ')
					except:
						pass
				totdfs.append(dfs)
				dfs = []
			dfs.append(item)
		if '****' in item:
			for b in range(len(dfs)):
				try:
					dfs.remove('')
				except:
					pass
				try:
					dfs.remove(' ')
				except:
					pass
			totdfs.append(dfs)
			dfs = []
			clnd_fl1[dkey] = totdfs
			dkey = ''
			totdfs = []
			continue
		dfs.append(item)

	dfs = []
	totdfs = []
	dkey = ''
	for item in fl2:
		if 'MD Anderson Cancer Center' in item:
			continue
		if 'Trend Definition Report' in item:
			continue
		if 'Selection:' in  item:
			continue
		if 'Points)' in item:
			continue
		if '____' in item:
			continue
		if 'Supervised:' in item:
			continue
		if 'Revision Number:' in item:
			continue
		if 'Descriptor:' in item:
			continue
		if 'Last Collect' in item:
			continue
		if item[-1] == "-":
			continue
		if "\\n" in item:
			item = item.replace('\\n', '', 1)
		if 'Point Name:' in item:
			if 'Trigger Point Name:' not in item:
				dkey = item
				continue
		if 'Definition' in item:
			if dfs:
				for b in range(len(dfs)):
					try:
						dfs.remove('')
					except:
						pass
					try:
						dfs.remove(' ')
					except:
						pass
				totdfs.append(dfs)
				dfs = []
			dfs.append(item)
		if '****' in item:
			for b in range(len(dfs)):
				try:
					dfs.remove('')
				except:
					pass
				try:
					dfs.remove(' ')
				except:
					pass
			totdfs.append(dfs)
			dfs = []
			clnd_fl2[dkey] = totdfs
			dkey = ''
			totdfs = []
			continue
		dfs.append(item)

	first = []
	second = []
	nomatch = []
	
	for ky1 in clnd_fl1.keys():
		if ky1 not in clnd_fl2.keys():
			first.append((ky1, clnd_fl1[ky1]))
	if first:
		variences['1st file only'] = first
	for ky2 in clnd_fl2.keys():
		if ky2 not in clnd_fl1.keys():
			second.append((ky2, clnd_fl2[ky2]))
	if second:
		variences['2nd file only'] = second
	for ky3 in clnd_fl1.keys():
		if ky3 in clnd_fl2.keys():
			if clnd_fl1[ky3] != clnd_fl2[ky3]:
				pnt1 = ''
				pnt2 = ''
				v = 0
				if (len(clnd_fl1[ky3])) == (len(clnd_fl2[ky3])):
					for i in range(len(clnd_fl1[ky3])):
						if clnd_fl2[ky3][v] != clnd_fl1[ky3][v]:
							pnt1 = clnd_fl1[ky3][v]
							pnt2 = clnd_fl2[ky3][v]
							nomatch.append((ky3, pnt1, pnt2))
						v += 1
				else:
					nomatch.append((ky3, clnd_fl1[ky3], clnd_fl2[ky3]))

	variences["Files don't match"] = nomatch

	return render(request, 'panels/trndDef.html', {'variences': variences})

