[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

PhantomBrowser is typed Python wrapper for [phantomjscloud.com](https://phantomjscloud.com) api with optimize magic rendering and support asynchronous.

## Installation

```
pip install phantombrowser
```

## Example

render html:

```python
from PhantomBrowser import Browser


browser = Browser()
response = browser.get("https://example.com")
print(response.text)
browser.close()
```

render plain text:
```python
from PhantomBrowser import Browser


browser = Browser()
response = browser.get("https://example.com", render="plainText")
print(response.text)
browser.close()
```

render image:
```python
from PhantomBrowser import Browser


browser = Browser()
response = browser.get("https://example.com", render="png")
browser.saveAs("example.png", response.content)
browser.close()
```

render PDF:
```python
from PhantomBrowser import Browser


browser = Browser()
response = browser.get("https://example.com", render="pdf")
browser.saveAs("example.pdf", response.content)
browser.close()
```

the other method like `browser.post()`, `browser.put()`, `browser.patch()`, `browser.option()` and `browser.delete()` also supported.

You can also use the API key by setting the environment variable `PHANTOMJSCLOUD.COM_APIKEY` or directly in the class
```python
from PhantomBrowser import Browser


browser = Browser("Your API Key")
```

## Asynchronous Example

```python
from PhantomBrowser import AsyncBrowser
import asyncio


async def main():
    browser = AsyncBrowser()
    response = await browser.get("https://example.com")
    print(await response.text())
    await browser.close()

if __name__ == '__main__':
    asyncio.run(main())
```

## License

MIT
