from django.db import models
from django.urls import reverse

# Create your models here.
# 상품 카테고리
class Category(models.Model):
    # db_index로 인해서 카테고리 정보가 저장되는 테이블은 이 이름 열을 인덱스 열로 설정
    name = models.CharField(max_length=200, db_index = True)
    # SEO 최적화를 위한 기능
    meta_description = models.TextField(blank = True)
    slug = models.SlugField(max_length=200, db_index = True, unique = True,
        allow_unicode = True)
        
    class Meta:
        ordering = ['name']
        # 관리자 페이지에서 볼때 단수, 복수여부에 따라서 verbose_name, or plural
        verbose_name = 'category'
        verbose_name_plural = 'categories'
        
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shopping:product_in_category', args = [self.slug])
    
class Product(models.Model):
    # 1. 카테고리와 ForeignKey를 잡아주고
    # 2. on_delete에 models.SET_NULL을 잡아준 이유는, 카테고리가 지워지더라도 상품이 지워지는 건 아니기때문에
    category = models.ForeignKey(
        Category, on_delete= models.SET_NULL, null = True, related_name= 'products')
    name = models.CharField(max_length=150, db_index=True)
    slug = models.SlugField(max_length=150, db_index=True, unique=True, allow_unicode=True)

    image = models.ImageField(upload_to='products/%Y/%m/%d', blank = True)
    description = models.TextField(blank = True)
    meta_description = models.TextField(blank = True)
    
    price = models.DecimalField(max_digits=10, decimal_places = 2)
    stock = models.PositiveIntegerField()

    # 품절 등에 대해 대비하기 위한 available 시리즈
    available_display = models.BooleanField('Display', default = True)
    available_order = models.BooleanField('Order', default = True)
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    # 이건 색인, 즉 검색할때 사용하는 index이다.
    class Meta:
        ordering = ['-created']
        index_together = [['id', 'slug']]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shopping:product_detail', args = [self.id, self.slug])
    
