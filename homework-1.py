# Task 1
# Каждое из слов «разработка», «сокет», «декоратор» представить в строковом формате и
# проверить тип и содержание соответствующих переменных. Затем с помощью
# онлайн-конвертера преобразовать строковые представление в формат Unicode и также
# проверить тип и содержимое переменных.
SEPARATORS = '-' * 20
print(SEPARATORS + ' Task 1 ' + SEPARATORS)
words = (
    "разработка",
    "сокет",
    "декоратор",
)

words_unicode = (
    '\u0440\u0430\u0437\u0440\u0430\u0431\u043e\u0442\u043a\u0430',
    '\u0441\u043e\u043a\u0435\u0442',
    '\u0434\u0435\u043a\u043e\u0440\u0430\u0442\u043e\u0440',
)

for word, word_after_converting in zip(words, words_unicode):
    print(f'Word: {word},  type: {type(word)}, type key points string: {type(word_after_converting)}')

# Task 2
# Каждое из слов «class», «function», «method» записать в байтовом типе без преобразования в
# последовательность кодов (не используя методы encode и decode) и определить тип,
# содержимое и длину соответствующих переменных.
print(SEPARATORS + ' Task 2 ' + SEPARATORS)
words = ("class", "function", "method")

for idx, word in enumerate(words):
    bytes_w = bytes(word, 'utf-8')
    print(f'{SEPARATORS[:10]} {idx + 1} {SEPARATORS[:10]}\n'
          f'Word before converting: {word}, type {type(word)}\n'
          f'Word after converting: {bytes_w}, type: {type(bytes_w)}\n')

# Task 3
# Определить, какие из слов «attribute», «класс», «функция», «type» невозможно записать в
# байтовом типе.
print(SEPARATORS + ' Task 3 ' + SEPARATORS)

words = ("attribute", "класс", "функция", "type")
for word in words:
    try:
        bytes(word, 'ascii')
    except UnicodeEncodeError:
        print(f"Word '{word}' can't convert to bytes with coding ASCII")

# Task 4
# Преобразовать слова «разработка», «администрирование», «protocol», «standard» из
# строкового представления в байтовое и выполнить обратное преобразование (используя
# методы encode и decode).

print(SEPARATORS + ' Task 4 ' + SEPARATORS)

words = (
    "разработка",
    "администрирование",
    "protocol",
    "standard"
)

for word in words:
    encoded_word = word.encode('UTF-8')
    decoded_word = encoded_word.decode('UTF-8')
    print(f"Word : '{word}'\n"
          f"Word after encode : '{encoded_word}'\n"
          f"Word after decoded : {decoded_word}\n")
    assert word == decoded_word

# Task 5
# Выполнить пинг веб-ресурсов yandex.ru, youtube.com и преобразовать результаты из
# байтовового в строковый тип на кириллице.
import multiprocessing
import subprocess

print(SEPARATORS + ' Task 5 ' + SEPARATORS)

web_sites = (
    "yandex.ru",
    "youtube.com",
)


def ping_and_decode(url):
    response = subprocess.run(['ping', '-c', '3', '-w', '3',  url], stdout=subprocess.PIPE)
    decoded_result = response.stdout.decode('cp1251')  # декодируем байты в строку на кириллице
    return decoded_result


def ping_websites(sites):
    with multiprocessing.Pool(processes=len(sites)) as pool:
        results = pool.map(ping_and_decode, sites)
    return results


results = ping_websites(web_sites)

for result in results:
    print(result)

# Task 6
# Создать текстовый файл test_file.txt, заполнить его тремя строками: «сетевое
# программирование», «сокет», «декоратор». Проверить кодировку файла по умолчанию.
# Принудительно открыть файл в формате Unicode и вывести его содержимое.

print(SEPARATORS + ' Task 6 ' + SEPARATORS)
words = (
    "сетевое программирование\n",
    "сокет\n",
    "декоратор\n",
)
with open('test_file.txt', 'w') as f:
    f.writelines(words)

with open('test_file.txt', 'r') as f:
    print(f'File encoding: {f.encoding}\n'
          f'File content:\n {f.read()}')
