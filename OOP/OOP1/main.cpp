#include <iostream>
using namespace std;

class MyString {

public:
    MyString() : lenString(0) { data = nullptr; }

    explicit MyString(char *s) {
        lenString = strlen(s);
        data = new char[lenString + 1];
        strcpy(data, s);
    }

    explicit MyString(size_t lenStr) : lenString(lenStr) {
        if (lenString > 20) {
            cout << "***Вы страшно не правы, по заднию размер строчки не  должен превышать < 20***" << endl << endl;
            data = new char[0];
            lenString = 0;
            return;
        }
        else data = randomText(lenStr);
    }

    MyString(const MyString &object) {
        lenString = strlen(object.data);
        data = new char[lenString + 1];
        strcpy(data, object.data);
    }

    size_t getLenString() {
        lenString = strlen(data);
        return (lenString);
    }

    bool operator>(const MyString &object) const {
        return strcmp(data, object.data) > 0;
    }

    bool operator<(const MyString &object) const {
        return strcmp(data, object.data) < 0;
    };

     MyString& operator=(const MyString &object) {
        delete[] data;
        lenString = strlen(object.data);
        data = new char[lenString + 1];
        strcpy(data, object.data);
        return *this;
    }

     MyString& operator=(char *b) {
        delete[] data;
        lenString = strlen(data);
        data = new char[lenString + 1];
        strcpy(data, b);
        return *this;
    }


    // destructor
    ~MyString() { delete[] data; }

    friend ostream& operator<<(ostream& stream, const MyString& object);

private:
    char* data;
    size_t lenString;

     char* randomText (size_t len) {
            data = new char[len + 1];
            for (int i = 0; i < len; i++)
                data[i] = (char)('a' + rand() % 26);
            data[len] = '\0';
            return data;
        }
};

ostream& operator<<(ostream& stream, const MyString& object) {
    return stream << object.data << endl;
}

class MyStringArray {
private:
    MyString *arr;
    size_t size;

public:
    explicit MyStringArray (size_t len) : size(len) {
        if (len <= 50) {
            arr = new MyString[len];
            for(int i = 0; i < len; i++) {
                arr[i] = MyString(static_cast<size_t>(rand() % 20 + 1));
            }
        }
        else cout << "Вы страшно не правы" << endl;
    }

     ~MyStringArray() {
        delete[] arr;
    }

    void sort_len()
    {
        std::sort(arr, arr+size, [](MyString& a, MyString& b) { return a.getLenString() < b.getLenString(); });
    }

    void sort() {

        std::sort(arr,arr+size);
    }


    MyString& operator[](int i) {
        return arr[i];
    }

    friend ostream& operator<<(ostream &stream, MyStringArray &b)
    {
        for (int i = 0; i < b.size; i++) {
            stream << b.arr[i];
        }
        return stream;
    };

};

int main() {
    srand(static_cast<unsigned int>(time(nullptr)));
    MyString str(20);
    MyStringArray arrStr(10);
    //MyString str2(40);

    /*
    MyString test(d);
    cout << test;
     */

    cout << "Рандомная динамическая строчка" << endl;
    cout << str << endl;

    cout << "Массив динамический cтрочек" << endl;
    cout << arrStr << endl;

    //cout << str2;

    arrStr.sort();
    cout <<  "Отсортированный  массив динамических строчек по алфовиту" << endl;
    cout << arrStr << endl;

    arrStr.sort_len();
    cout <<  "Отсортированный по длине динамический массив" << endl;
    cout << arrStr << endl;


    return 0;
}