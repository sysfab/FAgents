---
title: Message and attachments
---
# Message and attachments

## Message

[Message][message_url] is an object that holds message data - content and role.  
It's also easier to use than writing dicts manually:
```py
from FAgents import Message, File, Image

msg_dict = Message(
    "Can you find the bug in my code? Button should be rounded but it's not",
    File.from_file("code.tsx"),
    Image.from_file("screenshot.png"),

    role = 'user'
).to_dict()

# VS

msg_dict = {
    'type': 'message', 
    'content': [
        {'text': "Can you find the bug in my code? Button should be rounded but it's not", 'type': 'text'}, 
        File.from_file("code.tsx").to_dict(),
        Image.from_file("screenshot.png").to_dict()
    ], 
    'role': 'user'
}
```
> You can also use [User][user_url], [Assistant][assistant_url], [Developer][developer_url], [System][system_url] helpers to further simplify the creation:
> ```py
> User(
>     "Can you find the bug in my code? Button should be rounded but it's not",
>     File.from_file("code.tsx"),
>     Image.from_file("screenshot.png"),
> )
> ```

---

## Attachments

Message content is a list of [Text][text_url] and [Image][image_url], [File][file_url] attachments  
> Note: When creating Message, all strings are automatically converted into Text objects  

### Text

[Text][text_url] objects only contain `text` field:
```py
Text(text="Hello!")
```

### Image

[Image][image_url] objects contain `url`, `format` fields:
```py
Image(
    url="https://example.com/image.png",
    format="image/png" # MIME type
)
```  

You can also create images from base64 data:
```py
Image.from_base64(
    data="data:...", # raw png data encoded as base64
    format="image/png" # MIME type
)
```

Or you can load it from the local file directly (will parse as base64 automatically):
```py
Image.from_file("some_image.png")
```

### File

[File][file_url] objects contain many fields, and, when you still can construct it manually, preffered way is:
```py
File.from_file("some_file.txt")
```

<!-- References -->
[message_url]: ../api-reference/#FAgents.Message
[user_url]: ../api-reference/#FAgents.User
[assistant_url]: ../api-reference/#FAgents.Assistant
[developer_url]: ../api-reference/#FAgents.Developer
[system_url]: ../api-reference/#FAgents.System
[text_url]: ../api-reference/#FAgents.Text
[image_url]: ../api-reference/#FAgents.Image
[file_url]: ../api-reference/#FAgents.File