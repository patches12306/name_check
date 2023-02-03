import itertools 
from itertools import permutations
import pandas as pd
import numpy as np


key_list = [['06E01365', 'Acadiana','acadianacares.org' ], ['0613350', 'Access' ], ['0610680', 'Arbor', 'Innis', ], ['06E01275', 'Baptist' ], ['0618420', 'Baton Rouge' ], ['067570', 'CareSouth', 'Care South' ], ['06E01083', 'CASSE' ], ['062480', 'Catahoula' ], ['061550', 'City of New','homeless' ], ['06E01048', 'Common' ], ['06E00338', 'Crescent' ], ['061920', 'David' ], ['06E00261', 'Delhi' ], ['062870' , 'EXCELth'], ['06E01376', 'Go', 'Greater Ouachita'], ['062350', 'Iberia','ICCHC' ], ['0623760', 'Inclusiv' ], ['06E01062', 'Jeff' ], ['06E00523', 'DePaul', 'Marillac', 'Daughters', 'Ascension'], ['06E01298', 'Mercy' ], ['0627740', 'CommuniHealth', 'Morehouse', 'Communihealth'], ['06E01066', 'NOELA', 'MQVN'], ['06E01137', 'Odyssey'], ['06E01178', 'Open','ohcc' ], ['060190', 'Outpatient' ], ['06E01370', 'Plaquemines' ], ['0618980', 'RKM', 'Healthy Feliciana'], ['068480', 'Primary Health','PHSc' ], ['06E01198', 'Priority' ], ['067090', 'Rapides' ], ['063710', 'Southeast' ], ['062900', 'Southwest' ], ['064760', 'St. Gabriel' ], ['06E00020', 'St. Thomas' ], ['06E01206', 'START', 'start' ], ['063380', 'SWLA' ], ['060180', 'Teche' ], ['0622350', 'Tensas' ], ['06E00021', 'Winn', 'Trinity']]
email_list = [['LPCA','lpca.net'],['AcadianaCares', 'acadianacares.org'], ['Access', 'accesshealthla.org'], ['Arbor', 'arborfamilyhealth.org'], ['Arbor', 'inchc.org'], ['Ascension', 'ascension.org'], ['Ascension Depaul Services', 'dcsno.org'], ['Baptist', 'bchsnola.org'], ['Baton Rouge Primary Care', 'brprimarycare.org'], ['Care South', 'caresouth.org'], ['CASSE', 'casseusa.com'], ['Catahoula Paris Hospital District #2', 'cphd2.org'], ['Common Ground', 'commongroundclinic.org'], ['Communihealth', 'communihealth.org'], ['CrescentCare', 'crescentcare.org'], ['CrescentCare', 'crescentcarehealth.org '], ['David Raines', 'davidraineschc.org'],['CommuniHealth','mcmcinc.org'] ,['Delhi Hospital', 'delhihospital.com'], ['Excelth', 'excelth.com'], ['Go Care', 'go-care.org'], ['Healthcare for the Homeless', 'nola.gov'], ['Hospital Service District No. 1 Plaquemines Medical Center', 'plaqueminesmedicalcenter.com'], ['Iberia', 'icchc.org'], ['InclusivCare', 'inclusivcare.com'], ['InclusivCare', 'jchcc.org'], ['Jefferson Parish Human Services Authority', 'jphsa.org'], ['Mercy Medical', 'lamercymedical.com'], ['NOELA', 'noelachc.org'], ['Odyssey House', 'ohlinc.org'], ['Open Health', 'ohcc.org'], ['Outpatient', 'outpatientmedical.org'], ['Primary Health Services Center', 'phsccenter.org'], ['Priority Health Care', 'phc-no.org'], ['RKM', 'rkmcare.org'], ['Southeast', 'shchc.org'], ['Southwest', 'swlphc.com'], ['St. Gabriel', 'stgabrielchc.org'], ['St. Thomas', 'stthomaschc.org'], ['Start', 'startcorp.org'], ['SWLA', 'swlahealth.org'], ['Teche', 'tabhealth.org'], ['Tensas', 'tensashealth.org'], ['Winn', 'winnchc.org'],['Southeast','@schc.org']]


path = r"C:\Users\bnguyen\Documents\LPCA\DRVS_user_attendance\84988609327_RegistrationReport.csv"

HPT_dem = pd.read_csv(path)



def cap_permutations(s):

	#capital letter permutation
    lu_sequence = ((c.lower(), c.upper()) for c in s)
 
    perm = [''.join(x) for x in itertools.product(*lu_sequence)]
    # perm_arr = []
    

    # permutation
    #perms = [''.join(j) for j in permutations(s)]
     	#perm_arr.append(perms)

    # return perm_arr
    return perm



#check if email is in email list
#returns center name if email is in list
def email_check(email):
	for key in email_list:
		if key[1] in email:
			return key[0]


#check if center name is in key list
#returns BHCMISID if name in key list
#if not, a permutation check is done on the center name for capitalizations and mispellings
def check(name):
	for key in key_list:
		for common in key[1:]:
			if common in name:
				return key[0]
		
	for key in key_list:
		for common in key[1:]:
			# print(cap_permutations(common))
			if any(ele in name for ele in cap_permutations(common)) == True:
				#if cap_permutations(common) in name:
				return key[0]
			else:
				return
		



#HPT_dem['Center'] = HPT_dem.apply (lambda row: email_check(row['Email']), axis=1)

#calls email check on a column in a dataframe, creates a center column with center names based on emails
#returns a new dataframe
def email_fill(df, name_column):
	df['Center'] = df.apply (lambda row: email_check(row[name_column]), axis=1)
	return df

#calls name check ona column in a dataframe, creates a BHCMISID column based on center names
#returns a new datafrme with a BHCMISID column
def name_check(df,column_name):
	df = df.dropna(subset=[column_name])
	df['BHCMISID'] = df.apply (lambda row: check(row[column_name]), axis=1)
	return df


#combines email_fill and name_check to get a new df with a center column and a BHCMISID column from an email column
def email_name_check(df,name_column):
	new_df = email_fill(df,name_column)
	new_df = name_check(df,'Center')
	return new_df

