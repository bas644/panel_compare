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

		if rptType == 'ppcl':
			return redirect('panels-ppcl')

		if rptType == 'pntSrtr':
			return redirect('panels-pntSrtr')

		if rptType == 'P2BpntDef':
			return redirect('panels-P2BpntDef')
			
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



def ppcl_compare(request):
	clnd_fl1 = {}
	clnd_fl2 = {}
	variences = []

	lines = []
	newlines = []
	dkey = ''
	for item in fl1:
		if 'MD Anderson Cancer Center' in item:
			continue
		if 'Panel PPCL Report' in item:
			continue
		if 'Panel Name:' in item:
			continue
		if 'Program Name:' in item:
			continue
		if 'Field Panels:' in item:
			continue
		if 'Programs:' in item:
			continue
		if 'Line Range:' in item:
			continue
		if '____' in item:
			continue
		if item[-1] == "-":
			continue
		if "\\n" in item:
			item = item.replace('\\n', '', 1)
		item.strip()
		lines.append(item)	
	for line in lines:
		if len(line) > 4:
			newlines.append(line)
	lines = newlines
	newlines = []
	for a in range(len(lines)):
		if lines[a][0] == 'E' or lines[a][0] == 'D':
			newlines.append(lines[a])
		else:
			newlines[-1] = newlines[-1] + lines[a].strip()
	lines = newlines
	newlines = []
	for line in lines:
		ind = False
		newline = ''
		for char in line:
			try:
				if int(char):
					ind = True
			except:
				pass
			if ind:
				newline = newline + str(char)
		newlines.append(newline)
	lines = newlines
	newlines = []
	for line in lines:
		line = line.split(' ',1)
		dkey = line[0]
		line[1] = line[1].strip()
		clnd_fl1[dkey] = line[1]

	lines = []
	newlines = []
	for item in fl2:
		if 'MD Anderson Cancer Center' in item:
			continue
		if 'Panel PPCL Report' in item:
			continue
		if 'Panel Name:' in item:
			continue
		if 'Program Name:' in item:
			continue
		if 'Field Panels:' in item:
			continue
		if 'Programs:' in item:
			continue
		if 'Line Range:' in item:
			continue
		if '____' in item:
			continue
		if item[-1] == "-":
			continue
		if "\\n" in item:
			item = item.replace('\\n', '', 1)
		item.strip()
		lines.append(item)	
	for line in lines:
		if len(line) > 4:
			newlines.append(line)
	lines = newlines
	newlines = ['']
	for a in range(len(lines)):
		if lines[a][0] == 'E' or lines[a][0] == 'D':
			newlines.append(lines[a])
		else:
			newlines[-1] = newlines[-1] + lines[a].strip()
	lines = newlines
	newlines = []
	for line in lines:
		ind = False
		newline = ''
		for char in line:
			try:
				if int(char):
					ind = True
			except:
				pass
			if ind:
				newline = newline + str(char)
		newlines.append(newline)
	lines = newlines
	newlines = []
	for line in lines:
		line = line.split(' ',1)
		dkey = line[0]
		if len(line) > 1:
			line[1] = line[1].strip()
			clnd_fl2[dkey] = line[1]
	
	if clnd_fl1 == clnd_fl2:
		variences.append('All code in selected files match')
	else:
		variences.append('Check the following lines for discrepancies')
		for key in clnd_fl1.keys():
			if key not in clnd_fl2.keys():
				if 'The following lines only appears in the first file' not in variences:
					variences.append('The following lines only appears in the first file')
				variences.append(str(key) + '   ' + str(clnd_fl1[key]))
		for key in clnd_fl2.keys():
			if key not in clnd_fl1.keys():
				if 'The following lines only appears in the second file' not in variences:
					variences.append('The following lines only appears in the second file')
				variences.append(str(key) + '   ' + str(clnd_fl2[key]))
		for key in clnd_fl1.keys():
			if key in clnd_fl2.keys():
				if clnd_fl1[key] != clnd_fl2[key]:
					if 'The follow lines do not match between the files' not in variences:
						variences.append('The follow lines do not match between the files')
					variences.append(str(key) + '   ' + str(clnd_fl1[key]))
					variences.append(str(key) + '   ' + str(clnd_fl2[key]))

	return render(request, 'panels/ppcl.html', {'variences': variences})


