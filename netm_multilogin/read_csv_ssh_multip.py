
import json
import csv
import multiprocessing as mp


class SeeItAutomate():
    def __init(self):
        self.ip = ''
        self.vendor = ''
        self.mp_queue = mp.Queue()
        self.processes = []
        self.p = mp
        self.return_data = {}

    def printresults(self,ip,vendor):
        show_version = 'This device ip is '
        identifier = '{ip} : {vendor}'.format(ip,vendor)
        self.return_data[identifier] = (True,show_version)
        self.mp_queue.put(identifier)
        
    def main(self):
        open_f = open('Enterprise_Access_Switch_Descriptions.csv') # a simple list of IP addresses you want to connect to each one on a new line 
        reader = csv.DictReader(open_f)
        ip_add_d = {}

        for row in reader:
            #print(row['IP_Address'],row['Vendor'])
            ip_add_d.setdefault(row['IP_Address'],[]).append(row['Vendor'])
            multi_p = self.p.Process(target=self.printresults,args=(row['IP_Address'],row['Vendor']))
            self.processes.append(multi_p)
            multi_p.start()

            #ip_add_d[row['IP_Address']] += row['Vendor']
        results = []
        for p in self.processes:
            results.append(self.mp_queue.get())
        print(results)
        open_f.close()


        if __name__ == '__main__':
     
            main()

a= SeeItAutomate()