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
	clnd_fl1 = []
	clnd_fl2 = []
	pnts = []
	variences = []
	for item in fl1:		
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
		if '****' in item:
			clnd_fl1.append(pnts)
			pnts = []
			continue
		pnts.append(item)
	pnts = []

	for item in fl2:		
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
		if '****' in item:
			clnd_fl2.append(pnts)
			pnts = []
			continue
		pnts.append(item)

	a = 0
	if clnd_fl1 == clnd_fl2:
		variences.append('All Points Defined The Same Between The Selected Files.')
	elif len(clnd_fl1) <= len(clnd_fl2):
		for pnt in range(len(clnd_fl1)):
			if clnd_fl2[a] != clnd_fl1[a]:
				b = 0
				if len(clnd_fl2[a]) <= len(clnd_fl1[a]):
					for i in range(len(clnd_fl2[a])):
						if clnd_fl2[a][b] != clnd_fl1[a][b]:
							variences.append(clnd_fl1[a][b])
							variences.append(clnd_fl2[a][b])
						b += 1
				else:
					for i in range(len(clnd_fl1[a])):
						if clnd_fl2[a][b] != clnd_fl1[a][b]:
							variences.append(clnd_fl1[a][b])
							variences.append(clnd_fl2[a][b])
						b += 1
				variences.append(clnd_fl2[a])
				variences.append('<br>')
			a += 1
	elif len(clnd_fl2) < len(clnd_fl1):
		for pnt in range(len(clnd_fl2)):
			if clnd_fl2[a] != clnd_fl1[a]:				
				b = 0
				if len(clnd_fl2[a]) <= len(clnd_fl1[a]):
					for i in range(len(clnd_fl2[a])):
						if clnd_fl2[a][b] != clnd_fl1[a][b]:
							variences.append(clnd_fl1[a][b])
							variences.append(clnd_fl2[a][b])
						b += 1
				else:
					for i in range(len(clnd_fl1[a])):
						if clnd_fl2[a][b] != clnd_fl1[a][b]:
							variences.append(clnd_fl1[a][b])
							variences.append(clnd_fl2[a][b])
						b += 1
				variences.append(clnd_fl2[a])
				variences.append('<br>')
			a += 1
	print(len(variences))
	return render(request, 'panels/pntDef.html', {'variences': variences})