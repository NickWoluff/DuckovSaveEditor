import json
import base64
import struct
import os
import shutil
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import tkinter.font as tkfont
from typing import Any
import webbrowser
import sys
import os
import tkinter as tk

def resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path) # type: ignore
    return relative_path

icon_path = resource_path("icon.ico")

def get_version() -> str:
    try:
        with open(resource_path("version.txt"), "r", encoding="utf-8") as f:
            return f.read().strip()
    except Exception:
        return "unknown"

# ==================== DPI 适配 ====================
def enable_high_dpi(root: tk.Tk):
    try:
        import ctypes
        ctypes.windll.shcore.SetProcessDpiAwareness(2)
    except:
        pass
    try:
        dpi = root.winfo_fpixels("1i")
        scale = 1.0 if dpi <= 96 else 1.25 if dpi <= 120 else 1.4 if dpi <= 144 else 1.8
        root.tk.call("tk", "scaling", scale)
    except:
        pass


# ==================== Base64 编解码 ====================
def decode_b64(b64_str: str | None, dtype: int):
    if not b64_str or b64_str == "AAAAAA==":
        return 0
    try:
        raw = b64_str + "=" * (-len(b64_str) % 4)
        data = base64.b64decode(raw)
        if dtype == 1:
            return round(struct.unpack("<f", data)[0], 2)
        if dtype == 2:
            return struct.unpack("<i", data)[0]
        if dtype == 3:
            return data[0] != 0
    except:
        return 0
    return 0


def encode_b64(value: str, dtype: int) -> str:
    try:
        if dtype == 1:
            data = struct.pack("<f", float(value))
        elif dtype == 2:
            data = struct.pack("<i", int(value))
        elif dtype == 3:
            data = bytes([1 if str(value).lower() in ("1", "true", "yes") else 0])
        else:
            return ""
        return base64.b64encode(data).decode("ascii")
    except Exception as e:
        print("encode_b64 error:", e)
        return ""


