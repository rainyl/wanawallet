import sqlite3
import datetime
import shutil
from argparse import ArgumentParser
import pandas as pd
from pathlib import Path
from tqdm import tqdm

COLUMN_HASH = {
    "收/支": "io",
    "交易对方": "target",
    "对方账号": "targetid",
    "商品说明": "commodity",
    "商品": "commodity",
    "收/付款方式": "payment",
    "支付方式": "payment",
    "金额": "money",
    "金额(元)": "money",
    "交易状态": "status",
    "当前状态": "status",
    "交易分类": "category",
    "交易类型": "category",
    "交易订单号": "payid",
    "交易单号": "payid",
    "商家订单号": "sellerid",
    "商户单号": "sellerid",
    "交易时间": "paytime",
    "备注": "note",
}
TYPE_HASH = {
    "教育培训": 22,
    "医疗健康": 16,
    "退款": 35,
    "餐饮美食": 1,
    "日用百货": 4,
    "家居家装": 7,
    "充值缴费": 20,
    "数码电器": 13,
    "其他": 26,
    "服饰装扮": 8,
    "保险": 23,
    "投资理财": 26,
    "转账红包": 17,
    "交通出行": 5,
    "运动户外": 5,
    "文化休闲": 22,
    "生活服务": 37,
    "商业服务": 37,
    "美容美发": 15,
    "公共服务": 37,
    "收入": 34,
    "商户消费": 36,
    "扫二维码付款": 36,
    "转账": 36,
    "群收款": 36,
    "零钱通转出-到零钱": 36,
    "转账-退款": 36,
    "携程旅行-退款": 36,
    "微信红包（单发）": 36,
    "二维码收款": 36,
    "微信红包": 36,
    "微信支出": 36,
    "微信收入": 38,
}


def washer(path: str, kind: str):
    if kind == "alipay":
        data = pd.read_csv(path, skiprows=1, encoding="gbk")
    else:
        data = pd.read_csv(path, skiprows=16)
        data = pd.read_csv(path, skiprows=16)
        data.loc[(data[data["收/支"]=="支出"]).index, "交易类型"] = "微信支出"
        data.loc[(data[data["收/支"]=="收入"]).index, "交易类型"] = "微信收入"
    data = data.dropna(axis=1, how="all")
    data = data.rename(columns={c: c.strip() for c in data.columns})
    columnsOld = list(data.columns)
    columnsNew = [COLUMN_HASH[c] for c in columnsOld]
    data = data.rename(columns={co: cn for co, cn in zip(columnsOld, columnsNew)})
    data = data.dropna(axis=0, how="all", subset=["payid", "paytime"])

    return data


def insert2Na(db_path, data):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    try:
        cur.executemany(
            "insert into Record(money,remark,time,create_time,record_type_id,assets_id) values(?,?,?,?,?,?);",
            data
        )
        conn.commit()
        return {"status": 1, "msg": "success!"}
    except Exception as e:
        return {"status": 0, "msg": e}
    conn.close()


def getRecords(df: pd.DataFrame):
    allRecords = []
    for r in tqdm(range(df.shape[0])):
        row = df.iloc[r, :]
        money = int(float(str(row["money"]).strip().replace("¥", ""))*100)
        remark = "{}-{}".format(row["target"].strip(), row["commodity"].strip())
        actTime = int(datetime.datetime.strptime(row["paytime"].strip(), "%Y-%m-%d %H:%M:%S").timestamp()*1000)
        createTime = int(datetime.datetime.now().timestamp()*1000)
        recordType = TYPE_HASH[row["category"].strip()]
        tmp = [money, remark, actTime, createTime, recordType, -1]
        allRecords.append(tmp)
        # print(f"Working on {r}/{df.shape[0]}...")
    return allRecords


def main(src: Path, dst: Path, overwrite: bool, dbPath: Path):
    bills = src.glob("*.csv")
    if not dst.exists():
        dst.mkdir()
    if not overwrite:
        shutil.copyfile(dbPath, dst / dbPath.name)
        dbPath = dst / dbPath.name
    for bill in bills:
        kind = "alipay" if bill.name.startswith("alipay") else "wechat"
        washData = washer(bill, kind=kind)
        records = getRecords(washData)
        insert2Na(dbPath, records)
        print(f"Processed {bill.name}")


if __name__ == "__main__":
    parser = ArgumentParser("Convert alipay and wechat pay bills to nayang wallet")
    parser.add_argument("--src", "-s", default="data", type=Path, help="the source data directory where the bills data(.csv) in, default is data.")
    parser.add_argument("--dst", "-d", default="processed", type=Path, help="the destination directory where the database file to output, default is processed.")
    parser.add_argument("--overwrite", "-ow", default=0, type=bool, help="whether to overwrite the old database, 0 for not and 1 for overwrite.")
    parser.add_argument("--database", "-db", default="MoneyKeeper.db", type=Path, help="the database file backuped from nayang wallet.")
    args = parser.parse_args()
    main(args.src, args.dst, args.overwrite, args.database)
