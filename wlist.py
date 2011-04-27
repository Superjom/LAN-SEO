#coding=gbk
class List(list):
    def __init__(self):
        '用于重复性儿分法的实验'
    def find(self,word):
        l=len(self)
        ll=hash(word)
        fir=0
        end=l-1

        if fir>end:
            #空
            self.insert(0,word)
            return False
        elif fir<end:
            #not empty, need to compare
            while fir<=end:
                mid=(fir+end)/2
                if hash(self[fir])>ll:
                    self.insert(fir,word)
                    return False
                if mid == l-1:
                    if hash(self[mid])>ll:
                        self.insert(mid,word)
                        return False
                    elif hash(self[mid])<ll:
                        self.insert(mid+1,word)
                        return False
                    else:
                        if self[mid]==word:
                            return True
                        else:
                            self.insert(mid+1,word)
                            return False
                        
                if hash(self[mid])>ll:
                    end=mid-1
                elif hash(self[mid])<ll:
                    fir=mid+1
                else:
                    if word == self[mid]:
                        return True
                        break
                    else:
                        #hashgth equals but word is different
                        fir=mid
                        end=mid
                        while fir>=0 and hash(self[fir])==ll:
                            if self[fir]==word:
                                return True
                                break
                            fir-=1
                        while end<l and hash(self[end])==ll:
                            if self[end]==word:
                                return True
                                break
                            end+=1
                        self.insert(mid+1,word)
                        return False
            if hash(self[fir])>ll:
                self.insert(fir,word)
                return False


        else:
            #self mid equal hashgth of word
            if self[fir]==word:
                return True
            elif hash(self[fir])>ll:
                self.insert(fir,word)
                return False
            else:
                self.insert(fir+1,word)
                return False

if __name__=='__main__':
    l=List()
    print l.find('1')
    print l.find('11')
    print l.find('2')
    print l.find('32123')
    print l.find('21234')
    print l.find('23')
    print l.find('231')
    while True:
        data=raw_input('...')
        print l.find(data)
        print l
        if(data=='111'):
            print l
            for i in l:
                print hash(i),i
        if(data=='000'):
            break