# ==================== 映射 ====================
ITEM_NAME_MAP = {
1: "切肉刀", 2: "三级防弹衣", 3: "金色五角星", 4: "Gun Template", 8: "R6电池", 10: "止血绷带", 11: "PP3电池", 12: "焗豆罐头", 13: "苏打饼干", 14: "可乐", 15: "大急救箱", 16: "急救箱", 17: "小急救箱", 18: "水浸金枪鱼罐头", 19: "油浸金枪鱼罐头", 20: "阿司匹林", 21: "漂白剂", 22: "红条香烟", 23: "管状炸弹", 24: "集束管状炸弹", 25: "手电", 26: "防毒面具", 27: "滑雪镜", 28: "钉子", 29: "伏特加", 30: "MD40", 31: "扳手", 32: "一级防弹衣", 33: "二级防弹衣", 34: "四级防弹衣", 35: "五级防弹衣", 36: "装饰包", 37: "小学背包", 38: "旅行包", 39: "生存者背包", 40: "行军背包MAX", 41: "摩托头盔", 42: "老钢盔", 43: "特警头盔", 44: "SightPRO头盔", 45: "SCIFI面罩", 46: "神之电焊头", 47: "汽车扳手", 48: "大扩容箱", 49: "中扩容箱", 50: "小扩容箱", 51: "闹钟", 52: "洁厕灵", 53: "红色大桶", 54: "蓝色大桶", 55: "黄色大桶", 56: "金属油桶", 57: "高尔夫球棒", 58: "墨水", 59: "锅", 60: "卷纸", 61: "Cippo", 62: "压力传感器", 63: "uPhone手机", 64: "对讲机", 65: "军用对讲机", 66: "闪光手雷", 67: "手雷", 68: "巧克力", 69: "能量棒", 70: "蜂蜜", 71: "番茄酱", 72: "书", 73: "信件", 74: "安全屋隔间钥匙", 75: "飞机模型", 76: "足球", 77: "自行车模型", 78: "大炮", 79: "指南针", 80: "骰子", 81: "骰子", 82: "玩具鱼", 83: "怀表", 84: "鸭蛋", 85: "铝热剂", 86: "丙烷", 87: "绳子", 88: "一堆药", 89: "输液药品", 90: "扫帚", 91: "平头螺丝刀", 92: "电锯", 93: "金属桶", 94: "塑料桶", 95: "大锤子", 96: "锤子", 97: "煤油灯", 98: "铲子", 99: "望远镜", 100: "捕兽陷阱", 101: "撬棍", 102: "配件模板", 103: "奶牛面具", 104: "牛仔帽", 105: "可可奶", 106: "苏打水", 107: "水壶", 108: "威士忌", 109: "钢笔", 110: "剪刀", 111: "奖杯", 112: "麦克风", 113: "收音机", 114: "TOMSUNG手机", 115: "酸奶", 116: "报纸", 117: "笔记", 118: "口红", 119: "金戒指", 120: "花花戒指", 121: "智能机器人", 122: "玩具火箭", 123: "头骨饰品", 124: "手鼓", 125: "小号", 126: "木琴", 127: "轮胎", 128: "线", 129: "南瓜", 130: "购物框", 131: "杯子", 132: "蛋糕", 133: "胡萝卜", 134: "骨头玩具", 135: "心", 136: "注射器", 137: "黄针", 138: "头灯", 139: "子弹模板", 140: "L-普通弹", 141: "L-燃烧弹", 142: "L-穿甲弹", 143: "S-普通弹", 144: "S-达姆弹", 145: "S-燃烧弹", 146: "霰弹-鹿弹", 153: "探索者的信", 154: "宿舍楼103钥匙", 155: "宿舍楼106钥匙", 157: "L-涂毒弹", 158: "L-高级穿甲弹", 159: "S-穿甲弹", 160: "S-高级穿甲弹", 161: "霰弹-食人鱼", 162: "霰弹-龙息", 163: "霰弹-箭形弹", 164: "霰弹-电击", 165: "狙击-普通弹", 166: "狙击-穿甲弹", 167: "狙击-电击弹", 168: "狙击-空间弹", 169: "狙击-高级穿甲弹", 174: "突击握把Lv1", 175: "突击握把Lv2", 176: "突击握把Lv3", 177: "快拆握把Lv1", 178: "快拆握把Lv2", 179: "快拆握把Lv3", 180: "垂直握把Lv1", 181: "垂直握把Lv2", 182: "垂直握把Lv3", 183: "大口径制退器Lv1", 184: "大口径制退器Lv2", 185: "大口径制退器Lv3", 186: "霰弹枪集束器Lv1", 187: "霰弹枪集束器Lv2", 188: "霰弹枪集束器Lv3", 189: "狙击枪消音器Lv1", 190: "狙击枪消音器Lv2", 191: "狙击枪消音器Lv3", 192: "小口径制退器Lv1", 193: "小口径制退器Lv2", 194: "小口径制退器Lv3", 195: "4倍镜Lv1", 196: "4倍镜Lv2", 197: "4倍镜Lv3", 198: "8倍镜Lv1", 199: "8倍镜Lv2", 200: "8倍镜Lv3", 201: "数字瞄具Lv1", 202: "数字瞄具Lv2", 203: "数字瞄具Lv3", 204: "全息瞄具Lv1", 205: "全息瞄具Lv2", 206: "全息瞄具Lv3", 207: "快速瞄具Lv1", 208: "快速瞄具Lv2", 209: "快速瞄具Lv3", 210: "红点瞄具Lv1", 211: "红点瞄具Lv2", 212: "红点瞄具Lv3", 213: "步枪枪托Lv1", 214: "步枪枪托Lv2", 215: "步枪枪托Lv3", 216: "霰弹枪托Lv1", 217: "霰弹枪托Lv2", 218: "霰弹枪托Lv3", 219: "冲锋枪枪托Lv1", 220: "冲锋枪枪托Lv2", 221: "冲锋枪枪托Lv3", 222: "狙击枪枪托Lv1", 223: "狙击枪枪托Lv2", 224: "狙击枪枪托Lv3", 225: "战术激光Lv1", 226: "战术激光Lv2", 227: "战术激光Lv3", 228: "战术手电Lv1", 229: "战术手电Lv2", 230: "战术手电Lv3", 231: "大口径扩容弹夹Lv1", 232: "大口径扩容弹夹Lv2", 233: "大口径扩容弹夹Lv3", 234: "小口径扩容弹夹Lv1", 235: "小口径扩容弹夹Lv2", 236: "小口径扩容弹夹Lv3", 238: "AK-103", 240: "AK-47", 242: "MF", 244: "RPK", 246: "VPO-101", 248: "土制猎枪", 250: "MP-155", 252: "AK-74U", 254: "格力克", 256: "MMG", 258: "MP7", 260: "UP-45", 262: "UZI", 263: "突击握把Lv4", 264: "快拆握把Lv4", 265: "垂直握把Lv4", 266: "大口径扩容弹夹Lv4", 267: "小口径扩容弹夹Lv4", 268: "大口径制退器Lv4", 269: "霰弹枪集束器Lv4", 270: "狙击枪消音器Lv4", 271: "小口径制退器Lv4", 272: "4倍镜Lv4", 273: "8倍镜Lv4", 274: "数字瞄具Lv4", 275: "全息瞄具Lv4", 276: "快速瞄具Lv4", 277: "红点瞄见Lv4", 278: "步枪枪托Lv4", 279: "霰弹枪托Lv4", 280: "冲锋枪枪托Lv4", 281: "狙击枪枪托Lv4", 282: "战术激光Lv4", 283: "战术手电Lv4", 284: "蓝图模板", 285: "蓝图：AK-103", 286: "蓝图：AK-47", 287: "蓝图：AK-74U", 289: "蓝图：土制猎枪", 290: "蓝图：MF", 291: "蓝图：MMG", 292: "蓝图：MP-155", 293: "蓝图：MP-7", 294: "蓝图：RPK", 295: "蓝图：VPO-101", 296: "蓝图：UAK-45", 297: "蓝图：UZI", 298: "移动硬盘", 299: "移动硬盘：宿舍楼", 300: "移动硬盘：加油站录像", 301: "J-Lab软盘", 302: "枪", 305: "切肉刀", 306: "战斧", 307: "一级防弹衣", 308: "冷核碎片", 309: "赤核碎片", 312: "工厂门禁卡", 313: "工厂门禁卡（加密）", 314: "武器蓝图：基础", 315: "武器蓝图：专业", 316: "武器蓝图：进阶", 317: "武器蓝图：终极", 318: "图腾：甲胄Ⅱ", 319: "图腾：甲胄Ⅰ", 320: "图腾：进击Ⅱ", 321: "图腾：进击Ⅰ", 322: "图腾：战士Ⅱ", 323: "图腾：战士Ⅰ", 324: "图腾：轻盈Ⅱ", 325: "图腾：健壮Ⅲ", 326: "火箭弹Lv1", 327: "RPG-7", 328: "显示卡", 329: "充电宝", 330: "情报文件", 331: "LEDX皮肤透照仪", 332: "螺栓", 333: "灯泡", 334: "节能灯", 335: "螺母", 336: "电源线", 337: "电线", 338: "CD驱动器", 339: "电路板", 340: "电子元件", 343: "破旧鱼竿", 344: "Item_Bait1", 345: "Item_Bait2", 346: "一级鱼", 347: "二级鱼", 348: "Item_Bait3", 349: "三级鱼", 350: "S-涂毒弹", 351: "S-电击弹", 352: "L-电击弹", 353: "L-空间弹", 354: "S-空间弹", 355: "霰弹-穿甲弹", 356: "空手（游戏中图标是切肉刀）", 357: "劣质弓", 358: "木箭矢", 359: "灰房子钥匙", 360: "杂物围栏钥匙", 361: "木料", 362: "金属片", 363: "L-过期子弹", 364: "S-生锈子弹", 365: "木棍", 366: "老朋友的信", 367: "武器零件", 368: "虚化的羽毛", 369: "图腾：抗物Ⅰ", 370: "图腾：马拉松Ⅰ", 371: "图腾：饥饿大师", 372: "图腾：耐力", 373: "传送装置图纸", 374: "配方：MD40", 375: "农场镇传送密钥", 376: "蓝图：RPG发射器", 377: "配方：捕兽夹", 378: "配方：MD40", 379: "背带衣", 380: "T.H篮球", 381: "配方：背带衣", 382: "配方：撬棍", 383: "配方：电源线", 384: "机械钥匙", 385: "怀表", 386: "货物清单", 387: "配方：电路板", 388: "0.2BTC", 389: "神秘留言", 390: "小型能量弹药", 391: "方块枪", 392: "蓝图：方块枪", 393: "蓝图：小型能量弹药", 394: "计算核心", 395: "黑色针剂", 396: "配方：黑色针剂", 397: "比特币矿机", 398: "负重针", 399: "爆炸箭", 400: "蓝图：爆炸箭", 401: "蓝图：土豆显卡", 402: "土豆显卡", 403: "土豆", 404: "霰弹-破烂", 405: "蓝图：防毒面具", 406: "狙击-劣质子弹", 407: "M107", 408: "电抗性针", 409: "镇痛剂", 410: "配方：电抗性针", 411: "配方：镇痛剂", 412: "狙击枪弹匣Lv1", 413: "狙击枪弹匣Lv2", 414: "狙击枪弹匣Lv3", 415: "狙击枪弹匣Lv4", 416: "大口径消音器Lv1", 417: "大口径消音器Lv2", 418: "大口径消音器Lv3", 419: "大口径消音器Lv4", 420: "小口径消音器Lv1", 421: "小口径消音器Lv2", 422: "小口径消音器Lv3", 423: "小口径消音器Lv4", 424: "黑市联络笔记", 425: "加密U盘", 426: "地窖钥匙", 427: "隐居者的信", 428: "瓶装水", 429: "愿望单之力", 430: "图腾：抗电Ⅱ", 431: "图腾：抗电Ⅰ", 432: "图腾：效率Ⅱ", 433: "图腾：控枪Ⅲ", 434: "图腾：战术换弹", 435: "图腾：忍者Ⅱ", 436: "图腾：忍者Ⅰ", 437: "VPO-劳登改", 438: "热血针剂", 439: "配方：热血针剂", 440: "废弃加油站钥匙", 441: "厂区办公室钥匙", 442: "小隔间钥匙", 443: "地窖围栏钥匙", 444: "红包", 445: "小纸条", 446: "铜钱串", 447: "中国结", 448: "红灯笼", 449: "饺子", 450: "烂格力克", 451: "现金", 452: "快速握把A", 453: "快速握把B", 454: "Item_Grip_ALL_MOV_1", 455: "垂直握把Ⅰ", 456: "水平握把Ⅰ", 457: "平衡握把", 458: "垂直握把Ⅱ", 459: "水平握把Ⅱ", 460: "腰射握把Ⅰ", 461: "Item_Grip_ALL_SCA_2", 462: "腰射握把Ⅱ", 463: "手枪制退器-均衡A", 464: "手枪制退器-均衡B", 465: "手枪消音器", 466: "手枪延长枪口", 467: "手枪制退器-散布", 468: "冲锋枪制退器-均衡A", 469: "冲锋枪制退器-均衡B", 470: "冲锋枪垂直制退器", 471: "冲锋枪水平制退器", 472: "冲锋枪制退器-散布", 473: "冲锋枪螺旋制退器", 474: "冲锋枪消音器", 475: "步枪延长枪口", 476: "步枪制退器-均衡A", 477: "步枪制退器-均衡B", 478: "步枪垂直制退器", 479: "步枪水平制退器", 480: "步枪制退器-散布", 481: "步枪螺旋制退器", 482: "步枪消音器", 483: "Item_Muzzle_AR_SIL_2", 484: "狙击枪延长枪口", 485: "狙击枪制退器-均衡A", 486: "Item_Muzzle_SNP_REC_2", 487: "狙击枪水平制退器", 488: "狙击枪制退器-散布", 489: "狙击枪制退器-机动", 490: "狙击枪消音器", 491: "Item_Muzzle_SNP_SIL_2", 492: "Item_Muzzle_SNP_SIL_3", 493: "霰弹枪制退器-均衡A", 494: "Item_Muzzle_SHT_REC_2", 495: "Item_Muzzle_SHT_REC_3", 496: "Item_Muzzle_SHT_REC_4", 497: "Item_Muzzle_SHT_SCA_1", 498: "Item_Stock_PST_MOV_1", 499: "Item_Stock_PST_REL_1", 500: "Item_Stock_PST_SCA_1", 501: "Item_Stock_PST_SCA_2", 502: "Item_Stock_SMG_MOV_1", 503: "Item_Stock_SMG_REC_1", 504: "Item_Stock_SMG_REL_1", 505: "Item_Stock_SMG_SCA_1", 506: "Item_Stock_SMG_SCA_2", 507: "Item_Stock_SMG_SCA_3", 508: "快速枪托", 509: "平衡枪托Ⅰ", 510: "平衡枪托Ⅱ", 511: "轻型枪托", 512: "Item_Stock_AR_SCA_1", 513: "Item_Stock_AR_SCA_2", 514: "腰射枪托Ⅰ", 515: "控制枪托", 516: "腰射枪托Ⅱ", 517: "Item_Stock_AR_SCA_6", 518: "Item_Stock_SNP_REC_1", 519: "狙击枪平衡枪托Ⅱ", 520: "Item_Stock_SNP_SCA_1", 521: "狙击枪控制枪托Ⅰ", 522: "Item_Stock_SNP_SCA_3", 523: "狙击枪控制枪托Ⅱ", 524: "Item_Stock_SHT_MOV_1", 525: "Item_Stock_SHT_REC_1", 526: "Item_Stock_SHT_REL_1", 527: "Item_Stock_SHT_SCA_1", 528: "Item_Stock_SHT_SCA_2", 529: "Item_Stock_SHT_SCA_3", 530: "Item_Stock_SHT_SCA_4", 531: "手枪快速弹匣Ⅰ", 532: "手枪快速弹匣Ⅱ", 533: "手枪扩容弹匣Ⅰ", 534: "手枪扩容弹匣Ⅱ", 535: "Item_Magazine_PST_REL_1", 536: "冲锋枪快速弹匣", 537: "冲锋枪扩容弹匣Ⅰ", 538: "冲锋枪扩容弹匣Ⅱ", 539: "冲锋枪扩容弹匣Ⅲ", 540: "Item_Magazine_SMG_REL_1", 541: "Item_Magazine_SMG_REL_2", 542: "Item_Magazine_SMG_REL_3", 543: "步枪快速弹匣Ⅰ", 544: "步枪快速弹匣Ⅱ", 545: "Item_Magazine_AR_ADS_3", 546: "步枪扩容弹匣Ⅰ", 547: "步枪扩容弹匣Ⅱ", 548: "步枪扩容弹匣Ⅲ", 549: "Item_Magazine_AR_CAP_4", 550: "Item_Magazine_AR_REL_1", 551: "Item_Magazine_AR_REL_2", 552: "Item_Magazine_AR_REL_3", 553: "狙击枪快速弹匣Ⅰ", 554: "狙击枪快速弹匣Ⅱ", 555: "Item_Magazine_SNP_ADS_3", 556: "狙击枪扩容弹匣Ⅰ", 557: "狙击枪扩容弹匣Ⅱ", 558: "Item_Magazine_SNP_CAP_3", 559: "Item_Magazine_SNP_REL_1", 560: "Item_Magazine_SNP_REL_2", 561: "霰弹枪扩容弹匣Ⅰ", 562: "霰弹枪扩容弹匣Ⅱ", 563: "霰弹枪扩容弹匣Ⅲ", 564: "Item_Magazine_SHT_CAP_4", 565: "Item_Magazine_SHT_REL_1", 566: "Item_Magazine_SHT_REL_2", 567: "Item_Magazine_SHT_REL_3", 568: "步枪4倍镜", 569: "狙击枪8倍镜", 570: "数字瞄具", 571: "全息瞄具", 572: "快速瞄具", 573: "红点瞄具", 574: "2倍镜", 575: "Item_Tec_Laser_NON_1", 576: "激光-机动", 577: "激光-快反", 578: "激光-基础", 579: "激光-校准", 580: "战术手电", 583: "Item_Muzzle_SHT_SCA_2", 584: "霰弹枪制退器-机动", 594: "S-生锈弹", 595: "S-普通弹", 596: "S-燃烧弹", 597: "S-穿甲弹", 598: "S-高级穿甲弹", 599: "S-毒性弹", 600: "S-感电弹", 601: "S-空间弹", 602: "S-肉伤弹", 603: "AR-生锈弹", 604: "AR-普通弹", 605: "AR-燃烧弹", 606: "AR-穿甲弹", 607: "AR-高级穿甲弹", 608: "AR-毒性弹", 609: "AR-感电弹", 610: "AR-空间弹", 611: "AR-肉伤弹", 612: "L-生锈弹", 613: "L-普通弹", 614: "L-燃烧弹", 615: "L-穿甲弹", 616: "L-高级穿甲弹", 617: "L-毒性弹", 618: "L-感电弹", 619: "L-空间弹", 620: "L-肉伤弹", 621: "生锈狙击弹", 622: "普通狙击弹", 623: "燃烧狙击弹", 624: "中级穿甲狙击弹", 625: "高级穿甲狙击弹", 626: "毒性狙击弹", 627: "感电狙击弹", 628: "空间狙击弹", 629: "肉伤狙击弹", 630: "生锈霰弹", 631: "普通霰弹", 632: "燃烧霰弹", 633: "穿甲霰弹", 634: "高级穿甲霰弹", 635: "毒性霰弹", 636: "感电霰弹", 637: "空间霰弹", 638: "肉伤霰弹", 639: "MAG-生锈弹", 640: "MAG-普通弹", 641: "MAG-燃烧弹", 642: "MAG-中级穿甲弹", 643: "MAG-高级穿甲弹", 644: "MAG-毒性弹", 645: "MAG-感电弹", 646: "MAG-空间弹", 647: "MAG-肉伤弹", 648: "木矢", 649: "爆炸矢", 650: "小型能量弹", 651: "激光-暴击", 652: "ADAR 2-15", 653: "StG 77", 654: "StG 77A3", 655: "MP5", 656: "SKS-45", 657: "TOZ-66", 658: "TOZ-106", 659: "VPO-136", 660: "烟雾弹", 662: "中级武器零件", 663: "高级武器零件", 665: "蓝图：ADAR 2-15", 666: "蓝图：StG 77", 667: "蓝图：StG 77A3", 668: "蓝图：MP5", 669: "蓝图：SKS", 670: "蓝图：TOZ-66", 671: "蓝图：TOZ-106", 672: "蓝图：VPO-136", 675: "蓝图：普通重型弹", 676: "蓝图：普通狙击弹", 677: "蓝图：普通霰弹", 678: "蓝图：MAG-普通弹", 679: "耳机", 680: "VSS", 681: "AS Val", 682: "DT MDR-556", 683: "DT MDR-762", 688: "S-低级穿甲弹", 689: "S-中级穿甲弹", 690: "S-高级穿甲弹", 691: "S-特种弹", 692: "AR-低级穿甲弹", 693: "AR-中级穿甲弹", 694: "AR-特种穿甲弹", 695: "AR-碎甲弹", 696: "L-低级穿甲弹", 697: "L-中级穿甲弹", 698: "L-特种穿甲弹", 699: "L-碎甲弹", 700: "穿甲狙击弹", 701: "高级穿甲狙击弹", 702: "特种穿甲狙击弹", 703: "碎甲狙击弹", 704: "低级穿甲霰弹", 705: "中级穿甲霰弹", 706: "高级穿甲霰弹", 707: "特种霰弹", 708: "MAG-穿甲弹", 709: "MAG-高级穿甲弹", 710: "MAG-特种穿甲弹", 711: "MAG-碎甲弹", 712: "手枪增伤枪口", 713: "冲锋枪增伤枪口", 714: "步枪增伤枪口", 715: "狙击枪增伤枪口", 716: "霰弹枪增伤枪口", 717: "冲锋枪腰射枪托Ⅱ", 718: "GPNVG-18夜视仪", 719: "T-7热成像目镜", 733: "带电MP7", 734: "Bizon-2", 735: "PPSh", 736: "SR-3M", 737: "Vector", 738: "配方：急救箱", 740: "白大褂", 741: "黑色眼镜", 742: "闪光的眼镜", 743: "有机纤维", 744: "太阳镜", 745: "维生系统线索", 746: "标记器", 747: "空气循环单元", 748: "高性能计算单元", 749: "蓝图：高性能计算单元", 750: "大型主板", 751: "爱狗的项圈", 753: "飞船推进器图纸（加密）", 754: "J-Lab一级凭证", 755: "J-Lab二级凭证", 756: "J-Lab三级凭证", 757: "矢量推进器研究日志", 758: "矿长的虹膜信息", 759: "工棚钥匙", 760: "导航系统图纸", 761: "星图", 762: "星图碎片Part2", 763: "星图碎片Part3", 764: "聚乙烯片", 765: "胶带", 766: "宇宙级防御力场蓝图（加密）", 767: "能量重塑装置", 768: "能源球", 769: "蛋清能源碎片", 772: "警棍", 774: "高性能计算单元蓝图（加密）", 775: "5000w电源", 776: "霰弹枪重型消音器", 777: "狙击枪快速枪托", 778: "大型散热器", 779: "家门钥匙01", 780: "M700", 781: "Mosin-Nagant", 782: "SV98", 783: "TT-33", 784: "PM", 785: "沙漠之鹰", 786: "M1A", 787: "M14", 788: "MCX Spear", 790: "一级防火服", 791: "皮夹克", 793: "配方：黄针", 794: "配方：负重针", 795: "民房钥匙", 796: "蓝图：T7热成像目镜", 797: "硬化针", 798: "持久针", 799: "紫外灯", 800: "近战针", 801: "J-Lab门禁卡（黄）", 802: "J-Lab门禁卡（红）", 803: "J-Lab门禁卡（绿）", 804: "J-Lab门禁卡（蓝）", 805: "蓝图：VSS", 806: "蓝图：AS Val", 807: "蓝图：DT MDR-556", 808: "蓝图：DT MDR-762", 809: "蓝图：带电MP7", 810: "蓝图：Bizon-2", 811: "蓝图：PPSh", 812: "蓝图：SR-3M", 813: "蓝图：Vector", 814: "蓝图：M700", 815: "蓝图：Mosin-Nagant", 816: "蓝图：SV98", 817: "蓝图：TT-33", 818: "蓝图：PM", 819: "蓝图：沙漠之鹰", 820: "蓝图：M1A", 821: "蓝图：M14", 822: "蓝图：MCX Spear", 823: "MF蓝图碎片1", 824: "MF蓝图碎片2", 825: "MF蓝图碎片3", 826: "南长区钥匙卡", 827: "神秘钥匙X", 828: "神秘钥匙O", 829: "神秘钥匙Z", 830: "蓝图：夜视仪", 831: "超市隔间钥匙", 832: "餐厅隔间钥匙", 833: "万能胶A", 834: "万能胶B", 835: "快递", 836: "钥匙包", 837: "BR快速弹匣Ⅰ", 838: "BR快速弹匣Ⅱ", 839: "BR扩容弹匣Ⅰ", 840: "BR扩容弹匣Ⅱ", 841: "麻布头套", 842: "配方：紫外灯", 843: "配方：红色大桶", 844: "配方：蓝色大桶", 845: "配方：黄色大桶", 846: "配方：金属油桶", 848: "遮眼布", 849: "船票", 850: "Item_Bullet_Enemy_Piercing1", 851: "Item_Bullet_Enemy_Piercing2", 852: "Item_Bullet_Enemy_Piercing3", 853: "Item_Bullet_Enemy_Piercing4", 854: "Item_Bullet_Enemy_Piercing5", 855: "Item_Bullet_Enemy_Piercing6", 856: "弱效空间风暴防护针", 857: "测试用空间风暴防护针", 858: "空间防护服", 859: "空间防护头盔", 860: "空间晶体", 861: "被污染的武器零件", 862: "带火AK-47", 863: "蓝图：带火AK-47", 864: "火药", 865: "配方：管状炸弹", 866: "配方：集束管状炸弹", 867: "蓝图：Glick（格力克）", 868: "挑战船票", 869: "连珠弓", 870: "低级穿甲箭", 871: "中级穿甲箭", 872: "强翅针", 873: "配方：被污染的武器零件", 874: "配方：大扩容箱", 875: "恢复针", 876: "MP-155 ULTIMA", 877: "蓝图：MP-155 ULTIMA", 878: "蘑菇", 879: "？？？", 880: "Item_PaperBoxArmor", 881: "纸箱子", 882: "注射器收纳包", 883: "蛋白粉", 884: "配方：蛋白粉", 885: "六级防弹衣", 886: "J-Lab门禁卡（黑）", 887: "J-Lab门禁卡（紫）", 888: "苹果", 889: "维达头盔", 890: "狗牌", 891: "路障头盔", 892: "？？？", 893: "空手（图标是切肉刀）", 894: "噗咙防弹衣", 895: "噗咙头盔", 896: "咕噜防弹衣", 897: "咕噜头盔", 898: "？？？", 899: "Item_EGun_StormBoss_2_Poison", 900: "Item_EGun_StormBoss_3_Fire", 901: "Item_EGun_StormBoss_4_Electric", 902: "？？？", 908: "啪啦防弹衣", 909: "比利防弹衣", 910: "口口防弹衣", 911: "啪啦头盔", 912: "比利头盔", 913: "口口头盔", 914: "咕噜枪", 915: "风暴枪", 916: "啪啦枪", 917: "比利枪", 918: "大型能量弹", 919: "测试种子", 920: "空间防护服终极版", 921: "空间防护头盔终极版", 922: "蛇形武装（游戏卡带）", 923: "未来主机（红白机造型的游戏机）", 924: "Item_GameTable", 925: "黑白显示器", 926: "加速卡", 927: "碳酸危鸭（游戏卡带）", 928: "Item_Cartridge_FactoryPanicShock", 929: "鸭鸭矿工（游戏卡带）", 930: "彩色显示器", 931: "？？？", 932: "小石头", 933: "毒雾弹", 934: "Item_Helmat_Soda_battery1", 935: "Item_Helmat_Soda_battery2", 936: "罐子头盔", 937: "Item_Helmat_Soda_Displayer", 938: "粑粑（可叠加）", 939: "粑粑", 940: "粑粑", 941: "燃烧弹", 942: "电击手雷", 943: "噗噗枪", 944: "粑粑弹", 945: "蝇蝇翅膀", 946: "噗噗喷", 947: "图腾：甲胄Ⅲ", 948: "图腾：攻击Ⅱ", 949: "图腾：攻击Ⅲ", 950: "图腾：攻击Ⅰ", 951: "图腾：抗电Ⅲ", 952: "图腾：马拉松Ⅱ", 953: "图腾：马拉松Ⅲ", 954: "图腾：抗火Ⅱ", 955: "图腾：抗火Ⅲ", 956: "图腾：抗火Ⅰ", 957: "图腾：进击Ⅲ", 958: "图腾：恢复Ⅱ", 959: "图腾：恢复Ⅲ", 960: "图腾：恢复Ⅰ", 961: "图腾：生命Ⅱ", 962: "图腾：生命Ⅲ", 963: "图腾：生命Ⅰ", 964: "图腾：忍者Ⅲ", 965: "图腾：抗物Ⅱ", 966: "图腾：抗物Ⅲ", 967: "图腾：抗毒Ⅱ", 968: "图腾：抗毒Ⅲ", 969: "图腾：抗毒Ⅰ", 970: "图腾：抗空间Ⅱ", 971: "图腾：抗空间Ⅲ", 972: "图腾：抗空间Ⅰ", 973: "蝇蝇眼镜", 974: "图腾：效率Ⅲ", 975: "图腾：效率Ⅰ", 976: "图腾：控枪Ⅱ", 977: "图腾：控枪Ⅲ", 978: "图腾：控枪Ⅰ", 979: "图腾：爆头Ⅱ", 980: "图腾：爆头Ⅲ", 981: "图腾：爆头Ⅰ", 982: "图腾：狙击Ⅱ", 983: "图腾：狙击Ⅲ", 984: "图腾：狙击Ⅰ", 985: "图腾：战士Ⅲ", 986: "图腾：狂战Ⅱ", 987: "图腾：狂战Ⅲ", 988: "图腾：狂战Ⅰ", 989: "图腾：感知Ⅱ", 990: "图腾：感知Ⅲ", 991: "图腾：感知Ⅰ", 992: "图腾：轻盈Ⅲ", 993: "图腾：轻盈Ⅰ", 994: "图腾：健壮Ⅱ", 995: "图腾：健壮Ⅰ", 996: "洋蓟", 997: "茄子", 998: "香蕉", 999: "花椰菜", 1000: "樱桃", 1001: "辣椒", 1002: "椰子", 1003: "玉米", 1004: "黄瓜", 1005: "大蒜", 1006: "葡萄", 1007: "韭菜", 1008: "柠檬", 1009: "芒果", 1010: "洋葱", 1011: "橙子", 1012: "梨", 1013: "菠萝", 1015: "杨桃", 1016: "草莓", 1017: "西红柿", 1018: "西瓜", 1019: "苹果的种子", 1020: "洋蓟的种子", 1021: "茄子的种子", 1022: "香蕉的种子", 1023: "胡萝卜的种子", 1024: "花椰菜的种子", 1025: "樱桃的种子", 1026: "辣椒的种子", 1027: "椰子的种子", 1028: "玉米的种子", 1029: "黄瓜的种子", 1030: "大蒜的种子", 1031: "葡萄的种子", 1032: "韭菜的种子", 1033: "柠檬的种子", 1034: "芒果的种子", 1035: "洋葱的种子", 1036: "橙子的种子", 1037: "梨的种子", 1038: "菠萝的种子", 1039: "土豆的种子", 1040: "南瓜的种子", 1041: "杨桃的种子", 1042: "草莓的种子", 1043: "西红柿的种子", 1044: "西瓜的种子", 1045: "保险箱钥匙", 1046: "防御力场发生器", 1047: "快递", 1048: "快递", 1049: "快递", 1050: "快递", 1051: "快递", 1052: "快递", 1053: "快递", 1054: "快递", 1055: "特制AK-47（说明：无法带回基地）", 1056: "特制StG 77A3（说明：无法带回基地）", 1057: "特制M14（说明：无法带回基地）", 1058: "特制格力克（说明：无法带回基地）", 1059: "特制MP-155（说明：无法带回基地）", 1060: "特制SR-3M（说明：无法带回基地）", 1061: "特制Mosin-Nagant（说明：无法带回基地）", 1062: "毕业生名单", 1063: "校长室钥匙", 1064: "特种洁厕灵", 1065: "腿疼特效药", 1066: "手疼特效药", 1067: "头疼特效药", 1068: "特效止疼药", 1069: "强效蛋白粉", 1070: "火抗性针", 1071: "毒抗性针", 1072: "空间抗性针", 1073: "沉重的轮胎", 1074: "棒球棍", 1075: "带钉棒球棍", 1076: "蓝图：屎弹（粑粑弹）", 1077: "石棉工作服", 1078: "石棉工作头盔", 1079: "橡胶工作服", 1080: "比利背包", 1081: "啪啦背包", 1082: "咕噜背包", 1083: "碎蛋壳", 1084: "员工公寓102钥匙", 1085: "员工公寓105钥匙", 1086: "员工公寓101钥匙", 1087: "宿舍楼101钥匙", 1088: "未来控制器（红白机游戏手柄）", 1089: "TOZ-66龙息", 1090: "显示卡SLI", 1091: "蓝图：显示卡SLI", 1092: "一堆电子零件", 1093: "高手护甲", 1094: "蓝图：彩色显示器", 1095: "好钓竿", 1096: "厉害的钓竿", 1097: "绿鲷鱼", 1098: "蓝雀鲷鱼", 1099: "青南乳鱼", 1100: "蓝鲭鱼", 1101: "蓝枪鱼", 1102: "蓝旗鱼", 1103: "蓝吊鱼", 1104: "棕白石鲈", 1105: "棕梭鱼", 1106: "棕沙丁鱼", 1107: "黄金鱼", 1108: "绿胖头鱼", 1109: "绿背鳙鱼", 1110: "绿黄鲀", 1111: "蓝猫鲨鱼", 1112: "橙青鳍鱼", 1113: "橙金鳞鱼", 1114: "粉金鱼", 1115: "紫雀鲷鱼", 1116: "粉鳍火焰鱼", 1117: "红鳍鲷鱼", 1118: "红九间鱼", 1119: "红金鱼", 1120: "大眼红鱼", 1121: "红斑鱼", 1122: "白燕鱼", 1123: "大头金鱼", 1124: "白扁鱼", 1125: "黄绿鲷", 1126: "绿刺豚", 1127: "蓝图：TOZ-66龙息", 1128: "空间格力克", 1130: "高手背包", 1131: "洋蓟瓣", 1132: "玉米粒", 1133: "芒果丁", 1134: "蚯蚓", 1135: "葡萄粒", 1136: "鸭舌帽", 1137: "五级重型防弹衣", 1138: "四级重型防弹衣", 1139: "三级重型防弹衣", 1140: "四级作战防弹衣", 1141: "五级作战防弹衣", 1142: "三级作战防弹衣", 1143: "坦克头盔", 1144: "二级轻型头盔", 1145: "三级轻型头盔", 1146: "维和头盔", 1147: "四级防弹头盔", 1148: "五级轻型头盔", 1149: "五级作战头盔", 1150: "地窖岔路钥匙", 1151: "防空系统密钥", 1152: "Item_Grenade_SpaceBoss", 1153: "Item_Grenade_SpaceBoss", 1154: "鱼饵", 1155: "蓝图：电击手雷", 1156: "蓝图：燃烧弹", 1157: "蓝图：毒雾弹", 1158: "水族箱", 1159: "蓝图：风暴枪", 1160: "配方：鱼饵", 1161: "蓝图：大型能量弹", 1162: "强化小能量弹", 1163: "风暴工作服", 1164: "神秘飞船图纸", 1165: "蓝色方块", 1166: "方块收集装置", 1167: "蓝图：好钓竿", 1168: "蓝图：厉害的钓竿", 1169: "J-Lab放映室钥匙", 1170: "高级有机纤维", 1171: "顶级有机纤维", 1172: "小直刀", 1173: "木柄短刀", 1174: "指虎刀", 1175: "爪刀", 1176: "廓尔喀弯刀", 1177: "战术刺刀", 1178: "战术刀具箱", 1179: "配方：战术刀具箱", 1180: "自制糖果", 1181: "棒棒糖", 1182: "和平星", 1183: "和平星（粉末）", 1184: "高级火药", 1185: "蓝图：AR特种穿甲弹", 1186: "蓝图：L-特种穿甲弹", 1187: "蓝图：MAG-特种穿甲弹", 1188: "蓝图：特种霰弹", 1189: "蓝图：S-特种弹", 1190: "蓝图：特种穿甲狙击弹", 1191: "北厂区小屋钥匙", 1192: "罐装火药：蓝色包装", 1193: "罐装火药：绿色包装", 1194: "罐装火药：红色包装", 1195: "蓝图：穿甲狙击弹", 1196: "蓝图：AR-穿甲弹", 1197: "蓝图：AR-高级穿甲弹", 1198: "蓝图：L-穿甲弹", 1199: "蓝图：L-高级穿甲弹", 1200: "蓝图：MAG-穿甲弹", 1201: "蓝图：MAG-高级穿甲弹", 1202: "蓝图：穿甲霰弹", 1203: "蓝图：高级穿甲霰弹", 1204: "蓝图：S-穿甲弹", 1205: "蓝图：S-高级穿甲弹", 1206: "蓝图：高级穿甲狙击弹", 1207: "战术咸鱼", 1208: "猪肉刀", 1209: "玩具枪", 1210: "配方：可乐", 1213: "风暴工作头盔", 1214: "防御力场操作说明", 1215: "蓝图：五级防弹衣", 1216: "蓝图：空间防护服终极版", 1217: "蓝图：五级作战防弹衣", 1218: "蓝图：五级重型防弹衣", 1219: "蓝图：六级防弹衣", 1220: "蓝图：行军背包MAX", 1221: "蓝图：SCIFI面罩", 1222: "蓝图：空间防护头盔最终版", 1223: "蓝图：五级轻型头盔", 1224: "蓝图：五级作战头盔", 1225: "蓝图：神之电焊头盔", 1226: "疗养院机房钥匙", 1227: "疗养院餐厅钥匙", 1228: "疗养院房间钥匙-1", 1229: "疗养院房间钥匙-2", 1230: "加速器", 1231: "浓缩浆质", 1232: "晶体电池", 1233: "晶体过滤单元", 1234: "晶体增压器", 1235: "大块空间晶体", 1236: "风暴眼", 1237: "配方：浓缩浆质", 1238: "MF-毒液", 1240: "蓝图：MF-毒液", 1241: "汽车电池", 1243: "骨夹板", 1244: "高级骨夹板", 1245: "手术包", 1246: "增强手术包", 1247: "止血针", 1248: "斧子", 1249: "休闲套装", 1250: "运动背心", 1251: "金丝眼镜", 1252: "橘子耳机", 1253: "纯金徽章", 1254: "皇冠", 1255: "手提袋", 1256: "灵魂私酒"
}

