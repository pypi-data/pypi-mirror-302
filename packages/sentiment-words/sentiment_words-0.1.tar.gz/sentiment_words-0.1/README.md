# sentiment_words_arabic.py

مكتبة الكلمات الإيجابية والسلبية.

## كيفية الاستخدام

```python
from sentiment_words_arabic.py import add_positive_word, remove_positive_word, count_sentiment_words

# إضافة كلمة إيجابية
add_positive_word('كلمة جديدة')

# حساب عدد الكلمات الإيجابية والسلبية في نص
positive_count, negative_count = count_sentiment_words("هذا نص إيجابي رائع")
print(f"عدد الكلمات الإيجابية: {positive_count}, عدد الكلمات السلبية: {negative_count}")
