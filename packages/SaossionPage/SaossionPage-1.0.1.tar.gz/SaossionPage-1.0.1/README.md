# dumb_menu

[![Downloads](https://static.pepy.tech/badge/SaossionPage)](https://pepy.tech/project/SaossionPage)

The brother version of the Drissionpage library, SaossionPage, is referred to as Sao Shen for short


## Installation

```
pip install SaossionPage
```



## Usage

example:

```python

from SaossionPage import Browser



if __name__ == '__main__':
    browser = Browser(config=" ")


    browser.open('https://www.doc88.com/')


    t=browser.page.latest_tab

    y=t.ele('t:body')
    t.wait(2)
     
    # 打印树结构
    browser.get_tree(y)
       



    input(' press any key to exit')


```



## Update log





`1.0.0` first release