VAR_NAME_MAP = {
    "Count": "物品堆叠数量",
    "BulletCount": "弹药装填数量",
    "Durability": "当前耐久度",
    "DurabilityLoss": "损耗",
    "IsGun": "是否为枪",
    "IsMeleeWeapon": "是否为近战武器",
    "IsBullet": "是否为弹药",
    "Inspected": "已检查"
}

# ==================== JSON 块提取 ====================
def extract_json_block(text: str, key: str) -> str | None:
    idx = text.find(f'"{key}"')
    if idx == -1:
        return None
    start = text.find("{", idx)
    if start == -1:
        return None
    depth = 0
    for i in range(start, len(text)):
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
            if depth == 0:
                return text[start:i + 1]
    return None
   
# ==================== 编辑器 ====================
class DuckovEditor:
    EDITABLE_KEYS = {"Count", "Durability", "DurabilityLoss"}
    READ_ONLY_KEYS = {
        "IsGun",
        "IsMeleeWeapon",
        "IsBullet",
        "Inspected"
        "BulletCount"
    }

    def __init__(self, root: tk.Tk):
        self.root = root
        enable_high_dpi(root)
        
        # ==================== 字体 ====================
        default_font = tkfont.nametofont("TkDefaultFont")

        tree_font = default_font.copy()
        tree_font.configure(size=20)

        heading_font = default_font.copy()
        heading_font.configure(size=20)

        title_font = default_font.copy()
        title_font.configure(size=28, weight="bold")
        
        menu_font = default_font.copy()
        menu_font.configure(size=18)
              
        # ==================== 弹窗 ====================
        def show_about():
            win = tk.Toplevel(root)
            win.title("关于")
            win.geometry("750x300")
            
            win.iconbitmap(icon_path)
            about_title_font = default_font.copy()
            about_title_font.configure(size=28)
            version = get_version()

            tk.Label(
                win,
                text=f"逃离鸭科夫·存档编辑器 v{version}",
                font=about_title_font,
                anchor="w"
            ).pack(pady=10)
            
            about_builder_font = default_font.copy()
            about_builder_font.configure(size=24)
            tk.Label(win, text="作者: 尼克狼唔", font=about_builder_font).pack(pady=5)
            link_font = default_font.copy()
            link_font.configure(size=20)
            link = tk.Label(win, text="项目地址: Github.com/NickWoluff/DuckovSaveEditor",
                            font=link_font, fg="blue", cursor="hand2")
            link.pack(pady=40)
            link.bind("<Button-1>", lambda e: webbrowser.open("https://github.com/NickWoluff/DuckovSaveEditor"))
            
            tk.Label(win, text="仅用于学习用途免费分享, 请勿用于商业分发", font=menu_font).pack(pady=5)
        

        # ================== 菜单栏 ==================
        menubar = tk.Menu(root, font=menu_font)

        tools_menu = tk.Menu(menubar, tearoff=0, font=menu_font)
        tools_menu.add_command(label="刷新", command=self.refresh_tree)
        menubar.add_cascade(label="工具", menu=tools_menu)

        help_menu = tk.Menu(menubar, tearoff=0, font=menu_font)
        help_menu.add_command(label="关于", command=show_about)
        menubar.add_cascade(label="帮助", menu=help_menu)

        root.config(menu=menubar)
        
        # ================== 主体 ==================
        root.title("逃离鸭科夫·存档编辑器    作者: 尼克狼唔 © 2025 Nick Woluff  All rights reserved.")
        root.geometry("1800x1000")
        
        root.iconbitmap(icon_path)
        self.filepath = None
        self.raw_text = ""
        self.entry_map = {}
        self.blocks = []
        self.dirty_entries = set()

        ui_font = tkfont.nametofont("TkDefaultFont")

        style = ttk.Style()
        style.configure(
            "Treeview",
            font=ui_font,
            rowheight=34
        )
        style.configure(
            "Treeview.Heading",
            font=ui_font
        )

        try:
            style.theme_use("vista")
        except:
            pass

        tk.Label(
            root,
            text="逃离鸭科夫·存档编辑器",
            font=title_font
        ).pack(pady=10)
        
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=15)

        tk.Button(btn_frame, text="选择存档文件",
                  command=self.load_file, width=15, height=2).pack(side="left", padx=20)

        tk.Button(btn_frame, text="应用全部修改",
                  command=self.save_file, bg="#2f6566", fg="white",
                  width=15, height=2).pack(side="left", padx=20)

        self.status = tk.Label(root, text="未加载存档", fg="gray")
        self.status.pack()

        container = ttk.Frame(root)
        container.pack(fill="both", expand=True, padx=15, pady=10)

        cols = ("来源", "位置", "ID", "名称", "物品类型",
                "弹药/数量", "耐久度", "损耗", "其他变量")

        self.tree = ttk.Treeview(container, columns=cols, show="headings")
        widths = [100, 200, 80, 300, 150, 180, 150, 120, 420]

        for c, w in zip(cols, widths):
            self.tree.heading(c, text=c)
            self.tree.column(c, width=w, anchor="center")

        vsb = ttk.Scrollbar(container, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        container.rowconfigure(0, weight=1)
        container.columnconfigure(0, weight=1)

        self.tree.bind("<Double-1>", self.edit_item)
        self.tree.tag_configure("dirty", foreground="red")
        self.seen_entries = set()

    # ==================== 加载 ====================
    def load_file(self):
        self.seen_entries.clear()
        default_dir = os.path.expanduser(
            r"~\AppData\LocalLow\TeamSoda\Duckov\Saves"
        )

        path = filedialog.askopenfilename(
            initialdir=default_dir,
            filetypes=[("Save File", "*.sav")]
        )
        if not path:
            return

        self.filepath = path
        self.entry_map.clear()
        self.blocks.clear()
        self.tree.delete(*self.tree.get_children())

        with open(path, "r", encoding="utf-8") as f:
            self.raw_text = f.read()

        found = 0
        targets = [
            ("背包", r"Item\/MainCharacterItemData"),
            ("仓库", r"Inventory\/PlayerStorage")
        ]

        for label, key in targets:
            block = extract_json_block(self.raw_text, key)
            if not block:
                continue
            try:
                obj = json.loads(block)
            except:
                continue
            self.blocks.append((key, obj))
            found += self.walk_entries(obj.get("value", {}), label)

        self.status.config(
            text=f"✔ 成功加载 {found} 件物品" if found else "⚠ 未检测到任何物品",
            fg="green" if found else "orange"
        )

    # ==================== 遍历 ====================
    def walk_entries(self, obj: Any, source: str, pos: int | None = None) -> int:
        count = 0

        if isinstance(obj, dict):
            if source == "仓库" and "entries" in obj:
                for slot in obj["entries"]:
                    slot_pos = slot.get("inventoryPosition")
                    tree = slot.get("itemTreeData", {})
                    count += self.walk_entries(tree, source, slot_pos)

            for v in obj.values():
                count += self.walk_entries(v, source, pos)

            if "typeID" in obj and obj.get("typeID", 0) > 0:
                eid = id(obj)
                if eid not in self.seen_entries:
                    self.seen_entries.add(eid)
                    self.add_row(source, obj, pos)
                    count += 1

        elif isinstance(obj, list):
            for v in obj:
                count += self.walk_entries(v, source, pos)

        return count

    # ==================== 行添加 ====================
    def add_row(self, src: str, entry: dict, pos: int | None):
        if src == "仓库" and (pos is None or pos < 0):
            return

        tid = entry.get("typeID", 0)
        eid = str(id(entry))
        is_dirty = eid in self.dirty_entries
        name = ITEM_NAME_MAP.get(tid, f"未知物品 ({tid})")
        display_name = f"*{name}" if is_dirty else name


        pos_text = "-"
        if src == "仓库" and pos is not None:
            pos_text = f"第{pos // 5 + 1}行 第{pos % 5 + 1}列"

        count_val = ""
        durability = loss = ""
        item_type = ""
        others = []

        for v in entry.get("variables", []):
            key = v.get("key", "")
            val = decode_b64(v.get("data"), v.get("dataType", 0))
            if key in ("Count", "BulletCount"):
                count_val = val
            elif key == "Durability":
                durability = val
            elif key == "DurabilityLoss":
                loss = f"{round(val * 100)}%" if val != "" else ""
            elif key == "IsGun" and val:
                item_type = "枪"
            elif key == "IsMeleeWeapon" and val:
                item_type = "近战武器"
            elif key == "IsBullet" and val:
                item_type = "弹药"
            elif key == "Inspected" and val:
                inspected = "是"
            else:
                others.append(f"{key}:{val}")

        dur_display = str(durability) if durability != "" else ""

        eid = str(id(entry))
        self.entry_map[eid] = entry

        item_id = self.tree.insert(
            "", "end",
            values=(
                src, pos_text, tid, display_name, item_type,
                count_val, dur_display, loss,
                "; ".join(others)
            ),
            tags=(eid,)
        )

        if is_dirty:
            self.tree.item(item_id, tags=(eid, "dirty"))

    def refresh_tree(self):
        self.tree.delete(*self.tree.get_children())
        self.entry_map.clear()
        self.seen_entries.clear()
        for key, obj in self.blocks:
            src = "背包" if "MainCharacter" in key else "仓库"
            self.walk_entries(obj.get("value", {}), src)

    # ==================== 编辑 ====================
    def edit_item(self, event):
        sel = self.tree.focus()
        if not sel:
            return
        entry = self.entry_map[self.tree.item(sel, "tags")[0]]

        win = tk.Toplevel(self.root)
        win.title("修改物品属性")
        win.geometry("600x650")
        win.transient(self.root)
        win.grab_set()
        win.geometry(f"+{event.x_root + 10}+{event.y_root + 10}")

        fields = {}
        row = 0

        for v in entry.get("variables", []):
            key = v.get("key", "")
            val = decode_b64(v.get("data"), v.get("dataType", 0))

            tk.Label(win, text=VAR_NAME_MAP.get(key, key)).grid(row=row, column=0, sticky="e", padx=8, pady=6) # type: ignore

            if key == "DurabilityLoss":
                frame = tk.Frame(win)
                frame.grid(row=row, column=1, padx=8, pady=6, sticky="w")

                ent = tk.Entry(frame, width=10)
                ent.insert(0, str(round(val * 100)))
                ent.pack(side="left")

                tk.Label(frame, text="%").pack(side="left", padx=2)
            else:
                ent = tk.Entry(win, width=22)
                ent.insert(0, str(val))
                ent.grid(row=row, column=1, padx=8, pady=6)

            if key not in self.EDITABLE_KEYS:
                ent.config(state="disabled")

            fields[key] = (ent, v)
            row += 1

        def apply():
            changed = False
            for key, (w, v) in fields.items():
                if key in self.EDITABLE_KEYS:
                    old = decode_b64(v.get("data"), v.get("dataType", 0))
                    new = w.get()
                    if key == "DurabilityLoss":
                        try:
                            new_val = float(new) / 100
                        except:
                            new_val = 0
                    else:
                        new_val = new

                    if str(old) != str(new_val):
                        v["data"] = encode_b64(new_val, v.get("dataType", 0)) # type: ignore
                        changed = True

            if changed:
                eid = str(id(entry))
                self.dirty_entries.add(eid)
                self.refresh_tree()

            messagebox.showinfo("修改成功", "修改已保存，点击“应用全部修改”后生效\n若为手滑，点击“确认”后直接关闭该应用可撤销操作")
            win.destroy()

        tk.Button(win, text="确认修改", command=apply,
                bg="green", fg="white", width=24).grid(
            row=row, column=0, columnspan=2, pady=25
        )

    # ==================== 保存 ====================
    def save_file(self):
        if not self.filepath:
            return
        backup = self.filepath + ".backup"
        shutil.copy(self.filepath, backup)

        new_text = self.raw_text
        for key, obj in self.blocks:
            block = json.dumps(obj, ensure_ascii=False, indent=4)
            old = extract_json_block(new_text, key)
            if old:
                new_text = new_text.replace(old, block, 1)

        with open(self.filepath, "w", encoding="utf-8") as f:
            f.write(new_text)

        messagebox.showinfo("应用成功", f"已应用全部修改，请重新启动游戏\n旧存档已备份在相同目录下: {os.path.basename(backup)}\n\n注意: 请勿重复应用修改，否则可能导致备份存档被覆盖！")
        self.dirty_entries.clear()
        self.refresh_tree()

if __name__ == "__main__":
    root = tk.Tk()
    def setup_global_font(size: int):
        default_font = tkfont.nametofont("TkDefaultFont")
        default_font.configure(size=size)

        text_font = tkfont.nametofont("TkTextFont")
        text_font.configure(size=size)

        fixed_font = tkfont.nametofont("TkFixedFont")
        fixed_font.configure(size=size)

    # 使用
    setup_global_font(20)
    DuckovEditor(root)
    root.mainloop()