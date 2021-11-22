<!--
 * @Description: README.md
 * @Author: Rainyl
 * @Date: 2021-11-22 17:32:06
 * @LastEditTime: 2021-11-22 18:09:49
-->
# WANawallet - A tool for convert Alipay and WeChat Pay bills to Nayang Wallet's format

WANawallet stands for W(eChat)A(lipay)Nayang wallet(Link [here](https://play.google.com/store/apps/details?id=me.bakumon.moneykeeper)), a tool to convert your Alipay and WeChat Pay bills to Nayang wallet' format and database.

## Usage

- option 1: You can download the prebuilt files from [release](https://github.com/rainyl/wanawallet/releases) for windows now, cross platform will further supported if necessary.

- option 2: run from source
  - `pip install pyside6 pandas tqdm`
  - `python main.py`

After open the application, you should follow the following steps:

0. Config your `MoneyKeeper` app at your cell phone, then backup, you can get a `MoneyKeeperCloudBackup.zip` or `MoneyKeeperBackup.zip`, anyway, it includes two files, `me.bakumon.moneykeeper_preferences.xml` and `MoneyKeeper.db`, the second is your database file, which will be important in the next steps.

1. click the `Browse` next to `input` to select your bills in `.csv` format, you can obtain them from Alipay and WeChat Pay.

2. click the `Browse` next to the `output`, select your database, NOTE: the database will be overwrote!

3. You can delete rows in the right table by select them and click `delete` button.

4. click the `convert` button to write the data to your database

5. Compress your `MoneyKeeperCloudBackup.zip` or `MoneyKeeperBackup.zip` and replace your cell phone's with it, then restore in the `MoneyKeeper`

6. You can also combine it with `WebDAV` to avoid manul copy, and keep version history.

## TODO

- [ ] Add WebDAV to work with cloud backup
- [ ] Drop to add files
- [ ] Fetch from email and auto append

## LICENSE

No LICENSE for now, you can use the code for personal learn and research but `CAN'T` for commercial use.

The license will be add in the future.

&copy;Rainyl All Rights Reserved
