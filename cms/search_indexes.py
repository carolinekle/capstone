from haystack import indexes
from news.models import Article, Section, Author, Image


class ArticleIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Article

class SectionIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Section

class AuthorIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Author
    
class ImageIndex(indexes.SearchIndex, indexes.Indexable):
    text=indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Image