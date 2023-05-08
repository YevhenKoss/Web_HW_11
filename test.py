from datetime import datetime, timedelta

end_day = datetime.now() + timedelta(days=7)
current_day = datetime.now().date()
current_year = datetime.now().strftime("%Y")
end_day_str = end_day.strftime("%Y-%m-%d")

birthday = datetime(year=1989, month=5, day=8)
birthday_str = birthday.strftime("%Y-%m-%d")
birthday_str_new = birthday_str.replace(birthday.strftime("%Y"),  current_year)

birthday_str_new_dt = datetime.strptime(birthday_str_new, '%Y-%m-%d').date()


print(current_day <= birthday_str_new_dt <= end_day.date())
# contacts = db.query(Contact).all()
# for contact in contacts:
#     print((contact.date_of_birth.strftime("%m-%d")))