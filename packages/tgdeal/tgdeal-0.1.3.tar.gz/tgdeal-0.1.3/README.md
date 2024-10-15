## Описание

`tgdeal` — это Python-пакет, предоставляющий полноценный API-клиент для работы с B2B API сервиса. Предназначен для
использования как конечными пользователями, так и партнерскими сервисами.
<br>
<br>

## Установка

Вы можете установить этот пакет с помощью pip:

Для Windows:

```bash
pip install tgdeal
```

Для Linux:

```bash
pip3 install tgdeal
```


# Пример использования

Ниже приведены примеры использования различных функций, доступных в пакете `tgdeal`.


> **Все функции, доступные в пакете `tgdeal`, имеют внутрикодовую документацию, пажалуйста ознакомьтесь с ней, а также с
документацией изложенной на апи ресурсах. [Документация](https://api.tgdeal.net/b2b/docs)**


## Инициализация клиента

Для начала работы необходимо инициализировать клиент:

```python
from tgdeal.client import ApiClient

tgdeal_api = ApiClient()
tgdeal_api.initialize()

```


## Пользовательская часть

### **Получение профиля**

```python
import asyncio

API_KEY = "YOUR API KEY"


async def main():
    await tgdeal_api.endpoints.users.get_profile(
        query_user_api_key=API_KEY
    )  # tgdeal_api.endpoints.users.ProfileRead

    """
    example output:
    {
           "id": 2,
           "balance": 0,
           "total_earned": 156,
           "total_rent_workers": 0,
           "total_sold_in_30_days": 4,
           "total_sold_in_ever": 6,
           "total_hold_items": 0,
           "total_hold_balance": 0,
           "boost_level": 1,
           "boost_in_percent": 0,
           "statistic_at": "2024-09-23T07:17:20.699527Z"
    }
    """


asyncio.run(main())
```

<br>
<br>

### **Загрузка данных**

> **Метод загрузки файлов .session +.json(если имеются)**

```python
import asyncio
from tgdeal.lib.helpers import find_and_convert_session_files

API_KEY = "YOUR API KEY"


async def main():
    sessions = await find_and_convert_session_files(
        path="DIR",
        only_with_json=False  # Optional
    )

    await tgdeal_api.endpoints.users.send_strings(
        query_user_api_key=API_KEY,
        body_default_parameters=tgdeal_api.endpoints.users.Parameters(
            app_id=...,
            app_hash=...,
            device_model=...,
            # ...(Остальные параметры)

        ),  # Optional
        query_upload_type="SELL",
        body_sessions=sessions,
    )
    # tgdeal_api.endpoints.users.UploadRead


asyncio.run(main())
```

<br>
<br>

> **Метод загрузки telethon string сессий**

```python
import asyncio
from telethon import TelegramClient

API_KEY = "YOUR API KEY"


async def main():
    your_string_sessions = ["1AZ...", "1BZ..."]

    sessions = [
        tgdeal_api.endpoints.users.InputSession(
            string=string,
            parameters=None  # Optional - tgdeal_api.endpoints.users.Parameters(...)
        ) for string in your_string_sessions
    ]

    await tgdeal_api.endpoints.users.send_strings(
        query_user_api_key=API_KEY,
        body_default_parameters=tgdeal_api.endpoints.users.Parameters(
            app_id=...,
            app_hash=...,
            device_model=...,
            # ...(Остальные параметры)

        ),  # Optional
        query_upload_type="SELL",
        body_sessions=sessions,
    )
    # tgdeal_api.endpoints.users.UploadRead


asyncio.run(main())
```

<br>
<br>

### **История загрузок**

```python
import asyncio

API_KEY = "YOUR API KEY"


async def main():
     history = await tgdeal_api.endpoints.user.find_many_uploads(
          query_user_api_key=API_KEY,
          # Optional args:
          query_upload_type=...,
          query_upload_from=...,
          query_offset=...,
          query_limit=...,
          query_order_direction=...,
          query_order_by=...,
          query_start_date=...,
          query_end_date=...,
     )
     # tgdeal_api.endpoints.users.UploadsPaginated
     """
     example output:
     {
            "total": 1,
            "data": [
                    {
                     "id": 128,
                     "from_bot": true,
                     "from_api": false,
                     "user_id": 2,
                     "upload_rent_reauth": false,
                     "upload_app_id": 2496,
                     "upload_type": "SELL",
                     "counts": { 
                         "total": 62,"checking": 0,"invalid": 62, "received": 0, "duplicate": 0,
                         "hold": 0, "passed": 0, "free_income": 0,   "hold_income": 0
                     },
                     "done": true,
                     "cancelled": false,
                     "updated_at": "2024-09-14T12:35:08.535000Z",
                     "created_at": "2024-09-14T12:34:34.103000Z"
                   },
                ),
                ...
            ]
     }
     """


asyncio.run(main())
```

<br>
<br>

### **Поиск загрузки по ID**

```python
import asyncio

API_KEY = "YOUR API KEY"


async def main():
    item = await tgdeal_api.endpoints.users.find_one_upload(
        query_user_api_key=API_KEY,
        path_upload_id=...,

    )
    # tgdeal_api.endpoints.users.UploadRead
    """
    example output:
    {
          "id": 128,
          "from_bot": true,
          "from_api": false,
          "user_id": 2,
          "upload_rent_reauth": false,
          "upload_app_id": 2496,
          "upload_type": "SELL",
          "counts": { 
              "total": 62,"checking": 0,"invalid": 62, "received": 0, "duplicate": 0,
              "hold": 0, "passed": 0, "free_income": 0,   "hold_income": 0
          },
          "done": true,
          "cancelled": false,
          "updated_at": "2024-09-14T12:35:08.535000Z",
          "created_at": "2024-09-14T12:34:34.103000Z"
    }  
    """


asyncio.run(main())
```

<br>
<br>

### **Запрос выплаты**

> **Существует два типа запроса. "new" и "id"**
> 1. new - могут создать пользователи, не запускавшие бота (флаг `bot_initialized` в UserRead). То есть, созданные
     партнер-сервсом самостоятельно. В целях
     безопасности, после запуска бот-сервиса запрос по новым реквизитам будет запрещен.
> 2. id - В реквизитах нужно указать айди ранее созданной пользователем выплаты. Для получения истории
     воспользуйтесь `tgdeal_api.endpoints.user.find_many_withdrawals`

```python
import asyncio

API_KEY = "YOUR API KEY"


async def main():
    # Получаем доступные методы (для ознакомления)
    available_methods = await tgdeal_api.endpoints.system.get_available_withdrawal_methods()
    """
    example output:
    {
           "USDT_TON": {"stable_fee": 0, "percent_fee": 2},
           "LOLZ": {"stable_fee": 0, "percent_fee": 2}
    }
    """

    # Делаем предварительный подсчет (для ознакомления)
    count_req = await tgdeal_api.endpoints.users.count_withdrawal(
        query_user_api_key=API_KEY,
        body_method="LOLZ",  # Один из доступных
        body_requisite="TeleDealer",
        body_requisite_type="new"
    )
    # tgdeal_api.endpoints.users.WithdrawalCount
    """
    example output:
    {
           "input_value": 100,
           "output_value": 98,
           "method": "LOLZ",
           "requisite": "TeleDealer"
    }
    """

    # Запрашиваем выплату с теми же данными
    await tgdeal_api.endpoints.users.create_withdrawal(
        query_user_api_key=API_KEY,
        body_method="LOLZ",  # Один из доступных
        body_requisite="TeleDealer",
        body_requisite_type="new"
    )
    # tgdeal_api.endpoints.users.WithdrawalRead
    """
    example output:
    {
          "id": 12,
          "input_value": 100,
          "output_value": 98,
          "method": "LOLZ",
          "requisite": "TeleDealer",
          "status": "WAITING",
          "paid_at": null,
          "cancelled_at": null,
          "created_at": "2024-09-17T11:27:47.960000Z"
    }
    """


asyncio.run(main())
```

<br>
<br>

### **История выплат**

```python
import asyncio

API_KEY = "YOUR API KEY"


async def main():
    history = await tgdeal_api.endpoints.user.find_many_withdrawals(
        query_user_api_key=API_KEY,
        # Optional args:
        query_status=...,
        query_method=...,
        query_requisite=...,
        query_offset=...,
        query_limit=...,
        query_order_direction=...,
        query_order_by=...,
        query_start_date=...,
        query_end_date=...,
    )
    # tgdeal_api.endpoints.users.WithdrawalRead
    """
    example output:
    {
           "total": 1,
           "data": [
               {
                   "id": 12,
                   "input_value": 100,
                   "output_value": 98,
                   "method": "LOLZ",
                   "requisite": ...,
                   "status": "WAITING",
                   "paid_at": null,
                   "cancelled_at": null,
                   "created_at": "2024-09-17T11:27:47.960000Z"
               },
               ...
           ]
    }
    """


asyncio.run(main())
```

<br>
<br>

### **Поиск выплаты по ID**

```python
import asyncio

API_KEY = "YOUR API KEY"


async def main():
    item = await tgdeal_api.endpoints.users.find_one_withdrawal(
        query_user_api_key=API_KEY,
        path_withdrawal_id=...,

    )
    # tgdeal_api.endpoints.users.WithdrawalRead
    """
    example output:
    {
             "id": 12,
             "input_value": 100,
             "output_value": 98,
             "method": "LOLZ",
             "requisite": ...,
             "status": "WAITING",
             "paid_at": null,
             "cancelled_at": null,
             "created_at": "2024-09-17T11:27:47.960000Z"
    }
    """


asyncio.run(main())
```

<br>
<br>
<br>

## Партнер-сервис часть

<br>

### **Получение информации о сервисе**

```python
import asyncio

API_KEY = "YOUR SERVICE API KEY"


async def main():
    await tgdeal_api.endpoints.system.get_bot_profile(
        query_bot_api_key=API_KEY
    )  # tgdeal_api.endpoints.system.BotProfileRead

    """
    example output:
    {
           "id": 24,
           "balance": 0,
           "total_earned": 10256,
           "rev_share_percent": 80,
           "total_users": 623,
           "total_active_users": 324,
           "boost_level": 4,
           "boost_in_percent": 20,
           "statistic_at": "2024-09-23T07:17:20.699527Z"
    }
    """


asyncio.run(main())
```

<br>
<br>

### **Получение профиля пользователя**

```python
import asyncio

API_KEY = "YOUR SERVICE API KEY"


async def main():
    await tgdeal_api.endpoints.system.get_user(
        query_bot_api_key=API_KEY,
        query_user_telegram_id=832953402  # USER TG ID
    )  # tgdeal_api.endpoints.system.UserRead

    """
    example output:
    {
      "id": 1,
      "balance": ...,
      "language": "en",
      "telegram_id": 832953402,
      "full_name": ...,
      "username": ...,
      "api_token": "string_value",
      "bot_initialized": true
    }
    """


asyncio.run(main())
```

<br>
<br>

### **Создание пользователя через апи**

> Вы можете создать пользователя в своем парнер-сервисе самостоятельно, ему не обязательно запускать вашего бота. Также
> это обозначает, что вы сможете заказывать выплаты на любые реквизиты.

```python
import asyncio

API_KEY = "YOUR SERVICE API KEY"


async def main():
    await tgdeal_api.endpoints.system.create_user(
        query_bot_api_key=API_KEY,
        body_telegram_id=...,
        # Optional args:
        body_language=None,
        body_referrer_id=None,
        body_full_name=None,
        body_username=None,
    )  # tgdeal_api.endpoints.system.UserRead

    """
    example output:
    {
           "id": 435,
           "balance": 0,
           "language": ...,
           "telegram_id": ...,
           "full_name": ...,
           "username": ...,
           "api_token": ...,
           "bot_initialized": false
    }
    """


asyncio.run(main())
```