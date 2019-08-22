import logging.config
from ast.ast_processor_Production import AstProcessorProduction
from ast.ast_processor_Test import AstProcessorTest
from ast.ast_processor_TestMethodCall import AstProcessorTestMethodCall
from ast.basic_info_listener_pt import BasicInfoListener
import glob
import re
import os
from collections import defaultdict
import xlwt
 


class rdict(dict):
    def __getitem__(self, key):
        try:
            return super(rdict, self).__getitem__(key)
        except:
            try:
                ret=[]
                for i in self.keys():
                    m= re.match("^"+key+"$",i)
                    if m:ret.append( super(rdict, self).__getitem__(m.group(0)) )
            except:raise(KeyError(key))
        return ret


if __name__ == '__main__':

    def ClonePairwithOneTest():
        t = 't1'
        projectname = 'kafaka89'

        NicadTest = open(r'TestPath_' + t + '_' + projectname + '.txt','r',encoding="utf-8_sig")
        NicadTestPath = NicadTest.readlines()
        NtPath = [Ntline.replace('\n', '') for Ntline in NicadTestPath]

        getNicadPath = []
        for n in range(len(NtPath)):
            name = 'C:/Users/ryosuke-ku/Desktop/SCRAPING/Method_Scraping/xml_scraping/NicadOutputFile_' + t + '_' + projectname + '/Nicad_' + t + '_' + projectname + str(n+1) + '.java'
            getNicadPath.append(name)

        notest = 0
        hastest = 0
        nodetect = 0
        count = 0
        for i in range(len(NtPath)): 
            Testmethodcalls_list = AstProcessorTestMethodCall(None, BasicInfoListener()).execute('C:/Users/ryosuke-ku/Desktop/NiCad-5.1/systems/' + NtPath[i]) #target_file_path(テストファイル)内のメソッド名をすべて取得
            Productionmethods_list = AstProcessorProduction(None, BasicInfoListener()).execute(getNicadPath[i]) #プロダクションファイル内のメソッド名をすべて取得
            Testmethods_list = AstProcessorTest(None, BasicInfoListener()).execute('C:/Users/ryosuke-ku/Desktop/NiCad-5.1/systems/' + NtPath[i]) #target_file_path(テストファイル)内のメソッド呼び出しをすべて取得

            file = open(getNicadPath[i],'r')
            line = file.readline()
            line2 = file.readline()
            # print('<Production Code Path> ' + line2[2:].replace('\n',''))

            # # print('<プロダクションコードPath>' + getNicadPath[i])
            # print('<Test Code Path> ' + 'C:/Users/ryosuke-ku/Desktop/NiCad-5.1/systems/' + NtPath[i])
            # print('<Clone Pairs Path> ' + line[2:].replace('\n',''))
            # print('<Test Methods>')
            # # print(Testmethods_list)
            # for t in Testmethods_list:
            #     print(t)

            cnt = 1
            methodmapcall = defaultdict(list)
            for k in Testmethodcalls_list:
                # print(k)
                for l in Testmethodcalls_list[k]:
                    for m in l:
                        methodcall = str(cnt) + ':' + m
                        # print(methodcall)
                        methodmapcall[methodcall].append(k)
                        cnt+=1

            rd = rdict(methodmapcall)
            words = []
            reusetest1 = []
            try:
                key = Productionmethods_list[0]
                # print('<Production Methods>')
                # print(key)
                # print('<Reusable Test Methods>')
                # print(rd["^(?=.*" + key + ").*$"])
                # print(len(rd["^(?=.*" + key + ").*$"]))
                retmethods = rd["^(?=.*" + key + ").*$"]
                if len(rd["^(?=.*" + key + ").*$"]) == 0:
                    notest += 1
                else:
                    for o in re.split('([a-z]+)([A-Z][a-z]+)|([A-Z][a-z]+)', key):
                        if o != None and o != '':
                            words.append(o)
        
                    # print(words)
                    # print(retmethods)
                    for i in words:
                        # print(i.lower())
                        for j in retmethods:
                            if i.lower() in j[0].lower():
                                reusetest1.append(j[0])
                            #     j1 = 1
                            # else:
                            #     j1 = 0
                        
                    if len(reusetest1) != 0:
                        hastest += 1
                    else:
                        notest += 1

                rt1 = list(set(reusetest1))
                print(rt1)





                    # hastest += 1
                    # print('<Production Code Path> ' + line2[2:].replace('\n',''))
                    # # print('<プロダクションコードPath>' + getNicadPath[i])
                    # print('<Test Code Path> ' + 'C:/Users/ryosuke-ku/Desktop/NiCad-5.1/systems/' + NtPath[i])
                    # print('<Clone Pairs Path> ' + line[2:].replace('\n',''))
                    # print('<Test Methods>')
                    # # print(Testmethods_list)
                    # for t in Testmethods_list:
                    #     print(t)
                    # print('<Production Methods>')
                    # print(key)
                    # print('<Reusable Test Methods>')
                    # for w in retmethods:
                    #     print(w[0])
                    # # print(rd["^(?=.*" + key + ").*$"])
                    # print(hastest)
                    # print('-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')

            except IndexError:
                print('<Production Methods>')
                print('Error')
                nodetect += 1
                pass
            
            count += 1
        
        print('hastest : ' + str(hastest) + '(' + str(round(hastest/count*100,1)) + ')')
        print('notest : ' + str(notest)  + '(' + str(round(notest/count*100,1)) + ')')
        print('nodetect : ' + str(nodetect)  + '(' + str(round(nodetect/count*100,1)) + ')')
        print('Total : ' + str(count))

    # ClonePairwithOneTest()

    
    def ClonePairwithTwoTest():
        t = 't2'
        projectname = 'maven'

        # book = xlwt.Workbook()
        # sheet1 = book.add_sheet('sheet1')

        NicadTest = open(r'TestPath_' + t + '_' + projectname + '.txt','r',encoding="utf-8_sig")
        NicadTestPath = NicadTest.readlines()
        NtPath = [Ntline.replace('\n', '') for Ntline in NicadTestPath]
        cc = int(len(NtPath)/2)
        # print(cc)

        NicadFiles = defaultdict(list)
        c = 1
        for i in range(cc):
            NicadFiles['Clone Pairs ' + str(i+1)].append('C:/Users/ryosuke-ku/Desktop/SCRAPING/Method_Scraping/xml_scraping/NicadOutputFile_' + t + '_' + projectname + '/Clone Pairs ' + str(i+1) + '/Nicad_' + t + '_' + projectname + str(c) + '.java')
            c += 1
            NicadFiles['Clone Pairs ' + str(i+1)].append('C:/Users/ryosuke-ku/Desktop/SCRAPING/Method_Scraping/xml_scraping/NicadOutputFile_' + t + '_' + projectname + '/Clone Pairs ' + str(i+1) + '/Nicad_' + t + '_' + projectname + str(c) + '.java')
            c += 1
    
        # print(NicadFiles)

        tc1 = 0
        tc2 = 1
        nt = 0
        ot = 0
        tt = 0 
        excelnum = 0
        for x in NicadFiles:
            
            path1 = NicadFiles[x][0]
            path2 = NicadFiles[x][1]

            Productionmethods_list1 = AstProcessorProduction(None, BasicInfoListener()).execute(path1) #target_file_path(テストファイル)内のメソッド名をすべて取得
            Productionmethods_list2 = AstProcessorProduction(None, BasicInfoListener()).execute(path2) #target_file_path(テストファイル)内のメソッド名をすべて取得
            

            file = open(NicadFiles[x][0],'r')
            line1_1 = file.readline()
            line1_2 = file.readline()
            LINE1 = re.sub(r".*?:", "", line1_2)

            # print('① ' + Productionmethods_list1[0])

            Testmethodcalls1 = AstProcessorTestMethodCall(None, BasicInfoListener()).execute('C:/Users/ryosuke-ku/Desktop/NiCad-5.1/systems/' + NtPath[tc1])
            # print(Testmethodcalls1)

            cnt = 1
            methodmapcall1 = defaultdict(list)
            for k in Testmethodcalls1:
                for l in Testmethodcalls1[k]:
                    for m in l:
                        methodcall = str(cnt) + ':' + m
                        methodmapcall1[methodcall] = k
                        cnt+=1

            # print(methodmapcall1)
            tp1 = 'C:/Users/ryosuke-ku/Desktop/NiCad-5.1/systems/' + NtPath[tc1]

            rd = rdict(methodmapcall1)
            words = []
            reusetest1 = []
            try:
                key = Productionmethods_list1[0]
                retmethods = rd["^(?=.*" + key + ").*$"]
                # print(retmethods)
                if len(retmethods) == 0:
                    j1 = 0
                else: 
                    
                    for o in re.split('([a-z]+)([A-Z][a-z]+)|([A-Z][a-z]+)', Productionmethods_list1[0]):
                        if o != None and o != '':
                            words.append(o)
        
                    # print(words)
                    for i in words:
                        # print(i.lower())
                        for j in retmethods:
                            if i.lower() in j.lower():
                                reusetest1.append(j)
                            #     j1 = 1
                            # else:
                            #     j1 = 0
                        
                    if len(reusetest1) != 0:
                        j1 = 1
                    else:
                        j1 = 0

                rt1 = list(set(reusetest1))
                # print(rt1)
                # print(j1)
 

            except IndexError:
                # print('<Production Methods>')
                # print('Error')
                pass

            tc1 += 2

            file = open(NicadFiles[x][1],'r')
            line2_1 = file.readline()
            line2_2 = file.readline()
            LINE2 = re.sub(r".*?:", "", line2_2)

            # print('② ' + Productionmethods_list2[0])
            Testmethodcalls2 = AstProcessorTestMethodCall(None, BasicInfoListener()).execute('C:/Users/ryosuke-ku/Desktop/NiCad-5.1/systems/' + NtPath[tc2])

            cnt = 1
            methodmapcall2 = defaultdict(list)
            for k in Testmethodcalls2:
                for l in Testmethodcalls2[k]:
                    for m in l:
                        methodcall = str(cnt) + ':' + m
                        methodmapcall2[methodcall] = k
                        cnt+=1

            # print(methodmapcall2)

            tp2 = 'C:/Users/ryosuke-ku/Desktop/NiCad-5.1/systems/' + NtPath[tc2]
            rd = rdict(methodmapcall2)
            words2 = []
            reusetest2 = []
            try:
                key = Productionmethods_list2[0]
                retmethods2 = rd["^(?=.*" + key + ").*$"]
                # print(retmethods2)
                if len(retmethods2) == 0:
                    j2 = 0
                    # print('No Test')
                else:
                    # j2 = 1
                    # print('Has Test')
                    
                    for r in re.split('([a-z]+)([A-Z][a-z]+)|([A-Z][a-z]+)', Productionmethods_list2[0]):
                        if r != None and r != '':
                            words2.append(r)
                    #         print(o)
                    # print(words2)
                    for p in words2:
                        # print(i.lower())
                        for q in retmethods2:
                            if p.lower() in q.lower():
                                reusetest2.append(q)
                            #     j2 = 1
                            # else:
                            #     j2 = 0
                    if len(reusetest2) != 0:
                        j2 = 1
                    else:
                        j2 = 0
                rt2 = list(set(reusetest2))
                # print(rt2)
                # print(j2)
                    
            except IndexError:
                # print('<Production Methods>')
                # print('Error')
                pass
            
            # print('------------------------------------------------------------------------------------------------------------')

            tc2 += 2
            try:
                if j1 ==0 and j2 ==0:
                    nt += 1
                
                if j1 ==0 and j2 ==1:
                    # print('--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
                    # print(x)
                    # print('① ' + Productionmethods_list1[0])
                    # print('No Test')
                    # print('② ' + Productionmethods_list2[0])
                    # print('Has Test')
                    # print(line2_1[2:].replace('\n',''))
                    # print(line2_2[2:].replace('\n',''))
                    # print(tp2)
                    # print(retmethods2)
                    ot += 1
                
                if j1 ==1 and j2 ==0:
                    # print('--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
                    # print(x)
                    # print('① ' + Productionmethods_list1[0])
                    # print('Has Test')
                    # print(line1_1[2:].replace('\n',''))
                    # print(line1_2[2:].replace('\n',''))
                    # print(tp1)
                    # print(retmethods)
                    # print('② ' + Productionmethods_list2[0])
                    # print('No Test')
                    ot += 1
                
                if j1 ==1 and j2 ==1 and x!= 'Clone Pairs 47' and x!= 'Clone Pairs 61' and x!= 'Clone Pairs 127' and x!= 'Clone Pairs 129':
                    print('--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
                    print('<' + x + '>')
                    # sheet1.write(excelnum, 0, '<' + x + '>')
                    # similarity = line1_1[14:].replace('\n','')
                    # similarity2 = similarity[similarity.find(':')+1:]
                    # sheet1.write(excelnum, 1, similarity2[:similarity2.find(':')])
                    # sheet1.write(excelnum, 2, Productionmethods_list1[0])
                    # sheet1.write(excelnum, 3, Productionmethods_list2[0])
                    excelnum += 1
                    print('① ' + Productionmethods_list1[0])
                    print('Has Test')
                    print(line1_1[2:].replace('\n',''))
                    print('C:/Users/ryosuke-ku/Desktop/NiCad-5.1/systems/' + LINE1.replace('\n',''))
                    print(tp1)
                    # print(retmethods)
                    print(rt1)
                    print(len(rt1))
                    print('② ' + Productionmethods_list2[0])
                    print('Has Test')
                    print(line2_1[2:].replace('\n',''))
                    print('C:/Users/ryosuke-ku/Desktop/NiCad-5.1/systems/' + LINE2.replace('\n',''))
                    print(tp2)
                    # print(retmethods2)
                    print(rt2)
                    print(len(rt2))
                    tt += 1
                    
                
            except IndexError:
                pass

        print('--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
        print('onetest : ' + str(ot) + '(' + str(round(ot/(ot + nt + tt)*100,1)) + ')')
        print('notest : ' + str(nt)  + '(' + str(round(nt/(ot + nt + tt)*100,1)) + ')')
        print('twotest : ' + str(tt)  + '(' + str(round(tt/(ot + nt + tt)*100,1)) + ')')
        print('Total : ' + str(ot + nt + tt))
        # book.save('maven_t2.xls')

    ClonePairwithTwoTest()