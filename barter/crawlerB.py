import urllib.request
from bs4 import BeautifulSoup
import os
import MySQLdb
from datetime import datetime
from unidecode import unidecode


class crawlB:
    
    def __init__(self):
        
        self.user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
        self.req_headers = {'User-Agent':self.user_agent,}
        self.base_path = '/home/binnyabraham/workspace/crawl/'
        self.image_path = '/home/binnyabraham/workspace/xchange/barter/static/barter/images/downloads/'
        self.image_base_url = '/static/barter/images/downloads/'
        self.base_url = 'http://www.expatriates.com'
        self.db_credentials = {'NAME':'db_xchange', 'USER':'root', 'PASSWORD':'nonu@123', 'HOST':'127.0.0.1'}
        
    def connect_to_db(self, sql_query, qtype):
        
        db_conn = MySQLdb.connect(host=self.db_credentials['HOST'], user=self.db_credentials['USER'], passwd=self.db_credentials['PASSWORD'],
                                     db=self.db_credentials['NAME'])
        db_cursor = db_conn.cursor()
        db_cursor.execute(sql_query)
        if(qtype == 'select'):
            db_data = db_cursor.fetchall()
            return db_data
        
        db_conn.commit()
        

    def fetch_url(self, url):
        
        req = urllib.request.Request(url, None,  self.req_headers) #The assembled request
        resp = urllib.request.urlopen(req)
        data = resp.read()
        return data
    
    
    def parse_url(self, url):
        
        resp_main_data = self.fetch_url(url)
        main_soup = BeautifulSoup(resp_main_data)
        
        for divs in main_soup.find_all("div", { "class" : "category-box" }):
            for link in divs.find_all('a'):
                sec_url = self.base_url + link.get('href')
                resp_sec_data = self.fetch_url(sec_url)
                sec_soup = BeautifulSoup(resp_sec_data)
                for uls in sec_soup.find_all("ul", { "class" : "listing-content" }):
                    for sec_link in uls.find_all('a'):
                        sec_href = sec_link.get('href')
                        if (sec_href):
                            file_name = sec_href.split('/')[-1]
                            final_url = self.base_url + sec_href
                            print (final_url)
                            try:
                                final_data = self.fetch_url(final_url)
                                if file_name:
                                    file_path = self.base_path + file_name
                                    self.write_to_file(file_path, final_data)
                                    print (file_path)
                            except:
                                print ("Error in fetch url")
                                pass
        
    def write_to_file(self, file_path, data):
        file = open(file_path, "wb")
        file.write(data)
        file.close()


    def read_file(self, file_path):
        file = open(file_path, "rb")
        file_data = file.read()
        file.close()
        return file_data
        
    
    def parse_data(self, data):
        soup = BeautifulSoup(data)
        data_dct = {}
        try:
            for lis in soup.find("ul", {"class":"no-bullet"}).find_all('li'):
                try:
                    data_dct[lis.text.split(':')[0].strip()] = self.str_decode(lis.text.split(':')[1].strip())
                except Exception:
                    pass
            
            count = 0
            for bread in soup.find("ul", {"class":"breadcrumbs"}).find_all('li'):
                bread_crumb = self.str_decode(bread.find('a').text)
                if count == 1:
                    data_dct['Type'] =  bread_crumb
                elif count == 2:
                    data_dct['Country'] = bread_crumb
                elif count == 3:
                    data_dct['Main_category'] = bread_crumb
                elif count == 4:
                    data_dct['Category'] = bread_crumb
                count += 1
            try:
                data_dct['Main_title'] = self.str_decode(soup.find("div", {"class":"page-title"}).find('h1').text.replace('"','').strip())
            except:
                data_dct['Main_title'] = ''
            try:
                data_dct['Phone'] = self.str_decode(soup.find("button", {"class":"btn big primary posting-phone"}).find('a').text.strip())
            except:
                data_dct['Phone'] = ''
            try:
                data_dct['Desc'] = self.str_decode(soup.find("div", {"class":"post-body"}).text.replace('"',' ').strip())
            except:
                data_dct['Desc'] = ''
            
            data_dct['Img_url_vendor'] = [] 
            for img in soup.find("div", {"class":"posting-images top-margin"}).find_all('img'):
                try:
                    data_dct['Img_url_vendor'].append(self.base_url+img.attrs['src'].strip())
                except:
                    pass
                
            data_dct['Subregion'] = ''
            split_region = data_dct['Region'].split('(')
            if len(split_region)>1:
                data_dct['Subregion'] = self.str_decode(split_region[1].split(')')[0].strip())
            
            data_dct['Region'] = split_region[0].strip()
                
        except:
            pass
        return data_dct
    
            
    def populate_data(self):
        path = self.base_path
        dir_lst = os.listdir(path)
        for file in dir_lst:
            file_path = self.base_path + file
            data = self.read_file(file_path)
            data_dct = self.parse_data(data)
            sql_query = self.prepare_sql(data_dct)
            print (sql_query)
            if(sql_query):
                self.db_storage(sql_query, 'insert')
        
        
    def prepare_sql(self, data_dct):
        
        print (data_dct)
        if(data_dct):
            to_date = datetime.today()
            pub_date = datetime.strptime(data_dct['Date'], '%A, %B %d, %Y')
            inter_flag = False 
            if data_dct['Type'].lower().strip() == 'international':
                inter_flag = True
                
            query = """insert into barter_xchangestore (`main_title`, `category`, `main_category`, `country`, `region`, `sub_region`, `phone_num`, \
    `desc`, `image_url_vendor`, `is_international`, `active`, `pub_date`, `created_date`, `modified_date`) values ("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", \
    "%s", %s, %s, "%s", "%s", "%s");""" %(data_dct.get('Main_title',''), data_dct.get('Category',''), data_dct.get('Main_category',''), data_dct.get('Country',''), 
                              data_dct.get('Region',''), data_dct.get('Subregion',''), data_dct.get('Phone',''), data_dct.get('Desc',''), 
                              data_dct.get('Img_url_vendor',''), inter_flag, True, pub_date, to_date, to_date)
            return query
        else:
            return False
    
            
    def db_storage(self, sql_query, qtype):
        try:
            return self.connect_to_db(sql_query, qtype)
        except:
            print ('Insertion Error')
            
    
    def process_image_url(self):
        query = 'select image_url_vendor, id from barter_xchangestore where image_url is NULL;'
        data_row = self.db_storage(query, 'select')
        for rows in data_row:
            img_count = 1
            img_url_lst = []
            row_id = rows[1]
            for img in eval(rows[0]):
                img_file = str(img_count) + '.jpg'
                file_name = self.image_path + str(row_id) + '.' + img_file
                img_count +=1
                try:
                    img_data = self.fetch_url(img)
                    self.write_to_file(file_name, img_data)
                    img_url_lst.append(self.image_base_url + str(row_id) + '.' + img_file)
                except:
                    pass
            print (img_url_lst)
            img_query = 'update barter_xchangestore set image_url = "%s" where id = %s' % (img_url_lst, row_id)
            self.db_storage(img_query, 'update')
        
        
    def str_decode(self, strg):
        return unidecode(strg)
    
    
if __name__ == '__main__':
    
    url = "http://www.expatriates.com/classifieds/bhr/"
    cb = crawlB()
    print (cb.process_image_url())
    
    