def findIt(numOne, numTwo):
    var = []
    p1Key = []
    p2Key = []

    for p1Name in numOne:
        key = list(p1Name.keys())
        key = key[0]
        p1Key.append(key)
    for p2Name in numTwo:
        key = list(p2Name.keys())
        key = key[0]
        p2Key.append(key)

    for k in p1Key:
        if k not in p2Key:
            var.append('Point is in First file only:   ' + k)

    for k in p2Key:
        if k not in p1Key:
            var.append('Point is in Second file only:   ' + k)

    var.append('These points have non-matching attributes:')
    
    for p1Name in numOne:
        key = list(p1Name.keys())
        key = key[0]
        for p2Name in numTwo:
            if key in p2Name:
                if p1Name[key] == p2Name[key]:
                    var.append(key + ': matches')
                else:
                	att1s = []
                	att2s = []

                	att = list(p1Name[key].keys())
                	att1s.append(att)
                	att1s = att1s[0]

                	att = list(p2Name[key].keys())
                	att2s.append(att)
                	att2s = att2s[0]

                	for i in att1s:
                		if i not in att2s:
                			var.append(key + ': ' + i + ' only in first file')
                	for i in att2s:
                		if i not in att1s:
                			var.append(key + ': ' + i + ' only in second file')

                	for i in att1s:
                		if 'Panel Name' in i or 'Point Address' in i:
                			continue
                		if i in att2s:
                			if p1Name[key][i] != p2Name[key][i]:
                				var.append(key + '---> ' +  i + ' First File ' + str(p1Name[key][i]) + ' Second File ' + str(p2Name[key][i]))
                                                            
    return(var)      


def pntSrtr_compare(request):
	variences = []
	clnd_fl1 = []
	clnd_fl2 = []
	lines = []
	info = {}
	totalInfo = {}
	pnts = []
	pnt = ''

	for item in fl1:
		if '\\n' in item:
			if len(lines) > 0:
				lines = lines[0].split(',')
				pnts.append(lines)
			lines = []
			item = item.replace('\\n', '', 1)
			item = item.replace('"', '')
		if item == "b'":
			continue
		if 'End of Report' in item:
			continue
		lines.append(item)

	for p in range(1, len(pnts)):
		for i in range(len(pnts[0])):
			if pnts[0][i] == 'Name':
				pnt = pnts[p][i]
			info[pnts[0][i]] = pnts[p][i]
		totalInfo[pnt] = info
		clnd_fl1.append(totalInfo)
		info = {}
		pnt = ''
		totalInfo = {}

	lines = []
	info = {}
	totalInfo = {}
	pnts = []
	pnt = ''

	for item in fl2:
		if '\\n' in item:
			if len(lines) > 0:
				lines = lines[0].split(',')
				pnts.append(lines)
			lines = []
			item = item.replace('\\n', '', 1)
			item = item.replace('"', '')
		if item == "b'":
			continue
		if 'End of Report' in item:
			continue
		lines.append(item)

	for p in range(1, len(pnts)):
		for i in range(len(pnts[0])):
			if pnts[0][i] == 'Name':
				pnt = pnts[p][i]
			info[pnts[0][i]] = pnts[p][i]
		totalInfo[pnt] = info
		clnd_fl2.append(totalInfo)
		info = {}
		pnt = ''
		totalInfo = {}

	variences = findIt(clnd_fl1, clnd_fl2)
	return render(request, 'panels/pntSrtr.html', {'variences': variences})


def P2BpntDef_compare(request):
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
		if 'Object Name:' in item:
			continue
		if 'Object ID:' in item:
			continue
		if 'Point Address:' in item:
			continue
		if 'Alarm Count' in item:
			continue
		if 'Normal ack Enabled:' in item:
			continue
		if 'Print Info with Alarm:' in item:
			continue
		if 'Mode Point:' in item:
			continue
		if 'Mode Delay' in item:
			continue
		if 'Default Destination' in item:
			continue
		if 'Alarm Mode:' in item:
			continue
		if 'Offset     Alarm Priority' in item:
			continue
		if 'N/A               3' in item:
			continue
		if 'Notification Class:' in item:
			continue
		if 'Annunciate To' in item:
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
		if 'Relinquish Default:' in item:
			pnts.insert(-1, item)
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
		if 'Object Name:' in item:
			continue
		if 'Object ID:' in item:
			continue
		if 'Point Address:' in item:
			continue
		if 'Alarm Count' in item:
			continue
		if 'Normal ack Enabled:' in item:
			continue
		if 'Print Info with Alarm:' in item:
			continue
		if 'Mode Point:' in item:
			continue
		if 'Mode Delay' in item:
			continue
		if 'Default Destination' in item:
			continue
		if 'Alarm Mode:' in item:
			continue
		if 'Offset     Alarm Priority' in item:
			continue
		if 'N/A               3' in item:
			continue
		if 'Notification Class:' in item:
			continue
		if 'Annunciate To' in item:
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
		if 'Relinquish Default:' in item:
			pnts.insert(-1, item)
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
              




