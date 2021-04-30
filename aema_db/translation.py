from modeltranslation.translator import translator, TranslationOptions
from mezzanine.pages.models import RichTextPage,Page
from mezzanine.blog.models import BlogPost


class PageTranslationOptions(TranslationOptions):
        fields = ('content',)

class BasicPageTranslationOptions(TranslationOptions):
        fields = ('title',)        
        
class BlogTranslationOptions(TranslationOptions):
        fields = ('content','title')


translator.register(Page,BasicPageTranslationOptions)        
translator.register(RichTextPage,PageTranslationOptions)


translator.register(BlogPost,BlogTranslationOptions)


