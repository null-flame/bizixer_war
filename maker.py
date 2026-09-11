def make_invisible_text(text, count=300):
    # نویسه نامرئی (Zero-Width Non-Joiner)
    invisible_char = "\u200c"

    # ساخت رشته نامرئی با تعداد درخواستی
    padding = invisible_char * count

    # قرار دادن نویسه‌های نامرئی بین تمام حروف متن
    result = padding.join(text)

    # افزودن نویسه‌ها به ابتدا و انتهای متن
    return padding + result + padding


# متن ورودی
original_text = "سلاممم"

# اجرا با ۳۰۰ نویسه نامرئی بین هر کاراکتر
spammed_text = make_invisible_text(original_text, count=800)

# چاپ نتیجه
print(spammed_text)

# ذخیره در فایل (برای اینکه راحت کپی کنید)
with open("invisible_output.txt", "w", encoding="utf-8") as f:
    f.write(spammed_text)

print(
    f"\nمتن ساخته شد! طول واقعی متن خروجی: {len(spammed_text)} کاراکتر است."
)
