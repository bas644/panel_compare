from django import forms

class ReportForm(forms.Form):
	reportType = forms.ChoiceField(label= 'Report Type', choices=[('', ''), ('pplr', 'PPLR'),
																	 ('pntDef', 'Point Definition'), ('trndDef', 'Trend Definition'),
																	 ('ppcl', 'PPCL Report'), ('pntSrtr', 'Point Sorter Report'),
																	 ('P2BpntDef', 'P1 to BACnet Point Definition')],
																	  widget=forms.Select(attrs={'style': 'width:200px'}))

	f1 = forms.FileField(label= 'Please select the 1st file')
	
	f2 = forms.FileField(label= 'Please select the 2nd file')