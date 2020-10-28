from pyxnat import Interface
import os
import logging
import pydicom
from todayClass import todaytime
from config_read import config_data
import time


#print(date)
'''
url='https://dmxnat.nchc.org.tw'
username='v1_yhyang'
password='yhyang'
'''

'''
url,username,password = config_data().read_config('config.ini')    
interface = Interface(server=url,user=username,password=password)
print('ok')
reconnect_max_number=10
date = todaytime().today()
m="dx"
m2="otherDicom"
sec=7
for i in range(reconnect_max_number):
    try:
        interface.select('/project/v1_YHtest_0916-3'
                  ).create()
        print("create tree success")
        break
    except Exception as e:
        print(e)
        #print(logging.error(tree))
        print("reconnect "+str(i+1))
        time.sleep(sec)
for i in range(reconnect_max_number):
    try:
        interface.select('/project/v1_YHtest_0916-3/subject/test_subject'
                  ).create()
        print("create tree success")
        break
    except Exception as e:
        print(e)
        #print(logging.error(tree))
        print("reconnect "+str(i+1))
        time.sleep(sec)
for i in range(reconnect_max_number):
    try:
        interface.select('/project/v1_YHtest_0916-3/subject/test_subject/experiment/test_session/'
                  ).create(
                          **{'experiments':'xnat:'+m+'SessionData',
                            'xnat:'+m+'SessionData/date':date,
                            })
        print("create tree success")
        break
    except Exception as e:
        print(e)
        #print(logging.error(tree))
        print("reconnect "+str(i+1))
        time.sleep(sec)
for i in range(reconnect_max_number):
    try:
        interface.select('/project/v1_YHtest_0916-3/subject/test_subject/experiment/test_session/scan/test_san'
                  ).create(
                          **{
                            'scans':'xnat:'+m2+'ScanData',
                            'xnat:'+m2+'ScanData/quality':'usable',
                            'xnat:'+m2+'ScanData/type':'Unknow',
                            })
        print("create tree success")
        break
    except Exception as e:
        print(e)
        #print(logging.error(tree))
        print("reconnect "+str(i+1))
        time.sleep(sec)
'''   


def scan_root_dir():
    data_dirs = []
    for item in os.listdir('.'):
        if (os.path.isdir(item)):
            if (item[:1] != '.'):
                data_dirs.append(os.path.abspath(os.path.join(os.getcwd(), item)))

    return data_dirs


def create_projects():
    project_name=[]
    for index, dir_info in enumerate(os.walk(data_dir+"/projects/")):
        project_name = dir_info[1]
        break

    return project_name

def create_subjects(projects_name):
    subject_name={}
    for project in projects_name:
        for index, dir_info in enumerate(os.walk(data_dir+"/projects/"+project+"/")):
            subject_name[project] = dir_info[1]
            break
       
    return subject_name

