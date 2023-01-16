# TrendyolReviewsSentimentAnalysis

Trendyol ürün yorumlarının duygusal analizi projesi.

Dataset Adımları:
- Öncelikle Selenium kütüphanesi ile web-scraping işlemi yapılıp bir ürüne ait yorumlar comments.csv dosyasına yazılmıştır. Bu üründe 111 adet yorum vardır. Uygulanan modellerin başarısının kıyaslanması için az yorum sayısına ait bir ürün seçilmiştir. En yüksek başarıya sahip model daha sonra 1479 adet yoruma sahip başka bir ürüne uygulanmıştır.
- Ürüne verilen yıldız sayıları da web-scraping işlemi ile 'STARS' sütununa yazılmıştır.
- Denemeler sırasında büyük-küçük harf durumunun model başarısını etkilediği görülüp bütün yorumlar küçük harfe çevrilmiştir.

Model Adımları:
- Türkçe halihazırda NLP adımlarının zor olduğu bir dildir. Üstüne kullanıcıların yorum yazarken günlük dilde yazıp çok fazla yazım yanlışı yapması NLP adımlarını hayli zorlaştırmaktadır. 
- Bu sebeple Türkçe yorumları İngilizce'ye çevirerek analize devam etme yoluna gidilmiştir.
- 2 farklı Translator kütüphanesi kullanılıp elde edilen İngilizce yorumlar 'Englsih Comments' ve 'English Comments 2' sütunları olarak csv dosyasına eklenmiştir.
- from deep_translator import GoogleTranslator kütüphanesi ile çevrilen yorumların daha başarılı olduğu hem manuel kontrol ile hem modeller uygulandıktan sonraki başarı oranının kontrolü ile tespit edilmiştir.
- Daha sonra İngilizce yorumlara 'Vader' ve 'Bert' modeller uygulanmıştır. Uygulanırken hazır modeller kullanılmıştır.
- Vader Model -1(negatif),1(pozitif) arasında değer döndürmektedir.
- - Model sonucunda dönen değerler 0'dan büyükse pozitif, 0'dan küçükse negatif, 0'a eşitse nötr etiketi atanmıştır.
- - Atanan etiketler ile ürüne verilen yıldız sayıları karşılaştırılmış ve 'Vader Model Status' sütununa yazılmıştır.
- - İlk Translator kütüphanesi ile çevrilmiş yorumların sonuçları: 

![Vader Result](https://user-images.githubusercontent.com/87414202/212744256-ca1ff373-e7dc-4183-9506-13041a030853.png)
- - İkinci Translator kütüphanesi ile çevrilmiş yorumların sonuçları:

![Vader Result 2](https://user-images.githubusercontent.com/87414202/212744347-74607607-1202-4071-a7c7-c0885f7a1fda.png)

- Bert Model ise 3 değer döndürüp bunlar negatif-nötr-pozitif kutpu ifade etmektedir. Bu kutuplar 'Polarity' sütununa eklenmiştir.
- Pozitif-nötr-negatif kutup değerlerinden hangisi en büyükse ona kendi ismi etiket olarak atanıp yeni sütuna eklenmiştir.
- Daha sonra bu etiketler ile ürüne verilen yıldız sayıları karşılaştırılıp 'Roberta Model Status' sütunun olarak eklemiştir.
- - İlk Translator kütüphanesi ile çevrilmiş yorumların sonuçları: 

![Roberta Result](https://user-images.githubusercontent.com/87414202/212745483-5ab3afce-2ed0-4b3a-9ae0-a0d0cf8c0093.png)
- - İkinci Translator kütüphanesi ile çevrilmiş yorumların sonuçları: 

![Vader Result 2](https://user-images.githubusercontent.com/87414202/212745566-5bd6d64c-e55b-47ea-af03-d8bbc4240a2b.png)

