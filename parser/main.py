from parser import *
import contries
import wikipedia
import time

start_time = time.time()

# Делаем список со всеми страницами википедии, которые надо запарсить
list_of_countries = [country for country in contries.__dict__.keys() if not country.startswith('_')]
data = pd.DataFrame(columns=['person', 'position', 'start_precision', 'start', 'end_precision', 'end'])

# Пробегаемся по всем странам
for country in list_of_countries:
    print(f"~~~~~~~~~parsing of {country}~~~~~~~~~")
    country_rullers_df = page_links(wikipedia.page(country))
    data = pd.concat([data, country_rullers_df])

# Приводим данные в приличный види и сохраняем
data.drop_duplicates(inplace=True)
data_clear = data[
    (data['start'] != 'нет данных') & (data['end'] != 'нет данных') & (data['start_precision'] != 'нет данных') & (
            data['end_precision'] != 'нет данных') & (data['position'] != 'нет данных')]
data_clear.to_csv('хакатон_дата_чистые.csv', index=False)

print("--- %s seconds ---" % (time.time() - start_time))