def create_SessionAndScan_or_scan(projects_name,subject_name):
    datatype = 'DICOM'
    resource_name = 'DICOM'
    format_type="DICOM"
    #datatype = 'Unknow'
    session_name=dict()
    scan_name=[]
    sec=7
    for project in projects_name:
        for subject in subject_name[project]:
            for index, dir_info in enumerate(os.walk(data_dir+"/projects/"+project+"/"+subject+"/")):
                if index == 0 and len(dir_info[2]) > 0:
                    scan_tag = 2
                    break
                elif index == 0:
                    continue
                elif len(dir_info[2]) > 0:
                    scan_tag = 1
                    break
                elif len(dir_info[2]) == 0:
                    scan_tag = 0
                    break
            break

        print("scan_tag = "+str(scan_tag))
        
        if scan_tag == 2:
            for subject in subject_name[project]:
                for index, dir_info in enumerate(os.walk(data_dir+"/projects/"+project+"/"+subject+"/")):
                    for filename in dir_info[2]:
                        try:
                            print("one dir= "+data_dir+"/projects/"+project+"/"+subject+"/"+filename)
                            ds = pydicom.dcmread(data_dir+"/projects/"+project+"/"+subject+"/"+filename)
                            Modality1 = ds.Modality.lower()
                            Modality2 = ds.Modality.lower()
                            if Modality1 == 'dx':
                                Modality2= 'otherDicom'
                            elif Modality1 != 'mr' and Modality1 != 'ct' and Modality1 != 'hd' and Modality1 != 'cr' and filename == dir_info1[2][-1]:
                                Modality1 = 'otherDicom'
                                Modality2 = 'otherDicom'
                            elif Modality1 != 'mr' and Modality1 != 'ct' and Modality1 != 'hd' and Modality1 != 'cr':
                                continue
                            print("one Modality= "+Modality1)
                            break
                        except Exception as e:
                            continue
                    break
                for try_number in range(reconnect_max_number):
                    try:
                        interface.select('/project/'+project+'/subject/'+subject+'/experiment/'+subject+'_'+Modality1.upper()+'1'+'/scan/'+'999'
                                            ).create(
                                                **{'experiments':'xnat:'+Modality1+'SessionData',
                                                'xnat:'+Modality1+'SessionData/date':date,
                                                'scans':'xnat:'+Modality2+'ScanData',
                                                'xnat:'+Modality2+'ScanData/quality':'usable',
                                                'xnat:'+Modality2+'ScanData/type':datatype,
                                                })
                        print("create "+'/project/'+project+'/subject/'+subject+'/experiment/'+subject+'_'+Modality1.upper()+'1'+'/scan/'+'999'+" success")
                        break
                    except Exception as e:
                        print(e)
                        print("reconnect create "+'/project/'+project+'/subject/'+subject+'/experiment/'+subject+'_'+Modality1.upper()+'1'+'/scan/'+'999'+" "+str(try_number+1))
                        time.sleep(sec)
                        pass

                for try_number in range(reconnect_max_number):
                            try:
                                updataToScan = interface.select('/project/'+project+'/subject/'+subject+'/experiment/'+subject+'_'+Modality1.upper()+'1'+'/scan/'+'999')
                                dataResource = updataToScan.resource(resource_name)
                                dataResource.put_dir(data_dir+"/projects/"+project+"/"+subject+"/",format=format_type)
                                print("put data to "+'/project/'+project+'/subject/'+subject+'/experiment/'+subject+'_'+Modality1.upper()+'1'+'/scan/'+'999'+" success")
                                break
                            except Exception as e:
                                print(e)
                                print("reconnect to "+'/project/'+project+'/subject/'+subject+'/experiment/'+subject+'_'+Modality1.upper()+'1'+'/scan/'+'999'+" "+str(try_number+1)+" put data")
                                time.sleep(sec)
                                pass
                
                    
                    
        elif scan_tag == 1:
            for subject in subject_name[project]:
                for index, dir_info in enumerate(os.walk(data_dir+"/projects/"+project+"/"+subject+"/")):
                    scans_name = dir_info[1]
                    for scan in scans_name:
                        for index1, dir_info1 in enumerate(os.walk(data_dir+"/projects/"+project+"/"+subject+"/"+scan+"/")):
                            for filename in dir_info1[2]:
                                try:
                                    print("one dir= "+data_dir+"/projects/"+project+"/"+subject+"/"+scan+"/"+filename)
                                    ds = pydicom.dcmread(data_dir+"/projects/"+project+"/"+subject+"/"+scan+"/"+filename)
                                    Modality1 = ds.Modality.lower()
                                    Modality2 = ds.Modality.lower()
                                    if Modality1 == 'dx':
                                        Modality2= 'cr'
                                    elif Modality1 != 'mr' and Modality1 != 'ct' and Modality1 != 'hd' and Modality1 != 'cr' and filename == dir_info1[2][-1]:
                                        Modality1 = 'otherDicom'
                                        Modality2 = 'otherDicom'
                                    elif Modality1 != 'mr' and Modality1 != 'ct' and Modality1 != 'hd' and Modality1 != 'cr':
                                        continue
                                    print("one Modality= "+Modality1)
                                    break
                                except Exception as e:
                                    continue
                            break
                        
                        for try_number in range(reconnect_max_number):
                            try:
                                interface.select('/project/'+project+'/subject/'+subject+'/experiment/'+subject+'_AI-99'+'/scan/'+scan
                                                 ).create(
                                                     **{'experiments':'xnat:'+Modality1+'SessionData',
                                                        'xnat:'+Modality1+'SessionData/date':date,
                                                        'scans':'xnat:'+Modality2+'ScanData',
                                                        'xnat:'+Modality2+'ScanData/quality':'usable',
                                                        'xnat:'+Modality2+'ScanData/type':datatype,
                                                        })
                                print("create "+'/project/'+project+'/subject/'+subject+'/experiment/'+subject+'_AI-99'+'/scan/'+scan+" success")
                                break
                            except Exception as e:
                                print(e)
                                print("reconnect create "+'/project/'+project+'/subject/'+subject+'/experiment/'+subject+'_AI-99'+'/scan/'+scan+" "+str(try_number+1))
                                time.sleep(sec)
                                pass
                            
                        for try_number in range(reconnect_max_number):
                            try:
                                updataToScan = interface.select('/project/'+project+'/subject/'+subject+'/experiment/'+subject+'_AI-99'+'/scan/'+scan)
                                dataResource = updataToScan.resource(resource_name)
                                dataResource.put_dir(data_dir+"/projects/"+project+"/"+subject+"/"+scan,format=format_type)
                                print("put data to "+'/project/'+project+'/subject/'+subject+'/experiment/'+subject+'_AI-99'+'/scan/'+scan+" success")
                                break
                            except Exception as e:
                                print(e)
                                print("reconnect to "+'/project/'+project+'/subject/'+subject+'/experiment/'+subject+'_AI-99'+'/scan/'+scan+" "+str(try_number+1)+" put data")
                                time.sleep(sec)
                                pass
                    break

                
        elif scan_tag == 0:
            for subject in subject_name[project]:
                for index, dir_info in enumerate(os.walk(data_dir+"/projects/"+project+"/"+subject+"/")):
                    session_name[subject] = dir_info[1]
                    break
            #print("session_name"+str(session_name))
            
            for subject in subject_name[project]:
                for session in session_name[subject]:
                    for index, dir_info in enumerate(os.walk(data_dir+"/projects/"+project+"/"+subject+"/"+session+"/")):
                        scan_name = dir_info[1]
                        
                        if len(scan_name) == 0:
                            continue
                        else:
                            for scan in scan_name:
                                for index1, dir_info1 in enumerate(os.walk(data_dir+"/projects/"+project+"/"+subject+"/"+session+"/"+scan+"/")):
                                    for filename in dir_info1[2]:
                                        try:
                                            print("two dir= "+data_dir+"/projects/"+project+"/"+subject+"/"+session+"/"+scan+"/"+filename)
                                            ds = pydicom.dcmread(data_dir+"/projects/"+project+"/"+subject+"/"+session+"/"+scan+"/"+filename)
                                            Modality1 = ds.Modality.lower()
                                            Modality2 = ds.Modality.lower()
                                            if Modality1 == 'dx':
                                                Modality2= 'cr'
                                            elif Modality1 != 'mr' and Modality1 != 'ct' and Modality1 != 'hd' and Modality1 != 'cr' and filename == dir_info1[2][-1]:
                                                Modality1 = 'otherDicom'
                                                Modality2 = 'otherDicom'
                                            elif Modality1 != 'mr' and Modality1 != 'ct' and Modality1 != 'hd' and Modality1 != 'cr':
                                                continue
                                            print("two Modality= "+Modality1)
                                            break
                                        except Exception as e:
                                            continue
                                    break
                                
                                for try_number in range(reconnect_max_number):
                                    try:
                                        interface.select('/project/'+project+'/subject/'+subject+'/experiment/'+session+'_AI-99'+'/scan/'+scan
                                                         ).create(
                                                             **{'experiments':'xnat:'+Modality1+'SessionData',
                                                                'xnat:'+Modality1+'SessionData/date':date,
                                                                'scans':'xnat:'+Modality2+'ScanData',
                                                                'xnat:'+Modality2+'ScanData/quality':'usable',
                                                                'xnat:'+Modality2+'ScanData/type':datatype,
                                                                })
                                        print("create "+'/project/'+project+'/subject/'+subject+'/experiment/'+session+'_AI-99'+'/scan/'+scan+" success")
                                        break
                                    except Exception as e:
                                        print(e)
                                        print("reconnect create "+'/project/'+project+'/subject/'+subject+'/experiment/'+session+'_AI-99'+'/scan/'+scan+" "+str(try_number+1))
                                        time.sleep(sec)
                                        pass
                                    
                                for try_number in range(reconnect_max_number):
                                    try:
                                        updataToScan = interface.select('/project/'+project+'/subject/'+subject+'/experiment/'+session+'_AI-99'+'/scan/'+scan)
                                        dataResource = updataToScan.resource(resource_name)
                                        dataResource.put_dir(data_dir+"/projects/"+project+"/"+subject+"/"+session+"/"+scan,format=format_type)
                                        print("put data to "+'/project/'+project+'/subject/'+subject+'/experiment/'+session+'_AI-99'+'/scan/'+scan+" success")
                                        break
                                    except Exception as e:
                                        print(e)
                                        print("reconnect to "+'/project/'+project+'/subject/'+subject+'/experiment/'+session+'_AI-99'+'/scan/'+scan+" "+str(try_number+1)+" put data")
                                        time.sleep(sec)
                                        pass
                                
                          
if __name__ == "__main__" :
    
    url,username,password = config_data().read_config('config.ini')
    
    interface = Interface(server=url,user=username,password=password)
    reconnect_max_number=100
    date = todaytime().today()
    
    data_dirs = scan_root_dir()
    data_dir = data_dirs[0]
    
    cp=create_projects()
    cs=create_subjects(cp)
    #print(cs)
    csa=create_SessionAndScan_or_scan(cp,cs)










