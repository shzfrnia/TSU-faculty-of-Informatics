# Chain of responsibility (Цепочка обязанностей)
Позволяет избежать жесткой зависимости отправителя запроса от его получателя, при этом запрос начинает обрабатываться одним из нескольких объектов. Объекты-обработчики связываются в цепочку, и запрос передается по цепочке, пока кокой-то объекта его не обработает.
## Принцип применения
![Принцип](https://github.com/shzfrnia/TSU-faculty-of-Informatics/blob/master/Object-oriented%20analysis%20and%20design/pattern-chain-of-responsibility/app/static/example.png)
Знает язык - переводит и возвращает ответ. Не знает - передает следующему объекту(переводчику). И так до тех пор, пока не встретит либо терминальный объект _(последний обработчик, который, как правило, сообщает об ошибке обработки запроса)_ либо попросту запрос теряется.
 ## <span style="color:#a94442">Важное допущение!</span>
У меня нет достаточно времени и ресурсов, чтобы написать определитель языка. Поэтому я использую библиотечную функцию. По хорошему для каждого объекта-обработчика должен быть свой механизм определения языка.
