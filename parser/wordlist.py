#coding=gb2312
#import sys
#reload(sys)
#sys.setdefaultencoding('utf-8')


class wordList(list):
#����ʻ�  ͨ��find����  ��word��hash��˳����list��
#�Զ��ַ�����
#�������true  �����ͨ���˴ʻ��hash ����word����hit�������Ϣ
#��Ϊlist ���Ա��߳�ʹ��
#Ϊ�˷�ֹ�ظ�,�����˶��ظ����ʵĴ���
#��Ҫ��hash��������� 
#�����ظ����ʵĽ�������� ���Լ���������ڵ�һ�ű����ظ��ģ������ڵڶ��ű���ʹ��ͬ���ķ������д���
#��Щ������ǿ���ѹ����һ���
#���ظ��ʻ�Ĵ���ʽ��
#���ö��ַ�   ����ѯ��start ���� end ��hashֵ�� word���ʱ����ָ����Ӧ��ǰ������ƶ���ֱ��ȷ�������ձ߽硣
#����β��ȷ���˱߽���ڽ������ٲ�ѯ
    def find(self,word):
        #print word
        l=len(self)
        first=0
        end=l-1
        mid=0
        num=hash(word)  #the word's hash
        if l==0:
            self.insert(0,word)
            return False
        while first<end:
            #while ��Ŀ�ģ� ȷ���߽�
            mid=(first+end)/2
            if num>hash(self[mid]):
                first=mid+1
            elif num<hash(self[mid]):
                end=mid-1
            else:
                #hashֵ���
                #mid ��hashֵ���
                #��ʼ����ȷ��first��end
                first=mid
                end=mid
                while hash(self[first])==num and first>=0:
                    #��ǰ��չ����
                    if self[first]==word:
                        return True
                    first-=1

                while hash(self[end])==num and end<l:
                    #�����չ����
                    if self[end]==word:
                        return True 
                    end=end+1

                self.insert(mid+1,word)
                return False
            
        if first==end:
            if hash(self[first])>num:
                self.insert(first,word)
                return False
            elif hash(self[first])<num:
                self.insert(first+1,word)
                return False
            else:
                #hashֵ��� ����Ҳ��word�������
                if self[first]==word:
                    #hashֵ��� �Ҵʻ�Ҳ���
                    return True
                else:
                    #hashֵ��� ���Ǵʲ����
                    # ?ֻ���ڴ�һ��hashֵ��  ��� ֻ��Ҫ�����´�
                    self.insert(first+1,word)
                    return False

        elif first>end:
            self.insert(first,word)
            return False
        else:
            return True

if __name__=='__main__':
    print 'begin to add world'
    word=wordList()
    print 'hello',hash('hello')
    print 'world',hash('world')
    print '���',hash('���')
    print 'he',hash('he')
    print 'wold',hash('wold')

    word.find('hello')
    word.find('world')
    word.find('���')
    word.find('he')
    word.find('wold')
    print word
    while True:
        inword=raw_input('input>>')
        if inword=='000':
            break
        elif inword=='111':
            for i in word:
                print hash(i),i
        else:
            word.find(inword)
            print 'the word is here'
            print word
    print 'hello'
    print 'hello'
