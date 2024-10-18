#__init__.py
from text import CodeLibraryText
class CodeLibrary:
    
    
    def __init__(self):
        self.cdt = CodeLibraryText()  # Use self to make it an instance attribute
        pass

    def kmeans(self):
        print(self.cdt.kmeans)
        
    def apriori(self):
        print(self.cdt.apriori)

    def pagerank(self):
        print(self.cdt.pagerank)
        
    def fptree(self):
        print(self.cdt.fptree)
        
    def id3(self):
        print(self.cdt.id3)
        
    def naivebayes(self):
        print(self.cdt.naivebayes)



