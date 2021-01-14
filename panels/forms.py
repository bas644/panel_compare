from django import forms

class ReportForm(forms.Form):
	reportType = forms.ChoiceField(label= 'Report Type', choices=[('', ''), ('pplr', 'PPLR'),
																	 ('pntDef', 'Point Definition'), ('trndDef', 'Trend Definition'),
																	 ('ppcl', 'PPCL Report'),])
	f1 = forms.FileField(label= 'Please select the 1st file ---> ')
	f2 = forms.FileField(label= 'Please select the 2nd file ---> ')